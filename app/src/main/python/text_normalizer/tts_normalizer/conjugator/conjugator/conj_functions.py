from .utils import *


def conj_long_vowel_ending(word, suffix, categories):
    vowels = categories["vowels"]["all"]
    if suffix.startswith(tuple(vowels)):
        conjugated = word + "г" + suffix
    else:
        conjugated = word + suffix
    return conjugated


def conj_vowel_ending(word, suffix, categories):
    long_vowels = categories["vowels"]["long"] + ["ий"]
    gliding_vowels = categories["vowels"]["gliding"]
    y_vowels = categories["vowels"]["y_vowels"]
    consonants = categories["consonants"]["all"]
    if word.endswith(tuple(y_vowels)) and suffix.startswith(tuple(long_vowels)):
        if suffix.startswith("ий"):
            conjugated = word + suffix
        else:
            conjugated = word + suffix[1:]
    elif word.endswith(tuple(long_vowels + gliding_vowels)) and suffix.startswith(tuple(long_vowels)):
        conjugated = word + "г" + suffix
    elif len(word) > 1 and word[-2] in consonants and suffix.startswith(tuple(long_vowels)) or suffix.startswith(tuple(gliding_vowels)):
        if suffix[0] == "ы" or suffix[:2] == "ий":
            conjugated = word[:-1] + suffix
        else:
            conjugated = word + suffix[1:]
    else:
        conjugated = word + suffix
    return conjugated


def conj_vocalized_ending(word, suffix, categories):
    # 1 useg,ЭГ baival egshig jiireglene;
    # ЗГ baval shuud;
    # “х” useg, zuulruugu egshigt giiguulegch bvl egshig jiiireglene;
    # ye yu ya zalgahdaa hatuu zuulnii temdeg bichne
    conjugated = ""
    consonants = categories["consonants"]["all"]
    vocalized = categories["consonants"]["vocalized"]
    non_vocalized = categories["consonants"]["nonvocalized"]
    vowels = categories["vowels"]["all"] + ["ы"]
    y_vowels = categories["vowels"]["y_vowels"]

    non_vocalized_str = "".join(non_vocalized)
    vowels_str = "".join(vowels)
    l_r_ending = False
    hassan = word[:-2] + word[-1]
    if len(re.findall(f"([{non_vocalized_str}][{vowels_str}])(л|р)$", word)) > 0:
        l_r_ending = True

    if l_r_ending and suffix.startswith(tuple(vowels)):
        if len(word) > 3:
            conjugated = hassan + suffix
        else:
            conjugated = word + suffix
    elif suffix.startswith(tuple(vocalized)):
        if len(suffix) == 1:
            if l_r_ending:
                conjugated = pad_vowel(hassan, suffix)
            else:
                conjugated = pad_vowel(word, suffix)
            # conjugated = pad_vowel(word, suffix)
        elif suffix[0] in vocalized and suffix[1] in consonants:
            if l_r_ending:
                conjugated = pad_vowel(hassan, suffix)
            else:
                conjugated = pad_vowel(word, suffix)
        else:
            conjugated = word + suffix

    elif suffix.startswith(tuple(non_vocalized)):
        if suffix.startswith("х"):
            if l_r_ending:
                conjugated = pad_vowel(hassan, suffix)
            else:
                conjugated = pad_vowel(word, suffix)
        else:
            conjugated = word + suffix
    elif suffix in y_vowels:
        conjugated = pad_y_vowels(word, suffix)
    elif suffix.startswith(tuple(vowels)):
        if len(word) > 3 and word[-2] in vowels and  word[-2] != "и":
            if word[-3] in vocalized and word[-3:-2] not in ["га", "го", "гу", "гы"]:#!= "г":
                if len(word) < 4 or word[-4] not in vowels + y_vowels + ["й"]:
                    conjugated = word + suffix
                else:
                    conjugated = hassan + suffix
            elif word[-3] in non_vocalized:  # and word[-4] in vowels:
                if word[-2] != "и" and word[-3] not in ["ж", "ч", "ш"]:
                    conjugated = hassan + suffix
                else:
                    conjugated = word + suffix
            else:
                conjugated = word + suffix
        else:
            conjugated = word + suffix
    else:
        conjugated = word + suffix
    return conjugated


def conj_vocalized_l_r_ending(word, suffix, categories):
    conjugated = ""
    consonants = categories["consonants"]["all"]
    vocalized = categories["consonants"]["vocalized"]
    non_vocalized = categories["consonants"]["nonvocalized"]
    y_vowels = categories["vowels"]["y_vowels"]
    if suffix.startswith(tuple(vocalized)):
        if len(suffix) == 1:
            conjugated = pad_vowel(word, suffix)
        elif suffix.startswith(tuple(vocalized)) and suffix[1] in consonants:
            conjugated = pad_vowel(word[:-2] + word[-1], suffix)
        else:
            conjugated = word + suffix
    elif suffix.startswith(tuple(non_vocalized)):
        if suffix.startswith("х"):
            conjugated = pad_vowel(word[:-2] + word[-1], suffix)
        else:
            conjugated = word + suffix
    elif suffix in y_vowels:
        conjugated = pad_y_vowels(word, suffix)
    else:
        conjugated = word + suffix
    return conjugated


def conj_non_vocalized_ending(word, suffix, categories):
    # zuulruugu egshig giiguulegch bvl egshig jiireglene;
    # х usgeer ehelsen bvl egshig jiireglene;
    # ye yu ya zalgahdaa hatuu zuulnii temdeg bichne
    conjugated = ""
    consonants = categories["consonants"]["all"]
    vocalized = categories["consonants"]["vocalized"]
    non_vocalized = categories["consonants"]["nonvocalized"]
    vowels = categories["vowels"]["all"]
    y_vowels = categories["vowels"]["y_vowels"]
    if suffix.startswith(tuple(vocalized)):
        if len(suffix) == 1:
            conjugated = pad_vowel(word, suffix)
        elif suffix.startswith(tuple(vocalized)) and suffix[1] in consonants:
            conjugated = pad_vowel(word, suffix)
        else:
            conjugated = word + suffix
    elif suffix.startswith(tuple(non_vocalized)):
        if suffix.startswith("х") or len(suffix) == 1:
            conjugated = pad_vowel(word, suffix)
        else:
            conjugated = word + suffix
    elif suffix in y_vowels:
        conjugated = pad_y_vowels(word, suffix)
    elif suffix.startswith(tuple(vowels)):
        if len(word) > 3 and word[-2] in vowels:
            if word[-3] in consonants:
                conjugated = word[:-2] + word[-1] + suffix
        else:
            conjugated = word + suffix
    else:
        conjugated = word + suffix
    return conjugated


def conj_soft_sign_ending(word, suffix, categories):
    # neg ug deer uur ug zalgaj bvl zuulnii temdeg ni и bolohgui
    vocalized = categories["consonants"]["vocalized"]
    non_vocalized = categories["consonants"]["nonvocalized"]
    vowels = categories["vowels"]["all"]
    if suffix.startswith(tuple(vocalized)) or suffix.startswith("х"):
        if suffix == "гүй":
            conjugated = word + suffix
        else:
            conjugated = word[:-1] + "и" + suffix
    elif suffix.startswith(tuple(vowels)):
        conjugated = word[:-1] + "и" + suffix[1:]
    elif word[-2] in non_vocalized and suffix.startswith(tuple(non_vocalized)):
        conjugated = word[:-1] + "и" + suffix
    else:
        conjugated = word + suffix
    return conjugated


def conj_non_vocalized_d_ending(word, suffix, categories):
    # ЗГ eer ehelsen suffix baival balarhai egshig geegdene, egshig jiireglehgu;
    # zuulruugu ЭГ bvl egshig jiireglene, balarhai egshig geegdene,
    # egshigeeer ehelsen bvl balarhai egshig bas geegdene
    consonants = categories["consonants"]["all"]
    non_vocalized = categories["consonants"]["nonvocalized"]
    vowels = categories["vowels"]["all"]
    if len(suffix) == 1:
        conjugated = word[:-2] + word[-1] + detect_pad_vowel(word) + suffix
    else:
        if suffix.startswith("х") or suffix[1] in consonants:
            conjugated = word[:-2] + word[-1] + detect_pad_vowel(word) + suffix
        elif suffix.startswith(tuple(consonants)) and suffix[1] in vowels:
            conjugated = word + suffix
        elif suffix.startswith(tuple(vowels)):
            if len(word) > 3:
                conjugated = word[:-2] + word[-1] + suffix
            else:
                conjugated = word + suffix
        else:
            conjugated = word + suffix

    return conjugated


def conj_foreign_word(word, suffix, categories, word_lists):
    conjugated = ""
    vowels = categories["vowels"]["all"]
    long_vowels = categories["vowels"]["long"] + ["ий"]
    gliding_vowels = categories["vowels"]["gliding"]
    consonants = categories["consonants"]["all"]

    last_syllable = get_last_syllable(word, categories)
    vowels_without_duplicate = list(set(re.findall('[аэиоөуүяеёю]', last_syllable)))
    if "а" in vowels_without_duplicate or "о" in vowels_without_duplicate:
        if suffix[:2] == "ий":
            suffix = "ы"+ suffix[2:]

    if word.endswith(tuple(long_vowels + gliding_vowels)) and suffix.startswith(tuple(long_vowels)):
        if suffix[0] == "ы":
            suffix = "ий"+ suffix[2:]
        conjugated = word + "г" + suffix
    elif word[-2] in consonants and word.endswith(tuple(vowels)) and suffix.startswith(tuple(long_vowels + gliding_vowels)):
        if word[-1] == "и":
            if suffix[0] == "ы" or suffix[:2] == "ий":
                conjugated = word[:-1] + suffix
            else:
                conjugated = word + suffix[1:]
        else:
            if suffix[0] == "ы":
                suffix = "ий"+ suffix[1:]
            conjugated = word+"г"+suffix
    elif word.endswith(tuple(consonants)) and suffix == "д":
        dom_vowel = detect_dominating_vowel(word, categories, word_lists, True)
        if dom_vowel == "e":
            pad = "э"
        elif dom_vowel == "u":
            pad = "ө"
        if dom_vowel == "o":
            pad = "о"
        if dom_vowel == "a":
            pad = "а"

        conjugated = word + pad + suffix
    else:
        conjugated = word + suffix
    return conjugated
