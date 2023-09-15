package com.chimege.sonur;

import android.content.Context;
import android.content.res.TypedArray;
import android.util.AttributeSet;
import android.util.Log;

import androidx.appcompat.app.AlertDialog;
import androidx.preference.DialogPreference;

import java.util.Arrays;

public class SonurVoicePreference extends DialogPreference {
    private String mValue;
    private String[] titles;
    private PlayVoice player;

    public void setEntries(String[] voice_name) {
        titles = voice_name;
    }

    public void setPlayer(PlayVoice tts) {
        player = tts;
    }

    public interface PlayVoice {
        void play();
    }

    public SonurVoicePreference(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public SonurVoicePreference(Context context) {
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
        int index = mValue != null ? Arrays.asList(titles).indexOf(mValue) : -1;
        builder.setSingleChoiceItems(titles, index, (dialog, which) -> {
            mValue = titles[which];
            persistString(mValue);
            player.play();
        });
        builder.setPositiveButton("OK", (dialogInterface, i) -> notifyChanged());
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
