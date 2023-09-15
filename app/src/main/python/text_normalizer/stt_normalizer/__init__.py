from .number_normalizer import handle_numbers
from .abbreviate import abbrieviate
from .regex_normalizer import regex_fix
import re


def normalize_stt_text(text):
    text = text.lower()
    text = abbrieviate(text)
    text = handle_numbers(text)
    text = regex_fix(text)
    return text


NUM_OPTIONS = {
    "0": ["нойл", "тэг"],
    "1": ["нэг", "зуу", "мянга", "тэрбум", "сая", "ар"],
    "2": ["х"],
    "3": ["г"],
    "4": ["д"],
    "5": ["та"],
    "6": ["зур", "ж"],
    "7": ["д"],
    "8": ["на"],
    "9": ["е"],
}


def barefy(text):
    ch = text[0]
    if ch in "0123456789":
        return NUM_OPTIONS[ch]
    if len(text) > 2 and text[:2].upper() == text[:2]:
        return [ch.lower()]
    text = re.sub(r"[\.,?]", "", text.lower())
    return [text[0]]


def exist(bares, txt):
    for bare in bares:
        if bare in txt:
            return True
    return False


def starts(bares, txt):
    for bare in bares:
        if txt.startswith(bare):
            return True
    return False


def offset_matcher(normalized, raw, offsets):
    offsets = [int(o) for o in offsets.split(" ")]
    s_idx = 0
    matches = []
    words = normalized.split()
    prev = words[0]
    for word in words[1:]:
        bares = barefy(word)
        e_idx = s_idx + len(raw[s_idx:].strip().split(" ")[0]) + 1
        if not exist(bares, raw[e_idx:].strip()):
            print("FAILED", bares, word)
            raise ValueError
        while not starts(bares, raw[e_idx:].strip()):
            if " " in raw[e_idx:].strip():
                e_idx += raw[e_idx:].strip().index(" ")
            else:
                e_idx = -1
                break
        matches.append([
            prev,
            raw[s_idx:e_idx]
        ])
        s_idx = e_idx
        prev = word
    matches.append([
        prev,
        raw[s_idx:]
    ])
    s_idx = 0
    result = []
    for w, r in matches:
        result.append({"text": w + " ", "startAt": offsets[s_idx],
                       "isStopWord": False, "isHighlighted": False})
        s_idx += len(r)
    return result
