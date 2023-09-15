package com.chimege.sonur;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.speech.tts.TextToSpeech;
import android.speech.tts.Voice;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.ListPreference;
import androidx.preference.PreferenceFragmentCompat;
import androidx.preference.PreferenceGroup;

import com.chimege.sonur.tts.Config;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.stream.Collectors;

public class TtsSettingsActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.settings_activity);
        if (savedInstanceState == null) {
            getSupportFragmentManager()
                    .beginTransaction()
                    .replace(R.id.settings, new SettingsFragment())
                    .commit();
        }
        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(false);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.options, menu);
        return true;
    }

    @SuppressLint("NonConstantResourceId")
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == R.id.ttsSettings) {
            launchGeneralTtsSettings();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void launchGeneralTtsSettings() {
        Intent intent;
        intent = new Intent("com.android.settings.TTS_SETTINGS");
        startActivity(intent);
    }

    public static class SettingsFragment extends PreferenceFragmentCompat implements TextToSpeech.OnInitListener, SharedPreferences.OnSharedPreferenceChangeListener {
        private TextToSpeech defaultTTS;
        private TextToSpeech chimegeTTS;

        @Override
        public void onInit(int i) {
            PreferenceGroup group = (PreferenceGroup) getPreferenceScreen().getPreference(2);
            ListPreference preference = (ListPreference) group.getPreference(0);
            List<TextToSpeech.EngineInfo> tts = defaultTTS.getEngines();
            List<CharSequence> names = new ArrayList<>();
            List<CharSequence> codes = new ArrayList<>();
            for (int j = 0; j < tts.size(); j++) {
                if (tts.get(j).name.equals("com.chimege.sonur")) {
                    continue;
                }
                names.add(tts.get(j).label);
                codes.add(tts.get(j).name);
            }
            preference.setEntries(names.toArray(new CharSequence[]{}));
            preference.setEntryValues(codes.toArray(new CharSequence[]{}));
            for (String language : Config.languages) {
                group.removePreferenceRecursively("language_" + language);
                Set<Voice> voices = defaultTTS.getVoices();
                if (voices == null) {
                    continue;
                }
                List<Voice> filteredVoices = voices
                        .stream()
                        .filter(voice -> voice.getLocale().getLanguage().toLowerCase(Locale.ROOT).contains(language))
                        .filter(voice -> !voice.isNetworkConnectionRequired())
                        .collect(Collectors.toList());
                if (filteredVoices.size() > 0) {
                    String[] voice_name = new String[filteredVoices.size()];
                    String[] voice_idx = new String[filteredVoices.size()];
                    for (int j = 0; j < filteredVoices.size(); j++) {
                        voice_name[j] = filteredVoices.get(j).getName();
                        voice_idx[j] = Integer.toString(j);
                    }
                    VoicePreference voicePrefs = new VoicePreference(requireContext());
                    voicePrefs.setKey("language_" + language);
                    voicePrefs.setTitle("Хэл " + language);
                    voicePrefs.setEntries(voice_name);
                    voicePrefs.setEntryValues(voice_idx);
                    voicePrefs.setVoices(filteredVoices);
                    voicePrefs.setPlayer((voice) -> {
                        defaultTTS.setVoice(voice);
                        switch (language) {
                            case "en":
                                defaultTTS.speak("This is an example text", 0, null, "");
                                break;
                            case "ja":
                                defaultTTS.speak("これはサンプルテキストです", 0, null, "");
                                break;
                            case "ko":
                                defaultTTS.speak("이것은 예제 텍스트입니다", 0, null, "");
                                break;
                        }
                    });
                    group.addPreference(voicePrefs);
                }
            }
        }

        @Override
        public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
            setPreferencesFromResource(R.xml.root_preferences, rootKey);
            SharedPreferences settings = PreferenceManager.getDefaultSharedPreferences(getContext());
            defaultTTS = new TextToSpeech(getContext(), this, settings.getString("defaultEngine", ""));
            chimegeTTS = new TextToSpeech(getContext(), null, "com.chimege.sonur");

            PreferenceGroup group = (PreferenceGroup) getPreferenceScreen().getPreference(0);
            SonurVoicePreference voicePrefs = new SonurVoicePreference(requireContext());
            voicePrefs.setKey("voice");
            voicePrefs.setTitle("Сонурын хоолой");
            voicePrefs.setEntries(Config.voices.keySet().toArray(new String[]{}));
            voicePrefs.setPlayer(() -> chimegeTTS.speak("Энэ бол жишээ өгүүлбэр", 0, null, ""));
            group.addPreference(voicePrefs);
        }

        @Override
        public void onStart() {
            super.onStart();
            SharedPreferences mSettings = PreferenceManager.getDefaultSharedPreferences(getContext());
            mSettings.registerOnSharedPreferenceChangeListener(this);
        }

        @Override
        public void onStop() {
            super.onStop();
            SharedPreferences mSettings = PreferenceManager.getDefaultSharedPreferences(getContext());
            mSettings.unregisterOnSharedPreferenceChangeListener(this);
        }

        @Override
        public void onSharedPreferenceChanged(SharedPreferences prefs, String key) {
            if (key.equals("defaultEngine")) {
                defaultTTS = new TextToSpeech(getContext(), this, prefs.getString(key, ""));
            }
        }
    }
}