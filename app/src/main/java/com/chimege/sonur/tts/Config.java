package com.chimege.sonur.tts;

import android.content.SharedPreferences;
import android.speech.tts.SynthesisRequest;
import android.util.Pair;
import java.util.HashMap;
import java.util.Map;

public class Config {
    public String voice;
    public float speed;
    public float pitch;
    public float volume;
    public float defaultSpeed;
    public float defaultPitch;
    public int decoderChunkSize;
    public int overlapLength;
    public int charSplitSize;
    public boolean readEmoji;
    public String abbreviationLevel;
    public String numberChunkSize;
    public boolean dontReadNumberJunction;
    public boolean readDotNumbersAsListIndex;
    public String symbolReadOption;
    public String foreignCharacterOption;
    public String defaultTTSCode;
    public Map<String, Integer> defaultVoiceIdx;
    public int defaultSamplingRate;
    public long pause;

    public final static String[] languages = new String[]{"en", "ja", "ko"};
    public static Map<String, Pair<String, String>> voices = new HashMap<String, Pair<String, String>>() {
        {
            put("Эмэгтэй 1", new Pair<>("female1", "female1_vocoderv3"));
            put("Эмэгтэй tiny", new Pair<>("female1_tiny", "female1_tiny_vocoderv3"));
            put("Эмэгтэй 2", new Pair<>("female2", "female2_vocoderv3"));
            put("Эмэгтэй 3", new Pair<>("female3", "female3_vocoderv3"));
            put("Эрэгтэй 1", new Pair<>("male1", "male1_vocoderv3"));
            put("Эрэгтэй 2", new Pair<>("male2", "male2_vocoderv3"));
            put("Эрэгтэй 3", new Pair<>("male3", "male3_vocoderv3"));
        }
    };

    public Config(SharedPreferences settings, SynthesisRequest request) {
        voice = settings.getString("voice", "Эмэгтэй small");
        speed = (float) (settings.getInt("speed", 100) / 100.0);
        pitch = (float) (settings.getInt("pitch", 100) / 100.0);
        volume = (float) (settings.getInt("volume", 100) / 100.0);
        decoderChunkSize = settings.getInt("decoderChunkSize", 100);
        overlapLength = settings.getInt("overlapLength", 10);
        charSplitSize = settings.getInt("charSplitSize", 50);
        readEmoji = settings.getBoolean("readEmoji", true);
        abbreviationLevel = settings.getString("abbreviationLevel", "abbreviation");  // letter abbreviation skip
        numberChunkSize = settings.getString("numberChunkSize", "default"); //# double, single, whole, default
        dontReadNumberJunction = settings.getBoolean("dontReadNumberJunction", false);
        readDotNumbersAsListIndex = settings.getBoolean("readDotNumbersAsListIndex", false);
        symbolReadOption = settings.getString("symbolReadOption", "no_temdegt"); //"no_temdegt" # buh_temdegt, tugeemel_temdegt, no_temdegt, unshih_custom_temdegt, unshihgui_custom_temdegt
        foreignCharacterOption = settings.getString("foreignCharacterOption", "normalize"); // skip, normalize, leave
        defaultTTSCode = settings.getString("defaultEngine", "com.google.android.tts");
        defaultVoiceIdx = new HashMap<>();
        for (String language : Config.languages) {
            defaultVoiceIdx.put(language, Integer.parseInt(settings.getString("language_" + language, "0")));
        }
        defaultSpeed = (float) request.getSpeechRate() / 100;
        defaultPitch = (float) request.getPitch() / 100;
        defaultSamplingRate = Integer.parseInt(settings.getString("default_engine_sr", "22050"));
        pause = settings.getInt("pauseBetweenWords", 0);
    }
}
