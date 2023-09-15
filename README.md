# Chimege Text To Speech Engine for Android Talkback
## Dependencies
1. Android Studio (Arctic Fox 2020.03.01 or above)
2. Android SDK (33, minimum SDK 26)
3. Gradle (7.4 or above)
4. Chimege ONNX TTS Voice Models
5. JAVA JDK (16.0.1 or above)
6. Python 3.8 (with pip installed)

## Build Instruction
1. Copy onnx models into `voices/src/main/assets/`
2. Rename the encoder and decoder model files according to voice map located in `app/src/main/java/com/chimege/tts/Config.java`
```java
public static Map<String, Pair<String, String>> voices = new HashMap<String, Pair<String, String>>() {
    {
        put("[Name of the voice]", new Pair<>("[encoder model file name without extension]", "[decoder model file name without extension]"));
        put(... etc
    }
};
```
3. Build or publish the app using Android Studio
