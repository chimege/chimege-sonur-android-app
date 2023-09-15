package com.chimege.sonur;

import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.speech.tts.SynthesisCallback;
import android.speech.tts.SynthesisRequest;
import android.speech.tts.TextToSpeech;
import android.speech.tts.TextToSpeechService;

import com.chimege.sonur.tts.Synthesizer;
import com.chimege.sonur.tts.Config;

public class TtsService extends TextToSpeechService {
    private Synthesizer synthesizer = null;

    @Override
    public void onCreate() {
        super.onCreate();
        synthesizer = new Synthesizer(this);
    }

    @Override
    protected void onStop() {
        synthesizer.stop();
    }

    @Override
    protected void onSynthesizeText(SynthesisRequest synthesisRequest, SynthesisCallback synthesisCallback) {
        SharedPreferences settings = PreferenceManager.getDefaultSharedPreferences(this);
        Config normConfig = new Config(settings, synthesisRequest);
        synthesizer.synthesize(
                synthesisRequest.getCharSequenceText().toString(),
                normConfig,
                synthesisCallback
        );
    }

    @Override
    protected String[] onGetLanguage() {
        return new String[] { "mn", "MNG", "" };
    }

    @Override
    protected int onIsLanguageAvailable(String language, String country, String variant) {
        return TextToSpeech.LANG_AVAILABLE;
    }

    @Override
    protected int onLoadLanguage(String language, String country, String variant) {
        return TextToSpeech.LANG_AVAILABLE;
    }
}