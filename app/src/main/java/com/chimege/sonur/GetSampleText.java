package com.chimege.sonur;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;

public class GetSampleText extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        final String text = "Энэ бол жишээ бичвэр. This is an example";

        final int result = TextToSpeech.LANG_AVAILABLE;
        final Intent returnData = new Intent();
        returnData.putExtra(TextToSpeech.Engine.EXTRA_SAMPLE_TEXT, text);
        setResult(result, returnData);
        finish();
    }
}
