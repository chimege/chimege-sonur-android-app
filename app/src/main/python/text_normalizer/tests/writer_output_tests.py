from os.path import join, dirname

import json
import time
import unittest

from stt_normalizer import normalize_stt_text

everything = "нойл|ноль|тэг|нэг|хоёр|гурав|дөрөв|тав|зургаа|долоо|найм|ес|арав|хорь|гуч|дөч|тавь|жар|дал|ная|ер|зуу|мянга|сая|тэрбум|нэг|хоёр|нэгэн|хоёрон|гурван|дөрвөн|таван|зургаан|долоон|найман|есөн|арван|хорин|гучин|дөчин|тавин|жаран|далан|наян|ерөн|ерэн|зуун|мянга|сая|тэрбум"


class TestWriterOutputNormalization(unittest.TestCase):

    def test_stt_normalizations(self):
        with open(join(dirname(__file__), 'writer_output_tests.json'), encoding="utf-8") as f:
            tests = json.load(f)
            begin_t = time.time()
            times = []
            for input_text, target_text in tests.items():
                start_time = time.time()
                normalized_text = normalize_stt_text(input_text)
                end_time = time.time()
                times.append(end_time - start_time)
                self.assertEqual(normalized_text, target_text)

                # try:
                #     self.assertEqual(normalized_text, target_text)
                #     print(f"✅ time: {(end_time - start_time):.6f} | {normalized_text}")
                # except Exception as e:
                #     print(
                #         f"❌ Result {json.dumps(normalized_text, ensure_ascii=False)}\n❌ Target {json.dumps(target_text, ensure_ascii=False)}")
            print(f"Processed {len(tests)} case in {(time.time() - begin_t):.6f}")
            print("avg processing time", sum(times) / len(tests.items()))


if __name__ == '__main__':
    unittest.main()
