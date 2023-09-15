import re

regexes = []

regexes += [
    (
        r"\b[а-яёөү] [а-яёөү] [0-9]{8}\b",
        lambda m: m.group().replace(" ", "").upper()
    )
]


def regex_fix(text):
    for reg, fix in regexes:
        text = re.sub(reg, fix, text)
    return text
