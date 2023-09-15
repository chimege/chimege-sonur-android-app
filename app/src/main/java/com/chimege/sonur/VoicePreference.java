package com.chimege.sonur;

import java.util.Arrays;
import java.util.List;

import android.content.Context;
import android.content.res.TypedArray;

import androidx.appcompat.app.AlertDialog;
import androidx.preference.DialogPreference;

import android.speech.tts.Voice;
import android.util.AttributeSet;
import android.util.Log;

public class VoicePreference extends DialogPreference {
    private String mValue;
    private String[] titles;
    private String[] values;
    private PlayVoice player;
    private List<Voice> voices;

    public void setEntries(String[] voice_name) {
        titles = voice_name;
    }

    public void setEntryValues(String[] voice_idx) {
        values = voice_idx;
    }

    public void setPlayer(PlayVoice tts) {
        player = tts;
    }

    public void setVoices(List<Voice> voices) {
        this.voices = voices;
    }

    public interface PlayVoice {
        void play(Voice voice);
    }

    public VoicePreference(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public VoicePreference(Context context) {
        this(context, null);
    }

    @Override
    public CharSequence getSummary() {
        try {
            return titles[Integer.parseInt(mValue)];
        } catch (Exception e) {
            Log.d("CHIMEGE:", "VALUE:" + mValue);
            return "";
        }
    }

    @Override
    protected void onClick() {
        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        int index = mValue != null ? Arrays.asList(values).indexOf(mValue) : -1;
        builder.setSingleChoiceItems(titles, index, (dialog, which) -> {
            player.play(voices.get(which));
            mValue = values[which];
        });
        builder.setPositiveButton("OK", (dialogInterface, i) -> {
            persistString(mValue);
            notifyChanged();
        });
        builder.setNegativeButton("Cancel", (dialogInterface, i) -> {});
        AlertDialog mDialog = builder.create();
        mDialog.show();
    }

    @Override
    protected Object onGetDefaultValue(TypedArray a, int index) {
        return a.getString(index);
    }

    @Override
    protected void onSetInitialValue(boolean restoreValue, Object defaultValue) {
        if (restoreValue)
            mValue = getPersistedString("");
        else {
            persistString(titles[0]);
        }
    }
}
