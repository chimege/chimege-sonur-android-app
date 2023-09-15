import re
import pandas as pd
from os.path import join, dirname


def read_db(path, conjugations):
    conj = {}
    for _, row in pd.read_csv(conjugations).iterrows():
        if row["last_word"].lower() not in conj:
            conj[row["last_word"].lower()] = []
        conj[row["last_word"].lower()].append({
            "word": row["conjugated"].lower(),
            "suffix": row["suffix"]
        })
    lines = open(path, 'r', encoding="utf-8").readlines()
    abbreviations = []
    for line in lines:
        line = line.strip().split("|")
        if len(line) == 2:
            key = line[1].strip().split()
            if len(key[:-1]) == 0:
                continue
            abbreviations.append({
                "key": " ".join(key[:-1]).lower(),
                "abbrv": line[0].strip(),
                "conjugations": conj.get(key[-1].lower().strip(), []) + [{"word": key[-1].lower(), "suffix": ""}]
            })
    abbreviations.sort(key=lambda x: -len(x["key"]))
    return abbreviations


DB = read_db(
    join(dirname(__file__), "mongolian_abbreviations.csv"),
    join(dirname(__file__), "conj_abb.csv")
)


def abbrieviate(text):
    for e in DB:
        if e["key"] in text.lower():
            prev_start = None
            tmp = ""
            matches = list(re.finditer(f"{e['key']} ", text.lower()))
            matches.reverse()
            for m in matches:
                found = None
                si = m.end()
                for conj in e["conjugations"]:
                    if text[si:].lower().startswith(conj["word"]):
                        target_word = re.split(r"[^а-яөүё]", text[si:].lower())[0]
                        found = conj["suffix"] + target_word[len(conj["word"]):]
                        si += len(target_word)
                        break
                if found is None:
                    part = m.group()
                elif len(found) > 0:
                    part = e["abbrv"] + "-" + found
                else:
                    part = e["abbrv"]
                tmp = part + text[si:prev_start] + tmp
                prev_start = m.start()
            tmp = text[0:prev_start] + tmp
            text = tmp
    return text
