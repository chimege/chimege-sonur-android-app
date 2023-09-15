from .detection import *

def pad_vowel(word, suffix):
    d_vowel = detect_pad_vowel(word)
    return word + d_vowel + suffix

def check_is_foreign(word, conj_operation):
    is_foreign = False
    if conj_operation == "conj_foreign_word":
        is_foreign = True

    return is_foreign

def pad_y_vowels(word, suffix):
    if detect_word_gender(word) == "feminine":
        hard_soft_sign = "ь"
    else:
        hard_soft_sign = "ъ"
    return word + hard_soft_sign + suffix


def to_imperative(word, consonants, vowels):
    if count_syllables(word) > 1 and word[-1] == "х":
        word = word[:-1]
        # urt ni 2,3+ bh iig shalgah?
        if word[-1] in vowels and word[-2] in consonants:
            if not (word[-2] in ["л", "г"] and word[-3] in consonants):
                word = word[:-1]
    return word


def generate_code_string(word, categories, is_foreign, word_lists):
    vocalized = categories["consonants"]["vocalized"]
    non_vocalized = categories["consonants"]["nonvocalized"]
    d_vowel = detect_dominating_vowel(word, categories, is_foreign, word_lists)
    if word[-1] in vocalized:
        endswith = "vocalized_consonant"
    elif word[-1] in non_vocalized:
        endswith = "non_vocalized_consonant"
    else:
        endswith = "vowel"
    return f'endswith={endswith}&{d_vowel}_dominated', endswith
