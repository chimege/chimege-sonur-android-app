package com.chimege.sonur.tts;

import static com.chimege.sonur.tts.Utils.pause;
import android.media.AudioFormat;
import android.speech.tts.SynthesisCallback;
import java.util.ArrayList;

public class AudioBuffer {
    public ArrayList<byte[]> queue;
    public boolean isSpeaking;
    public boolean isStopped;
    public final SynthesisCallback mCallback;
    public Thread processor;
    public long startTime;

    public AudioBuffer(SynthesisCallback callback, int sampleRate) {
        queue = new ArrayList<>();
        isSpeaking = false;
        isStopped = false;
        mCallback = callback;
        mCallback.start(sampleRate, AudioFormat.ENCODING_PCM_16BIT, 1);
        processor = null;
    }

    public void add(byte[] audio) {
        if (!isStopped) {
            if (processor == null) {
                startTime = System.currentTimeMillis();
            }
            queue.add(audio);
            if (!isSpeaking) {
                isSpeaking = true;
                processor = new Thread(this::next);
                processor.start();
            }
        }
    }

    public void next() {
        while (queue.size() > 0) {
            if (isStopped) {
                break;
            }
            play(queue.remove(0));
        }
        isSpeaking = false;
    }

    public void stop() {
        queue = new ArrayList<>();
        isSpeaking = false;
        isStopped = true;
        if (processor != null && processor.isAlive()) {
            processor.interrupt();
        }
    }

    public void play(byte[] audio) {
        if (audio == null || audio.length == 0) {
            return;
        }
        final int maxBytesToCopy = mCallback.getMaxBufferSize();
        int outOffset = 0;
        while (outOffset < audio.length) {
            if (isStopped) {
                break;
            } else {
                final int bytesToWrite = Math.min(maxBytesToCopy, (audio.length - outOffset));
                mCallback.audioAvailable(audio, outOffset, bytesToWrite);
                outOffset += bytesToWrite;
            }
            pause(10);
        }
    }
}
