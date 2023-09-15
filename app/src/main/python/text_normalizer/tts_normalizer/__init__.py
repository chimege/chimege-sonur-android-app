import json
import sys
from os.path import join, dirname
import re

TTS_NORMALIZER_PATH = dirname(__file__)
CONJUGATOR_PATH = join(TTS_NORMALIZER_PATH, 'conjugator')
sys.path.append(CONJUGATOR_PATH)

from conjugator.conjugator import Conjugator
from .sentence_splitter import SentenceSplitter
from .abbreviations import Abbreviations
from .numeric_normalizer import NumericNormalizer
from .preprocessor import PreProcessor
from .postprocessor import PostProcessor
from .emoji_replacer import EmojiReplacer
try:
    from .phoneme_translator import Phonemizer
except ModuleNotFoundError:
    from .phoneme_translator_non_espeak import Phonemizer

tts_normalizers = []


def init_normalizers(config):
    conjugator_json_file = join(CONJUGATOR_PATH, 'json', config['noun_conj'])
    symbols_file = json.load(open(join(TTS_NORMALIZER_PATH, config["symbols_file"]), encoding="utf-8"))
    conjugator = Conjugator(conjugator_json_file)

    emo_replacer = EmojiReplacer(name="emoji_replacer", emojis_json=join(TTS_NORMALIZER_PATH, config["emoji_list"]))
    prep = PreProcessor(name="preprocessor")
    phonemizer = Phonemizer(name="phonemizer_lite")
    abbreviation = Abbreviations(name="abbreviation",
                                 abbreviation_file=join(TTS_NORMALIZER_PATH, config["abbreviation_file"]),
                                 conjugator=conjugator)
    numeric = NumericNormalizer(name="numeric",
                                conjugator=conjugator)
    postp = PostProcessor("postprocessor", symbols_file)
    sentence_normalizer = SentenceSplitter("sentence_splitter", config, symbols_file, conjugator)
    global tts_normalizers
    tts_normalizers = [
        emo_replacer,
        phonemizer,
        prep,
        abbreviation,
        numeric,
        postp,
        sentence_normalizer,
    ]


def normalize_tts_text(input_text):
    for normalizer in tts_normalizers:
        input_text = normalizer(input_text)
    return input_text


EMERGENCY_MAP = {
    "0": "тэг", "1": "нэг", "2": "хоёр", "3": "гурав", "4": "дөрөв",
    "5": "тав", "6": "зургаа", "7": "долоо", "8": "найм", "9": "ес",
    'Q': 'кюү', 'W': 'дабэлюү', 'E': 'ий', 'R': 'оар', 'T': 'тий',
    'Y': 'вая', 'U': 'юү', 'I': 'ая', 'O': 'оөү', 'P': 'пий', 'A': 'эй',
    'S': 'эйс', 'D': 'дий', 'F': 'эйф', 'G': 'жий', 'H': 'эйч', 'J': 'жэй',
    'K': 'кэй', 'L': 'эйл', 'Z': 'сий', 'X': 'эйкс', 'C': 'сий', 'V': 'вий',
    'B': 'бий', 'N': 'эйн', 'M': 'эйм'
}


def tts_emergency(input_text):
    text = input_text.lower()
    for c, r in EMERGENCY_MAP.items():
        text = text.replace(c.lower(), " " + r + " ")
    text = re.sub(r"[^А-Яа-яЁёҮүӨө\-\.,\!\?:\"']", " ", text)
    text = re.sub(r"[ ]+", " ", text)
    return [text[i:i+300] for i in range(0, len(text), 300)]
