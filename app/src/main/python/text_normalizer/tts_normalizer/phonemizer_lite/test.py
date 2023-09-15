from espeak import EspeakBackend

espeak = EspeakBackend("en-us")

phonemized = espeak.phonemize(["hi", "what", "is","up"])
print(phonemized)
