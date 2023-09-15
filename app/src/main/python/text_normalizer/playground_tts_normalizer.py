import time
import yaml
from tts_normalizer import normalize_tts_text, init_normalizers

config = yaml.safe_load(open("config.yaml", encoding="utf-8"))
init_normalizers(config["runtime_config"]["initial_config"])

with open("misc/tts_use_cases.txt", encoding="utf-8") as f:
    texts = [s for s in f.read().split("\n") if s != ""]

for text in texts:
    if len(text.strip()) == 0:
        continue
    s = time.time()
    print("input:", text)
    if type(text) == str:
        normalized_text = normalize_tts_text(dict({"text": text}, **config["default_options"]))
    elif type(text) == dict:
        normalized_text = normalize_tts_text(text)
    else:
        raise TypeError("Input should be str or dict")
    print(normalized_text)
    print("Done case in", time.time() - s)
    print("*" * 69)
