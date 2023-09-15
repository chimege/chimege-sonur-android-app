package com.chimege.sonur.tts;

import static com.chimege.sonur.tts.Utils.audioOverlapHandler;
import static com.chimege.sonur.tts.Utils.calcChunks;
import static com.chimege.sonur.tts.Utils.pause;
import static com.chimege.sonur.tts.Utils.pauseBuffer;
import static com.chimege.sonur.tts.Utils.readAllBytes;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.speech.tts.SynthesisCallback;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.speech.tts.Voice;
import android.util.Log;
import android.util.Pair;

import java.io.File;
import java.io.IOException;
import java.lang.NullPointerException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;
import java.nio.LongBuffer;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

import ai.onnxruntime.OnnxTensor;
import ai.onnxruntime.OrtEnvironment;
import ai.onnxruntime.OrtException;
import ai.onnxruntime.OrtSession;
import kotlin.Triple;

public class Synthesizer implements TextToSpeech.OnInitListener {

    @Override
    public void onInit(int status) {
        defaultVoices = new HashMap<>();
        try {
            for (String language : Config.languages) {
                Set<Voice> voices = defaultTTS.getVoices();
                if (voices != null) {
                    List<Voice> filteredVoices = voices
                            .stream()
                            .filter(voice -> voice.getLocale().getLanguage().toLowerCase(Locale.ROOT).contains(language))
                            .filter(voice -> !voice.isNetworkConnectionRequired())
                            .collect(Collectors.toList());
                    if (voices.size() > 0) {
                        defaultVoices.put(language, filteredVoices);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (unfinished_business != null) {
            send_default_request(unfinished_business.component1(), unfinished_business.component2(), unfinished_business.component3());
            unfinished_business = null;
        }
    }

    private final Context mContext;
    private String currentVoice;
    public final Preprocessor preprocessor;

    private OrtSession encoder = null;
    private OrtSession decoder = null;
    private boolean waitingDefaultTTS = false;
    AudioBuffer audioBuffer;

    private TextToSpeech defaultTTS;
    private String defaultTTSCode = "com.google.android.tts";
    private HashMap<String, List<Voice>> defaultVoices = null;
    private Triple<String, Config, String> unfinished_business = null;
    private String currentLanguage = "en";

    public Synthesizer(Context context) {
        mContext = context;
        preprocessor = new Preprocessor(context);
        SharedPreferences settings = PreferenceManager.getDefaultSharedPreferences(context);
        loadModel(settings.getString("voice", "Эмэгтэй small"));
        defaultTTS = new TextToSpeech(context, this, "com.google.android.tts");
    }

    public void loadModel(String name) {
        try {
            currentVoice = name;
            OrtEnvironment ortEnv = OrtEnvironment.getEnvironment();
            Pair<String, String> selection = Config.voices.get(name);
            if (selection == null) {
                selection = Objects.requireNonNull(Config.voices.get("Эмэгтэй 1"));
            }
            String encoderName = selection.first;
            String decoderName = selection.second;
            byte[] encoderBytes = readAllBytes(mContext.getAssets().open(encoderName + ".onnx"));
            byte[] decoderBytes = readAllBytes(mContext.getAssets().open(decoderName + ".onnx"));
            encoder = ortEnv.createSession(encoderBytes);
            decoder = ortEnv.createSession(decoderBytes);
        } catch (IOException | OrtException e) {
            e.printStackTrace();
        }
    }

    public void speak_with_chimege_tts(String text, Config config) {
        if (!audioBuffer.isStopped) {
            if (text.length() == 0) {
                return;
            }
            config.overlapLength = Math.min(config.overlapLength, (config.decoderChunkSize - 10) / 2);
            try {
                long[] indices = new long[text.length()];
                float[] pauses = new float[text.length()];
                for (int i = 0; i < text.length(); i++) {
                    String symbolsToId = "_-!'(),.:;? абвгдеёжзийклмноөпрстуүфхцчшъыьэюя";
                    indices[i] = symbolsToId.indexOf(text.charAt(i));
                    if ((i > 0) && (text.charAt(i) == ' ') && (".,!?".indexOf(text.charAt(i - 1)) == -1)) {
                        if (config.pause < 30) {
                            pauses[i] = (float) config.pause;
                        } else {
                            pauses[i] = 0.0f;
                        }
                    } else {
                        pauses[i] = 0.0f;
                    }
                }

                Map<String, OnnxTensor> encoderInput = new HashMap<>();
                OrtEnvironment ortEnv = OrtEnvironment.getEnvironment();

                encoderInput.put("text", OnnxTensor.createTensor(ortEnv, LongBuffer.wrap(indices), new long[]{1, text.length()}));
                encoderInput.put("text_lengths", OnnxTensor.createTensor(ortEnv, LongBuffer.wrap(new long[]{text.length()}), new long[]{1}));
                encoderInput.put("pause", OnnxTensor.createTensor(ortEnv, FloatBuffer.wrap(pauses), new long[]{1, text.length()}));
                encoderInput.put("speed", OnnxTensor.createTensor(ortEnv, FloatBuffer.wrap(new float[]{1}), new long[]{1}));

                OrtSession.Result encoderOutput = encoder.run(encoderInput);
                float[][][] z = (float[][][]) encoderOutput.get(0).getValue();
                int B = z.length;
                int F = z[0].length;
                int L = z[0][0].length;

                List<Pair<Integer, Integer>> slices = calcChunks(L, config.decoderChunkSize, config.overlapLength);
                float[] previousBuffer = null;
                byte lastVal = 0;
                for (int s = 0; s < slices.size(); s++) {
                    if (audioBuffer.isStopped) {
                        break;
                    }
                    try {
                        Pair<Integer, Integer> slice = slices.get(s);
                        int size = slice.second - slice.first;
                        float[][][] tmp = new float[B][F][size];
                        for (int i = 0; i < B; i++) {
                            for (int j = 0; j < F; j++) {
                                System.arraycopy(z[i][j], slice.first, tmp[i][j], 0, size);
                            }
                        }

                        Map<String, OnnxTensor> decoderInput = new HashMap<>();
                        decoderInput.put("z", OnnxTensor.createTensor(ortEnv, tmp));
                        OrtSession.Result decoderOutput = decoder.run(decoderInput);
                        float[] rawAudio = ((float[][][]) decoderOutput.get(0).getValue())[0][0];
                        Pair<float[], float[]> overlapResult = audioOverlapHandler(
                                rawAudio,
                                config.overlapLength,
                                previousBuffer,
                                s < (slices.size() - 1)
                        );
                        rawAudio = overlapResult.first;
                        previousBuffer = overlapResult.second;

                        rawAudio = Resample.resample(rawAudio, rawAudio.length, false, 22050, config.defaultSamplingRate);

                        byte[] audioData = new byte[2 * rawAudio.length];
                        ByteBuffer convertBuffer = ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN);
                        for (int i = 0; i < rawAudio.length; i++) {
                            convertBuffer.clear();
                            convertBuffer.putShort((short) (rawAudio[i] * 32767));
                            audioData[i * 2] = convertBuffer.get(0);
                            audioData[i * 2 + 1] = convertBuffer.get(1);
                        }

                        Sonic sonic = new Sonic(22050, 1);
                        int bufferSize = audioData.length;
                        int outBufferSize = (int) ((bufferSize / config.speed) + 1);
                        byte[] outBuffer = new byte[outBufferSize];
                        sonic.setSpeed(config.speed);
                        sonic.setPitch(config.pitch);
                        sonic.setVolume(config.volume);
                        sonic.writeBytesToStream(audioData, bufferSize);
                        sonic.flushStream();
                        sonic.readBytesFromStream(outBuffer, outBufferSize);

                        while (waitingDefaultTTS) {
                            if (audioBuffer.isStopped) {
                                break;
                            }
                            pause(100);
                        }
                        audioBuffer.add(outBuffer);
                        lastVal = outBuffer[outBuffer.length - 1];
                    } catch (OrtException e) {
                        Log.e("CHIMEGE", "Decoder Err:" + text + ":" + s + ":" + e);
                    }
                }
                audioBuffer.add(pauseBuffer(config.speed, lastVal));
            } catch (OrtException e) {
                Log.e("CHIMEGE", "Encoder Err:" + text + ":" + e);
            }
        }
    }

    public class DefaultTtsListener extends UtteranceProgressListener {
        private final int BUFFER_SIZE = 4000;
        private int cursor = 0;
        private byte[] buffer = new byte[BUFFER_SIZE];
        private final AudioBuffer mBuffer;

        public DefaultTtsListener(AudioBuffer buffer) {
            mBuffer = buffer;
        }

        @Override
        public void onStart(String s) {
        }

        @Override
        public void onAudioAvailable(String utteranceId, byte[] audio) {
            for (byte b : audio) {
                buffer[cursor] = b;
                cursor += 1;
                if (cursor == BUFFER_SIZE) {
                    mBuffer.add(buffer);
                    buffer = new byte[BUFFER_SIZE];
                    cursor = 0;
                }
            }
        }

        @Override
        public void onDone(String s) {
            mBuffer.add(buffer);
            waitingDefaultTTS = false;
        }

        @Override
        public void onError(String s) {
        }
    }

    private void send_default_request(String text, Config config, String language) {
        try {
            if (!currentLanguage.equals(language)) {
                currentLanguage = language;
                defaultTTS.setLanguage(new Locale(language));
            }
            defaultTTS.setSpeechRate(config.defaultSpeed);
            defaultTTS.setPitch(config.defaultPitch);
            List<Voice> voices = defaultVoices.get(language);
            if (voices != null) {
                Integer voiceIdx = config.defaultVoiceIdx.get(language);
                if (voiceIdx != null) {
                    if (voiceIdx < voices.size()) {
                        Voice voice = voices.get(voiceIdx);
                        if (voice != null) {
                            defaultTTS.setVoice(voice);
                        }
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            File file = File.createTempFile("default", "wav");
            defaultTTS.setOnUtteranceProgressListener(new DefaultTtsListener(audioBuffer));
            defaultTTS.synthesizeToFile(text, new Bundle(), file, text);
            waitingDefaultTTS = true;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void speak_with_default_tts(String text, Config config, String language) {
        if (!audioBuffer.isStopped) {
            if (!defaultTTSCode.equals(config.defaultTTSCode)) {
                defaultTTSCode = config.defaultTTSCode;
                defaultTTS = new TextToSpeech(mContext, this, defaultTTSCode);
                unfinished_business = new Triple<>(text, config, language);
            } else {
                send_default_request(text, config, language);
            }
        }
    }

    public void synthesize(String text, Config config, SynthesisCallback callback) {
        if (!currentVoice.equals(config.voice)) {
            loadModel(config.voice);
        }
        List<Pair<String, String>> text_with_languages = preprocessor.normalize(text, config);
        waitingDefaultTTS = false;
        audioBuffer = new AudioBuffer(callback, config.defaultSamplingRate);
        for (Pair<String, String> chunk : text_with_languages) {
            final String chunk_text = chunk.second;
            final String language = chunk.first;
            Log.d("CHIMEGE:", chunk_text);
            if (language.equals("mn")) {
                speak_with_chimege_tts(chunk_text, config);
            } else {
                if (defaultTTS != null) {
                    speak_with_default_tts(chunk_text, config, language);
                }
            }
        }
        while (audioBuffer.isSpeaking || waitingDefaultTTS) {
            if (audioBuffer.isStopped) {
                break;
            }
            pause(100);
        }
        callback.done();
    }

    public void stop() {
        if (audioBuffer != null) {
            audioBuffer.stop();
        }
    }
}
