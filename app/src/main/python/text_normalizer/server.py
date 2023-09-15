import re
from flask import Flask, request
from waitress import serve
import time
import yaml
from tts_normalizer import normalize_tts_text, init_normalizers, tts_emergency
from stt_normalizer import normalize_stt_text
from Bio import pairwise2
from Bio.pairwise2 import format_alignment


from logger import init_logger
import traceback

import os

os.environ["PATH"] += os.pathsep + os.path.dirname(__file__)

app = Flask(__name__)

config = yaml.safe_load(open("config.yaml", encoding="utf-8"))
init_normalizers(config["runtime_config"]["initial_config"])
API = config["api_key"]

default_options = config["runtime_config"]["default_options"]

# tts_logger = init_logger(config["loggers"]["tts_logger"])
# stt_logger = init_logger(config["loggers"]["stt_logger"])


def process_tts(input_text):
    normalized_text = normalize_tts_text(input_text)
    return normalized_text


def process_stt(text):
    normalized_text = normalize_stt_text(text)
    return normalized_text


def fill_defaults(options):
    if options.keys() != default_options.keys():
        for k, v in default_options.items():
            if k not in options:
                options[k] = v
    return options


@app.route("/tts_normalize", methods=["POST"])
def tts_normalize():
    if request.headers.get('Key') == API:
        s = time.time()
        input_seq = request.json["data"]
        try:
            options = request.json.get("options", config["runtime_config"][
                "default_options"])  # split_sentences, abbreviation_level, read_symbols, use_phonemizer, read_emojis, dont_read_number_n
            options = fill_defaults(options)
            normalized = process_tts(dict({"text": input_seq}, **options))
            print("Processed in:", time.time() - s, "\t", input_seq[:50], "\t=>\t", normalized[0][:50])
            # tts_logger.info("Processed", extra={"process_input": input_seq, "process_output": str(normalized),
            #                                     "time": time.time() - s})
            return {"normalized": normalized}
        except Exception as e:
            print("Normalizer exception:", e)
            # tts_logger.error("Failed", extra={"process_input": input_seq, "process_output": str(traceback.format_exc()),
            #                                   "time": time.time() - s})
            return {"normalized": tts_emergency(input_seq)}
    else:
        return "Invalid API"


@app.route("/stt_normalize", methods=["POST"])
def stt_normalize():
    if request.headers.get('Key') == API:
        s = time.time()
        input_seq = request.json["data"]
        normalized = process_stt(input_seq)
        print("Processed in:", time.time() - s)
        return {"normalized": normalized}
    else:
        return "Invalid API"


@app.route("/normalizer_pipeline", methods=["POST"])
def normalizer_pipeline():
    if request.headers.get('Key') == API:
        s = time.time()
        input_seq = request.json["data"].replace("\n", "")
        result = {}
        try:
            print("Input            :", input_seq[:80])
            options = request.json.get("tts_options", config["runtime_config"][
                "default_options"])  # split_sentences, abbreviation_level, read_symbols, use_phonemizer, read_emojis, dont_read_number_n
            options = fill_defaults(options)
            normalized = process_tts(dict({"text": input_seq}, **options))
            print("TTS normalized in:", time.time() - s, "\t", normalized[0][:80])
            result["tts"] = normalized

            use_stt = request.json.get("use_stt", False)
            if use_stt:
                # input_seq = re.sub(r"[^-_.,!?:\"' \-А-ЯӨҮЁа-яөүёA-Za-z0-9]", r"", input_seq)
                normalized = process_stt(" ".join(normalized))
                result["stt"] = normalized
                print("STT normalized in:", time.time() - s, "\t", normalized[:80])
                print(f"TTS, STT IO match: {normalized == input_seq}")
                # if normalized.lower() != input_seq.lower():
                alignments = pairwise2.align.globalxx(list(input_seq.lower()), list(normalized.lower()), gap_char=['x'])
                formatted_alignment = format_alignment(*alignments[0]).split("\n")
                score = (int(formatted_alignment[3].split("=")[1]) - formatted_alignment[0].count("x")) / len(input_seq)
                diff_str = "\n".join(format_alignment(*alignments[0]).split("\n")[:3])
                result["diff"] = diff_str
                print("Difference:")
                print(diff_str)
                print(f"Score", score)
            return {"normalized": result}
        except Exception as e:
            print(e)
    else:
        return "Invalid API"


print(f'Started Server on {config["host"]}:{config["port"]}')
serve(app, host=config["host"], port=config["port"], threads=config["thread"])
