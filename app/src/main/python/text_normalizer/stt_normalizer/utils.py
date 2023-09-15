import random
import string
import copy
from .definitions import *

# utility variables for converting words to numbers
digits = {
    'тэг': (0, False),
    'ноль': (0, False),
    'нойл': (0, False),
    'нэг': (1, True),
    'нэгэн': (1, False),
    'хоёр': (2, True),
    "хоёрон": (2, True),
    'гурав': (3, False),
    'гурван': (3, True),
    'дөрөв': (4, False),
    'дөрвөн': (4, True),
    'тав': (5, False),
    'таван': (5, True),
    'зургаа': (6, False),
    'зургаан': (6, True),
    'долоо': (7, False),
    'долоон': (7, True),
    'найм': (8, False),
    'найман': (8, True),
    'ес': (9, False),
    'есөн': (9, True),
}
decimals = {
    'арав': (10, False),
    'арван': (10, True),
    'хорь': (20, False),
    'хорин': (20, True),
    'гуч': (30, False),
    'гучин': (30, True),
    'дөч': (40, False),
    'дөчин': (40, True),
    'тавь': (50, False),
    'тави': (50, True),
    'тавин': (50, True),
    'жар': (60, False),
    'жаран': (60, True),
    'дал': (70, False),
    'далан': (70, True),
    'ная': (80, False),
    'наян': (80, True),
    'ер': (90, False),
    'ерэн': (90, True),
    'ерөн': (90, True)
}
multiplier = {
    'мянга': (1000, True),
    'мянган': (1000, True),
    'сая': (1000000, True),
    'тэрбум': (1000000000, True)
}
centier = {
    'зуу': (100, False),
    'зууг': (100, False),
    'зуун': (100, True)
}
number_suffixes = {
    "ний": "ний", "ны": "ны", "ын": "ын", "гийн": "гийн", "ийг": "ийг", "ийн": "ийн", "ыг": "ыг", "онд": "нд",
    "нд": "нд", "д": "д", "ид": "д",
    "аас": "аас", "наас": "наас", "нээс": "нээс", "ээс": "ээс", "ас": "аас", "ос": "оос", "ноос": "ноос", "оос": "оос",
    "өөс": "өөс", "нөөс": "нөөс", "наар": "наар", "аар": "аар", "нээр": "нээр", "ээр": "ээр", "нөөр": "нөөр",
    "өөр": "өөр", "ноор": "ноор", "оор": "оор", "г": "г", "т": "т",
    "тай": "тай", "тэй": "тэй", "той": "той", "рүү": "рүү", "руу": "руу", "уул": "уул", "ул": "уул", "үүл": "үүл",
    "даа": "даа", "уулаа": "уулаа", "үүлээ": "үүлээ", "улаа": "уулаа", "дугаар": "дугаар", "дүгээр": "дүгээр",
    "дугаарт": "дугаарт", "дүгээрт": "дүгээрт", "тэйгээ": "тэйгээ", "тайгаа": "тайгаа", "аараа": "аараа",
    "ээрээ": "ээрээ", "оороо": "оороо", "гаас": "аас", "гаар": "гаар", "гоос": "гоос", "гоор": "гоор", "өөд": "өөд", "аад": "аад",
    "ээд": "ээд", "хан": "хан", "хэн": "хэн", "хон": "хон", "хөн": "хөн"
}
numbers = [
    ("нолий", "ноль"), ("ноль", "ноль"), ("нойл", "нойл"), ("тэг", "тэг"), ("нэгэ", "нэг"), ("нэг", "нэг"),
    ("хоёр", "хоёр"), ("хоёрон", "хоёр"), ("хоёро", "хоёр"), ("хоё", "хоёр"),
    ("гурав", "гурав"), ("гурва", "гурав"), ("гурв", "гурав"), ("дөрөв", "дөрөв"), ("дөрвө", "дөрөв"),
    ("дөрв", "дөрөв"), ("тави", "тавь"), ("тава", "тав"), ("тав", "тав"), ("зургаа", "зургаа"), ("зург", "зургаа"),
    ("дол", "долоо"), ("долоо", "долоо"), ("долоон", "долоо"), ("найм", "найм"), ("найма", "найм"), ("ес", "ес"),
    ("есө", "ес"), ("арав", "арав"), ("арва", "арав"), ("арв", "арав"), ("хори", "хорин"), ("хорь", "хорь"),
    ("гучи", "гучин"), ("гуч", "гуч"), ("дөчи", "дөч"), ("дөч", "дөч"), ("тавь", "тавь"), ("жара", "жар"), ("жар", "жар"),
    ("дала", "дал"), ("дал", "дал"), ("ная", "ная"), ("ер", "ер"), ("зуу", "зуу"), ("мянга", "мянга"),
    ("мянг", "мянга"), ("сая", "сая"), ("тэрбум", "тэрбум")]


def suffix_separator(text):
    words = text.split(" ")
    result = ""
    rep = {}
    for word in words:
        selected = False
        for root, repl in numbers:
            if word.startswith(root):
                suffix = word[len(root):]
                if suffix in number_suffixes:
                    result += f" {repl} -{number_suffixes[suffix]}"
                    rep[f" {repl} -{number_suffixes[suffix]} "] = word
                    # rep["тави ас"] = тавиас
                    selected = True
                    break
        if not selected:
            result += " " + word

    for c in manual_suffix_fix:
        result = result.replace(c[0], c[1])
    return result.strip(), rep


def generate_encoding(encodings):
    generated = "".join(random.choices(string.ascii_letters, k=8))
    if generated not in encodings:
        return generated
    else:
        return generate_encoding(encodings)

def inject_one_before_lone_multiplier(text):
    text = re.sub(slip_one_before_lone_multipliers, r"нэг \1", text)
    return text

def strip_match(match, group_n):
    text, start, end = match.group(group_n), match.start(group_n), match.end(group_n)
    n_spaces_at_start = len(re.search(r"^([ ]*)", text).group())
    n_spaces_at_end = len(re.search(r"([ ]*)$", text).group())
    start = start + n_spaces_at_start
    end = end - n_spaces_at_end
    return text.strip(), start, end


def encode_special_cases(text, defined_cases):
    encoding = {}
    cases = copy.deepcopy(defined_cases)
    for i, case in enumerate(cases):
        case_matches = list(re.finditer(case[0], text))
        for m in case_matches[::-1]:
            group = case[1]
            if isinstance(group, int):
                group = [group]
            if group == [9999]:  # for нэг
                if m[2] is not None and all(
                        True if not m[2].startswith(n) else False for n in everything.split("|") + special_stoppers.split("|")):
                    group = [3]
                elif m[2] is None:
                    group = [3]
                else:
                    group = []
                    continue
            for g in group[::-1]:
                uid = generate_encoding(encoding)
                mgroup, mstart, mend = strip_match(m, g)
                if mgroup:
                    text = text[:mstart] + uid + text[mend:]
                    encoding[uid] = mgroup
    return text, encoding


def decode_special_cases(text, global_encodings):
    for local_enc in global_encodings:
        for uid, repl in local_enc.items():
            text = re.sub(rf"\b{uid}\b", repl, text)
    return text


def manual_fixer(text):
    # region format law zuil zaalts
    zuil_matches = list(re.finditer(fr"(([0-9]+)(-ын|-ийн|-гийн)[ ]+)+([0-9]+)\b(-(ан|өн|он|эн)|)", text))
    for m in zuil_matches[::-1]:
        new_zuil = re.sub(r"(-ын|-ийн|-гийн)[ ]+", ".", m.group(0))
        new_zuil_split = new_zuil.split(".")
        if m[5] != "" and len(new_zuil_split) == 2 and new_zuil_split[0] == new_zuil_split[1].split("-")[0]:
            continue
        text = text[:m.start()] + new_zuil + text[m.end():]
    # endregion

    text = re.sub(r"([0-9])-(ан|өн|он|эн)", r"\1", text)

    text = re.sub(r"([а-я]+)-([а-я]+)", r"\1 \2", text.strip().replace("  ", " "))

    # region abbreviate metrics
    for keyword, replacement in number_tailers:
        matches = list(re.finditer(rf"([0-9]+|мянга|мянган|зуу|зуун|сая|тэрбум)([ ]*({keyword})([^ ]*))", text))
        for m in matches[::-1]:
            if m.group(4).strip() != "":
                replacement += "-" + m.group(4)
            if not re.search(r"[0-9]", m.group(1)):
                replacement = " " + replacement
            text = text[:m.start(2)] + replacement + text[m.end(2):]
    # endregion

    for keyword, replacement in percentage:
        text = re.sub(rf"([0-9]+)[ ]*{keyword}(\b|$)", rf"\1{replacement}", text)

    text = re.sub(r"(хасах[ ]+)([0-9])", r"-\2", text)

    # region format time
    for case in time_catchers:
        matches = list(re.finditer(case[0], text))
        for m in matches[::-1]:
            hour = m.group(case[1][0])
            minute = m.group(case[1][1])
            if len(minute) == 1:
                minute = "0" + minute
            text = text[:m.start(case[1][0])] + hour + ":" + minute + text[m.end(case[1][1]):]
    # endregion

    # 1-дүгээр 2-дугаарт ==> 1 дүгээр 2 дугаарт
    text = re.sub(r"([0-9])-(дүгээр|дугаар)", r"\1 \2", text)

    # region format date
    year_enumeration = list(re.finditer(r"([21][0-9]{3})[ ]+([0-9]{1,2})([-][а-яөүё]+|)[ ]+(он[а-яөүё]*)\b", text))
    for m in year_enumeration[::-1]:
        first_year = m[1]
        second_year = m[2]
        second_year_base = first_year[:len(first_year) - len(second_year)] + "0" * len(second_year)
        new_year = int(second_year_base) + int(second_year)
        text = text[:m.start(1)] + first_year + ", " + str(new_year) + text[m.end(2):]
    # endregion
    return text
