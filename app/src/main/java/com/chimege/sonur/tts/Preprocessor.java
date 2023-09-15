package com.chimege.sonur.tts;

import android.content.Context;
import android.util.Pair;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.util.ArrayList;
import java.util.List;

public class Preprocessor {
    final PyObject module;

    public Preprocessor(Context context) {
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(context));
        }
        Python py = Python.getInstance();
        module = py.getModule("process");
    }

    public List<Pair<String, String>> normalize(String text, Config config) {
        PyObject normalized = module.callAttr("process", text,
                config.readEmoji,
                config.abbreviationLevel,
                config.numberChunkSize,
                config.dontReadNumberJunction,
                config.readDotNumbersAsListIndex,
                config.symbolReadOption,
                config.foreignCharacterOption,
                config.charSplitSize
        );
        List<Pair<String, String>> result = new ArrayList<>();
        for (PyObject segment: normalized.asList()) {
            List<PyObject> row = segment.asList();
            result.add(new Pair<>(
                    row.get(0).toString(),
                    row.get(1).toString()
            ));
        }
        return result;
    }
}
