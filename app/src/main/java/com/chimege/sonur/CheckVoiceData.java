package com.chimege.sonur;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech.Engine;
import java.util.ArrayList;

public class CheckVoiceData extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ArrayList<String> availableLanguages = new ArrayList<>();
        availableLanguages.add("eng");
        availableLanguages.add("mon");

        final Intent returnData = new Intent();
        returnData.putStringArrayListExtra(Engine.EXTRA_AVAILABLE_VOICES, availableLanguages);
        setResult(Engine.CHECK_VOICE_DATA_PASS, returnData);
        finish();
    }
}
