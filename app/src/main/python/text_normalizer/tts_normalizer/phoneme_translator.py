import re

from .mongolian_digit_letter import dugaar
from .normalizer_interface import Normalizer
from .phonemizer_lite.espeak import EspeakBackend


class Phonemizer(Normalizer):
    def __init__(self, name):
        super().__init__(name)
        self.backend = EspeakBackend("en-us")
        self.eng_vowels_mono = ["ɪ", "ʊ", "e", "ə", "æ", "ʌ", "ɒ", "ɑ", "i", "a", "u", "ɔ", "j", "o", "ɜ"]
        self.eng_vowels_di = ["ɪə", "eɪ", "ʊə", "ɔɪ", "əʊ", "eə", "aɪ", "aʊ", "iː", "aː", "ɜː", "ɔː", "uː", "ɑː", "oː",
                              "je", "juː", "ja", "jo", "jɪ", "jʊə"]
        self.eng_consonants = ["p", "b", "t", "d", "f", "v", "θ", "ð", "m", "n", "ŋ", "h", "k", "g", "s", "z", "ʃ", "ʒ",
                               "l", "r", "w", "j"]

        self.email_regex = r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*"
        self.domain_regex = r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{0,61}[a-z]"

        self.combi_consonants = ["tʃ", "dʒ"]
        self.chars = [".", ",", "!", "?", ":", " "]
        self.phn_map = {"ð": "д",
                        "ɒ": "о",
                        "ʊ": "өү",
                        "ɔ": "өа",
                        "ɔː": "өо",
                        "ə": "э",
                        "f": "ф",
                        "o": "о",
                        "n": "н",
                        "m": "м",
                        "a": "а",
                        "ɪ": "и",
                        "z": "с",
                        "ɚ": "эр",
                        "ɐ": "ай",
                        "l": "л",
                        "s": "с",
                        "p": "п",
                        "e": "э",
                        "ᵻ": "и",
                        "ʃ": "ш",
                        "ʧ": "ч",
                        "eɪ": "эй",
                        "eə": "эй",
                        "ɑː": "оа",
                        "dʒ": "ж",
                        "ɛ": "эй",
                        "ɹ": "р",
                        "tʃ": "ч",
                        "aʊ": "ау",
                        "əʊ": "өү",
                        "aɪ": "ая",
                        "ɔɪ": "оё",
                        "juː": "юү",
                        "jɪ": "еи",
                        "ɾ": "т",
                        "iː": "ий",
                        "æ": "эай",
                        "ʌ": "а",
                        "b": "б",
                        "t": "т",
                        "d": "д",
                        "v": "в",
                        "θ": "т",
                        "ŋ": "н",
                        "h": "х",
                        "r": "р",
                        "k": "к",
                        "ɡ": "г",
                        "ʒ": "ж",
                        "ʤ": "ж",
                        "y": "я",
                        "w": "в",
                        "u": "ү",
                        "i": "ы",
                        "c": "к",
                        "jo": "ё",
                        "g": "г",
                        "uː": "үү",
                        "ɜː": "иоур",
                        "oː": "ао",
                        "jɑː": "яа",
                        "joː": "ёо",
                        "ʔ": "тт",
                        "jʊə": "еөү",
                        }

    def split_phonemes(self, word):
        char_list = []

        for i, char in enumerate(word):
            if i == 0:
                skip = False
                skip_twice = False
            if skip == True:
                skip = False
                continue
            if skip_twice == True:
                skip_twice = False
                skip = True
                continue
            if char == "j" and i < len(word) - 2:
                if word[i + 2] == "ː":
                    char_list.append(char + word[i + 1] + word[i + 2])
                    skip_twice = True
                elif char + word[i + 1] in self.eng_vowels_di:
                    char_list.append(char + word[i + 1])
                    skip = True
            elif char == "j" and i < len(word) - 3:
                if char + word[i + 1] + word[i + 2] in self.eng_vowels_di:
                    char_list.append(char + word[i + 1] + word[i + 2])
                    skip = True
            elif char in self.eng_vowels_mono and i < len(word) - 1 and char + word[i + 1] in self.eng_vowels_di:
                char_list.append(char + word[i + 1])
                skip = True
            elif char in self.eng_consonants and i < len(word) - 1 and char + word[i + 1] in self.combi_consonants:
                char_list.append(char + word[i + 1])
                skip = True
            else:
                char_list.append(char)
        return char_list

    def latin_phonemes(self, words):
        phns = self.backend.phonemize(words)
        return phns

    def translate_phonemes(self, phonemes):
        cyrill = []
        split_phn = []
        for word in phonemes:
            word = word.replace("ˈ", "")
            split_phn.append(self.split_phonemes(word))
            split_word = self.split_phonemes(word)
            cyr_word = ""
            for phoneme in split_word:
                if phoneme in self.chars:
                    cyr_word += phoneme
                else:
                    if phoneme in self.phn_map:
                        cyr_word += self.phn_map[phoneme]
            cyrill.append(" " + cyr_word + " ")
        return cyrill

    def cyrillize(self, regex, text):
        matches = [x for x in re.finditer(regex, text)]
        if len(matches) == 0:
            return text

        match_words = [word.group() for word in matches]
        words_and_positions = []
        for word in matches:
            words_and_positions.append({"word": word.group(), "start": word.start(), "end": word.end()})

        phn = self.latin_phonemes(match_words)
        cyrill = self.translate_phonemes(phn)
        cyrill = [c.replace(".", " цэг ") for c in cyrill]

        for word, c in zip(matches[::-1], cyrill[::-1]):
            start = word.start()
            end = word.end()
            text = text[:start] + c + text[end:]
        return text

    def roman_conv(self, s, use_dugaar=True):
        roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000, 'IV': 4, 'IX': 9,
                 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
        i = 0
        num = 0
        while i < len(s):
            if i + 1 < len(s) and s[i:i + 2] in roman:
                num += roman[s[i:i + 2]]
                i += 2
            else:
                num += roman[s[i]]
                i += 1
        return str(num) + dugaar(str(num)) if use_dugaar else str(num)

    def roman_handler(self, match):
        if match.group(2) != "":
            return self.roman_conv(match.group(1), False) + "-аас " + self.roman_conv(match.group(3))
        else:
            return self.roman_conv(match.group(1))

    def __call__(self, input_text):
        text = input_text["text"]
        text = text.replace("e-mongolia", "ий монгьоол яа")
        if input_text["read_roman_number"]:
            matches = list(re.finditer(r'\b([IVXLCDM]+)(-([IVXLCDM]+)|)\b', text))
            matches.sort(key=lambda x: -x.end())
            for m in matches:
                text = text[:m.start()] + self.roman_handler(m) + text[m.end():]

        urls = list(re.finditer(r"(https|http|)([:][/]{2}|)(www|)([.]|)([a-z]{2,})([.])([a-z]{2,3})", text))
        for m in urls[::-1]:
            text = text[:m.start(6)] + " цэг " + text[m.end(6):]
            if m[4]:
                text = text[:m.start(4)] + " цэг " + text[m.end(4):]

        if input_text["use_phonemizer"]:
            text = self.cyrillize(self.email_regex, text)
            # text = self.cyrillize(self.domain_regex, text)
            text = self.cyrillize(r"[A-Za-z]+", text)

        text = re.sub(r" +", " ", text)
        input_text["text"] = text
        return input_text


