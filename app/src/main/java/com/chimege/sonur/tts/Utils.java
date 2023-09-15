package com.chimege.sonur.tts;
import android.util.Pair;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Utils {
    public static void pause(int duration) {
        try {
            Thread.sleep(duration);
        } catch (InterruptedException ignored) {}
    }

    public static byte[] readAllBytes(InputStream inputStream) throws IOException {
        final int bufLen = 4 * 0x400; // 4KB
        byte[] buf = new byte[bufLen];
        int readLen;
        IOException exception = null;

        try {
            try (ByteArrayOutputStream outputStream = new ByteArrayOutputStream()) {
                while ((readLen = inputStream.read(buf, 0, bufLen)) != -1)
                    outputStream.write(buf, 0, readLen);

                return outputStream.toByteArray();
            }
        } catch (IOException e) {
            exception = e;
            throw e;
        } finally {
            if (exception == null) inputStream.close();
            else try {
                inputStream.close();
            } catch (IOException e) {
                exception.addSuppressed(e);
            }
        }
    }

    public static List<Pair<Integer, Integer>> calcChunks(int length, int chunkLength, int overlapLength) {
        List<Pair<Integer, Integer>> chunks = new ArrayList<>();
        for (int i = 0; i < length; i += chunkLength) {
            if (i < length - 1) {
                chunks.add(new Pair<>(i, Math.min(i + chunkLength + overlapLength, length - 1)));
            }
        }
        return chunks;
    }

    public static Pair<float[], float[]> audioOverlapHandler(float[] audio, int overlapLength, float[] previousBuffer, boolean notLast) {
        int overlapAudioLength = overlapLength * 256;
        float[] buffer_to_save = null;
        if (notLast) {
            buffer_to_save = Arrays.copyOfRange(audio, audio.length - overlapAudioLength, audio.length);
            audio = Arrays.copyOfRange(audio, 0, audio.length - overlapAudioLength);
        }
        if (previousBuffer != null) {
            float step = 1 / (float) overlapAudioLength;
            for (int i = 0; i < Math.min(overlapAudioLength, audio.length); i++) {
                float delta = i * step;
                audio[i] = audio[i] * delta + previousBuffer[i] * (1 - delta);
            }
        }
        return new Pair<>(audio, buffer_to_save);
    }

    public static byte[] pauseBuffer(float speed, byte lastVal) {
        int pauseBufferSize = (int) ((4000 / speed) + 1);
        byte[] pauseBuffer = new byte[pauseBufferSize];
        for (int i = 0; i < pauseBufferSize; i++) {
            pauseBuffer[i] = (byte) (lastVal * Math.max(0, 1 - (i / ((float) pauseBufferSize * 0.25))));
        }
        return pauseBuffer;
    }
}
