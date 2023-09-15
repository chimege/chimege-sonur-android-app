from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from stt_normalizer import normalize_stt_text
import re
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


class TestNormalizationPipeline(unittest.TestCase):

    def test_normalization_pipeline(self):
        with open(join(dirname(__file__), 'pipeline_tests.json'), encoding="utf-8") as f:
            tests = json.load(f)
            accuracy = 0
            for input_seq in tests:
                start_time = time.time()
                normalized = normalize_tts_text(dict({"text": input_seq}, **default_options))
                print("TTS normalized in:", time.time() - start_time, "\t", normalized[0][:80])

                input_seq = re.sub(r"[^-_.,!?:\"' \-А-ЯӨҮЁа-яөүёA-Za-z0-9]", r"", input_seq)
                normalized = normalize_stt_text(" ".join(normalized))
                print("STT normalized in:", time.time() - start_time, "\t", normalized[:80])
                print(f"TTS, STT IO match: {normalized == input_seq}")

                if normalized.lower() != input_seq.lower():
                    alignments = pairwise2.align.globalxx(list(input_seq.lower()), list(normalized.lower()),
                                                          gap_char=['✖'])
                    formatted_alignment = format_alignment(*alignments[0]).split("\n")
                    score = (int(formatted_alignment[3].split("=")[1]) - formatted_alignment[0].count("✖")) / len(
                        input_seq)
                    print("Difference:")
                    print("\n".join(format_alignment(*alignments[0]).split("\n")[:3]))
                    print(f"Score", score)
                    accuracy += score
                else:
                    accuracy += 1
                print()
            print(f"Character accuracy over {len(tests)} cases: {(accuracy / len(tests)):.3f}")

if __name__ == '__main__':
    unittest.main()