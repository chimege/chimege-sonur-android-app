import time
from stt_normalizer import normalize_stt_text

with open("misc/stt_use_cases.txt", encoding="utf-8") as f:
    texts = f.read().split("\n")

for text in texts:
    if len(text.strip()) == 0:
        continue
    s = time.time()
    text = normalize_stt_text(text)
    print("result:", text)
    print("Done case in", time.time() - s)
    print("*"*69)
