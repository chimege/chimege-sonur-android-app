package com.chimege.sonur.tts;

public class Resample {
    public static float[] resample(float[] data, int length, boolean stereo, int inFrequency, int outFrequency) {
        if (inFrequency < outFrequency)
            return upsample(data, length, stereo, inFrequency, outFrequency);

        if (inFrequency > outFrequency)
            return downsample(data, length, stereo, inFrequency, outFrequency);

        return trimArray(data, length);
    }

    private static float[] upsample(float[] data, int length, boolean inputIsStereo, int inFrequency, int outFrequency) {

        // Special case for no action
        if (inFrequency == outFrequency)
            return trimArray(data, length);

        double scale = (double) inFrequency / (double) outFrequency;
        double pos = 0;
        float[] output;

        if (!inputIsStereo) {
            output = new float[(int) (length / scale)];
            for (int i = 0; i < output.length; i++) {
                int inPos = (int) pos;
                double proportion = pos - inPos;
                if (inPos >= length - 1) {
                    inPos = length - 2;
                    proportion = 1;
                }

                output[i] = (float) (data[inPos] * (1 - proportion) + data[inPos + 1] * proportion);
                pos += scale;
            }
        } else {
            output = new float[2 * (int) ((length / 2) / scale)];
            for (int i = 0; i < output.length / 2; i++) {
                int inPos = (int) pos;
                double proportion = pos - inPos;

                int inRealPos = inPos * 2;
                if (inRealPos >= length - 3) {
                    inRealPos = length - 4;
                    proportion = 1;
                }

                output[i * 2] = (float) (data[inRealPos] * (1 - proportion) + data[inRealPos + 2] * proportion);
                output[i * 2 + 1] = (float) (data[inRealPos + 1] * (1 - proportion) + data[inRealPos + 3] * proportion);
                pos += scale;
            }
        }

        return output;
    }

    private static float[] downsample(float[] data, int length, boolean inputIsStereo, int inFrequency, int outFrequency) {

        // Special case for no action
        if (inFrequency == outFrequency)
            return trimArray(data, length);

        double scale = (double) outFrequency / (double) inFrequency;
        float[] output;
        double pos = 0;
        int outPos = 0;

        if (!inputIsStereo) {
            double sum = 0;
            output = new float[(int) (length * scale)];
            int inPos = 0;

            while (outPos < output.length) {
                double firstVal = data[inPos++];
                double nextPos = pos + scale;
                if (nextPos >= 1) {
                    sum += firstVal * (1 - pos);
                    output[outPos++] = (float) (sum);
                    nextPos -= 1;
                    sum = nextPos * firstVal;
                } else {
                    sum += scale * firstVal;
                }
                pos = nextPos;

                if (inPos >= length && outPos < output.length) {
                    output[outPos++] = (float) (sum / pos);
                }
            }
        } else {
            double sum1 = 0, sum2 = 0;
            output = new float[2 * (int) ((length / 2) * scale)];
            int inPos = 0;

            while (outPos < output.length) {
                double firstVal = data[inPos++], nextVal = data[inPos++];
                double nextPos = pos + scale;
                if (nextPos >= 1) {
                    sum1 += firstVal * (1 - pos);
                    sum2 += nextVal * (1 - pos);
                    output[outPos++] = (float) (sum1);
                    output[outPos++] = (float) (sum2);
                    nextPos -= 1;
                    sum1 = nextPos * firstVal;
                    sum2 = nextPos * nextVal;
                } else {
                    sum1 += scale * firstVal;
                    sum2 += scale * nextVal;
                }
                pos = nextPos;

                if (inPos >= length && outPos < output.length) {
                    output[outPos++] = (float) (sum1 / pos);
                    output[outPos++] = (float) (sum2 / pos);
                }
            }
        }

        return output;
    }

    /**
     * @param data   Data
     * @param length Length of valid data
     * @return Array trimmed to length (or same array if it already is)
     */
    public static float[] trimArray(float[] data, int length) {
        if (data.length == length)
            return data;

        float[] output = new float[length];
        System.arraycopy(output, 0, data, 0, length);
        return output;
    }
}
