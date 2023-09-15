import re
import json

from .utils import *
from .conj_functions import *


class Conjugator:
    def __init__(self, json_file) -> None:
        with open(json_file, encoding="utf-8") as f:
            f = json.load(f)
        self.conjugations = f["conjugations"]
        self.categories = f["categories"]
        self.word_lists = f["word_lists"]
        

    def determine_conj_operation(self, word):
        vowels_str = "".join(self.categories["vowels"]["all"])
        vocalized_str = "".join(self.categories["consonants"]["vocalized"])
        non_vocalized_str = "".join(self.categories["consonants"]["nonvocalized"])
        foreign_letters_str = "".join(self.categories["consonants"]["foreign"])
        all_vowels_str = "".join(self.categories["vowels"]["all"] + self.categories["vowels"]["y_vowels"])
        if len(re.findall(f"[{foreign_letters_str}]", word)) > 0 or word in self.word_lists["foreign_words"]:
            return "conj_foreign_word"

        elif len(re.findall(f"[{all_vowels_str}]$", word)) > 0:
            return "conj_vowel_ending"  # 1

        # vocalized consonant ending
        elif len(re.findall(f"[{vocalized_str}]$", word)) > 0:
            return "conj_vocalized_ending"  # 2

        # non vocalized ending
        elif len(re.findall(f"[{non_vocalized_str}]$", word)) > 0:
            if len(re.findall(f"[{non_vocalized_str}][{vowels_str}][ж|ч|ш|д]$", word)) > 0:
                return "conj_non_vocalized_d_ending"  # 5
            else:
                return "conj_non_vocalized_ending"  # 3

        # hard, soft sign ending
        elif len(re.findall("ь|ъ$", word)) > 0:
            return "conj_soft_sign_ending"  # 4
        else:
            return "conj_foreign_word"
            # raise ("Unrecognized word group")

    def conjugate(self, word, suffix):
        conj_operation = self.determine_conj_operation(word)
        if check_is_foreign(word, conj_operation):
            return eval(f'{conj_operation}(word, suffix, self.categories, self.word_lists)')    
        else:
            return eval(f'{conj_operation}(word, suffix, self.categories)')

    def get_suffixes(self, word, code, is_foreign):
        conjugations = self.conjugations.copy()
        code_str, endswith = generate_code_string(
            word, self.categories, self.word_lists, is_foreign)
        if code_str not in conjugations[code]:
            code_str = code_str.replace(f"endswith={endswith}&", "")
        conjs = conjugations[code][code_str]
        suffixes = conjs['default'].copy()
        if "special" in conjs:
            for sp_obj in conjs["special"]:
                if "replace" in sp_obj.keys():  # and sp_obj["replace"] in suffixes:
                    if provides_condition(word, sp_obj, self.categories, self.word_lists, is_foreign):
                        for suffix_to_replace in sp_obj["replace"]:
                            if suffix_to_replace in suffixes:
                                i = suffixes.index(suffix_to_replace)
                                suffixes[i] = sp_obj["suffix"]
        return suffixes

    def form_conjugations(self, word, code):
        code = code.upper()
        if code[0] == "v":
            word = to_imperative(word, self.categories["consonants"]["all"], self.categories["vowels"]["all"])

        conj_operation = self.determine_conj_operation(word)
        is_foreign = check_is_foreign(word, conj_operation)
        
        suffixes = self.get_suffixes(word, code, is_foreign)
        variations = []
        for suffix in suffixes:
            variations.append(self.conjugate(word, suffix))
        return variations
