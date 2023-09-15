from os.path import join, dirname

import yaml
import json
import time
import unittest

from tts_normalizer import normalize_tts_text, init_normalizers

config = yaml.safe_load(open(join(dirname(__file__), "../config.yaml"), encoding="utf-8"))
init_normalizers(config["runtime_config"]["initial_config"])
default_options = config["runtime_config"]["default_options"]

def fill_defaults(options):
    if options.keys() != default_options.keys():
        for k, v in default_options.items():
            if k not in options:
                options[k] = v
    return options


class TestTTSNormalization(unittest.TestCase):

    def test_tts_normalizations(self):
        with open(join(dirname(__file__), 'tts_tests.json'), encoding="utf-8") as f:
            tests = json.load(f)
            d = {}
            for text, target_text in tests:
                start_time = time.time()
                if type(text) == str:
                    normalized_text = normalize_tts_text(
                        dict({"text": text}, **default_options))
                elif type(text) == dict:
                    text = fill_defaults(text)
                    normalized_text = normalize_tts_text(text)
                else:
                    raise TypeError("Input should be str or dict")
                d[" ".join(normalized_text).lower()] = ""
                end_time = time.time()

                if not config["debug_test"]:
                    self.assertEqual(normalized_text, target_text)
                    self.assertLess(end_time - start_time, 0.9, target_text)
                else:
                    try:
                        self.assertEqual(normalized_text, target_text)
                        print(f"✅ time: {(end_time - start_time):.6f} {normalized_text}")
                    except AssertionError:
                        print(
                            f"❌ Result {json.dumps(normalized_text, ensure_ascii=False)}\n❌ Target {json.dumps(target_text, ensure_ascii=False)}")
            # json.dump(d, open("tts_out1.json", "w"), ensure_ascii=False)


if __name__ == '__main__':
    unittest.main()
