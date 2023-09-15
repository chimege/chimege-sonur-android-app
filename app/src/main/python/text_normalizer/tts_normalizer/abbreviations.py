import re
from .normalizer_interface import Normalizer

suffix_code_map = {
    "N-HARIYALAH ": ["ний", "ны", "ийн", "ын", "н", "ий", "ы"],
    "N-UGUH_ORSHIH ": ["д", "т", "нд"],
    "N-ZAAH ": ["ыг", "ийг", "г"],
    "N-GARAH ": ["с", "ээс", "өөс", "аас", "оос", "нээс", "нөөс", "наас", "ноос"],
    "N-UILDEH ": ["р", "ээр", "өөр", "аар", "оор"],
    "N-HAMTRAH ": ["тэй", "тай", "той"],
    "N-CHIGLEH ": ["руу", "рүү"]

}
not_uildeh_regx = "([0-9])(_р)"

letter_vocal_map = {
    "Е": "ЕЕ",
    "Щ": "",
    "Ъ": "",
    "К": "КА",
    "З": "ЗЭ",
    "Ү": "ҮҮ",
    "Ш": "ИШ",
    "Г": "ГЭ",
    "Н": "ЭН",
    "Э": "ЭЭ",
    "Ж": "ЖЭ",
    "У": "УУ",
    "Ц": "ЦЭ",
    "Ф": "ФФ",
    "Й": "ХАГАС ИЙ",
    "Ы": "",
    "Б": "БЭ",
    "Ө": "ӨӨ",
    "А": "АА",
    "Х": "ХЭ",
    "Р": "ЭР",
    "О": "ОО",
    "Л": "ИЛ",
    "Д": "ДЭ",
    "П": "ПЭ",
    "Ю": "ЮҮ",
    "В": "ВЭ",
    "Ь": "",
    "Т": "ТЭ",
    "И": "ИЙ",
    "М": "ИМ",
    "С": "ЭС",
    "Ё": "ЁО",
    "Ч": "ЧЭ",
    "Я": "ЯА"
}


class Abbreviations(Normalizer):
    def __init__(self, name, abbreviation_file, conjugator):
        super().__init__(name)
        lines = open(abbreviation_file, 'r', encoding="utf-8").readlines()
        self.abbreviations = {}
        for line in lines:
            line = line.strip().split("|")
            if len(line) == 2:
                self.abbreviations[line[0].strip()] = line[1].strip()

        self.conjugator = conjugator

        self.signs = {" -": "-", "Чимэгэ": "Чимээгээ", "chimege": "чимээгээ",
                      "Chimege": "Чимээгээ", "чаямж": "чимээгээ", "мян. ": "мянган "}
        self.metrics = {"мкв": " метр квадрат", "гр": " грамм", "кг": " килограмм", "тн": " тонн", "км": " километр",
                        "мм": " миллиметр",
                        "см": " сантиметр", "°": " градус", "м3": " метр куб", "мл": " миллилитр",
                        "вт": " ватт", "мг": "миллиграмм",
                        "квт": " киловатт", "сек": " секунд", "%": " хувь",
                        "мин": " минут", "₮": " төгрөг", "\$": " доллар", "€": " евро", "¥": " иен", "£": " фунт",
                        "мвт": " мегаватт", "дм": " дециметр", "дм3": " дециметр куб",
                        "дм2": " дециметр квадрат", "ам.доллар": " америк доллар", "ам доллар": " америк доллар",
                        "м2": " метр квадрат", }
        self.conj_metr = {"л": " литр", "в": "вольт", "А": "ампер", "м": " метр"}

        self.re_allowed_str = '|'.join(sorted(self.metrics.keys(), key=len, reverse=True))
        self.re_allowed_str = self.re_allowed_str.replace(".", "\.")
        self.str = '|'.join(sorted(self.conj_metr.keys(), key=len, reverse=True))
        numbers = [
            "нэг", "хоёр", "гурван", "дөрвөн", "таван", "зургаан", "долоон", "есөн", "найман"
        ]
        self.numbers = " |".join(numbers)

    def replace_signs(self, text):
        for sign_key in self.signs.keys():
            text = text.replace(sign_key, self.signs[sign_key])
        return text

    def expand_all_metrics(self, text):
        matches = list(re.finditer('([^А-ЯӨҮЁа-яөүё]|^)(' + self.re_allowed_str + ')([^А-ЯӨҮЁа-яөүё+]|$)', text))
        for match in matches[::-1]:
            match_second_group = match.group(2)
            if match.group(2) == "$":
                match_second_group = "\$"
            metric_str = self.metrics[match_second_group]
            match_start_in_text = match.start() + match.group().index(match.group(2))
            match_end_in_text = match_start_in_text + len(match.group(2))
            text = text[:match_start_in_text] + metric_str + text[match_end_in_text:]
        for key in self.conj_metr.keys():
            if key in text:
                matches = list(
                    re.finditer(r'([^А-ЯӨҮЁа-яөүё\s]+|^])(' + self.str + ')([^А-ЯӨҮЁа-яөүё]|$)',
                                text))
                for match in matches[::-1]:
                    metric_str = self.conj_metr[match.group(2)]
                    match_start_in_text = match.start() + match.group().index(match.group(2))
                    match_end_in_text = match_start_in_text + len(match.group(2))
                    text = text[:match_start_in_text] + metric_str + text[match_end_in_text:]
        return text

    def combine_suffix(self, word, suffix):
        suffix_code = ""
        for code in suffix_code_map:
            if re.sub("[,.!?]", "", suffix) in suffix_code_map[code]:
                suffix_code = code
                break
        if suffix_code != "":
            conjugated = self.conjugator.form_conjugations(word, suffix_code.strip())[0]
        else:
            conjugated = self.conjugator.conjugate(word, suffix)
        return conjugated, suffix_code

    def expand_abbreviations(self, words, option):
        if option == "skip":
            return [words.lower()]

        def find_abbr(word):
            eval_word = word
            prefix = re.search(r"^[^А-ЯӨҮЁа-яөүё]+", word)
            if prefix is None:
                prefix = ""
            else:
                prefix = prefix.group()
                eval_word = eval_word[len(prefix):]
            suffix = re.search(r"[^А-ЯӨҮЁа-яөүё]+$", word)
            if suffix is None:
                suffix = ""
            else:
                suffix = suffix.group()
                eval_word = eval_word[:-len(suffix)]
            if eval_word in self.abbreviations.keys():
                if option == "letter":
                    return prefix + " ".join([letter_vocal_map[letter].lower() for letter in eval_word]) + suffix, True
                elif option == "abbreviation":
                    return prefix + self.abbreviations[eval_word].lower() + suffix, True
                else:
                    return word, True
            else:
                return word, False

        result = []
        for word in re.split("(\s)", words):
            if '▁' in word:
                if len(re.findall(not_uildeh_regx, word)) > 0:
                    continue
                word, suff = word.split('▁', 1)
                suff = suff.replace("-", "")
                word, found = find_abbr(word)
                if found:
                    if option == "letter":
                        word = word + " " + suff
                    elif option == "abbreviation":
                        word = word.split(" ")
                        last = word[-1]
                        conjugated, code = self.combine_suffix(last, suff.lower())
                        if code != "":
                            found = list(re.finditer(r"[\.,?!]", suff.lower()))
                            if len(found) > 0:
                                conjugated += found[0].group()
                        word = " ".join(word[:-1] + [conjugated])
                    else:
                        word = word + " " + suff
                else:
                    word = word + " " + suff
            else:
                word, _ = find_abbr(word)
            result.append(word)
        return result

    def __call__(self, input_text):
        text = input_text["text"]
        if text.upper() == text and len(text) > 5:
            text = text.lower()
        else:
            text = re.sub(r"([А-ЯӨҮЁ]{3,}[^а-яөүёА-ЯӨҮЁ]){3,}", lambda match_obj: match_obj.group().lower(), text)
        text = text.replace("ХААН", "хаан")
        text = re.sub(r" +", " ", text)
        abbr_suffixes = [x for x in re.finditer(r'([А-ЯӨҮЁ] ?\-[А-ЯӨҮЁа-яөүё])', text)]
        for match in abbr_suffixes[::-1]:
            text = text[:match.start() + 1] + "▁" + text[match.start() + 2:]
        text = ' '.join(text.split(" "))
        text = self.replace_signs(text)
        text = self.expand_all_metrics(text)
        text = self.expand_abbreviations(text, input_text["abbreviation_level"])
        text = ''.join(text)

        suffix_match_after_metrics = list(re.finditer("([А-ЯӨҮЁа-яөүё]+)-([а-яөүё]+|[А-ЯӨҮЁ]+)(\b|[-])", text))
        for match in suffix_match_after_metrics[::-1]:
            word = match.group(1)
            suffix = match.group(2)
            conjugated, code = self.combine_suffix(word, suffix)
            text = text[:match.start()] + conjugated + text[match.end():]

        if re.match(r'^[А-Яа-яӨөҮүЁё]+\s*[,\.]+$', text.strip()):
            text = text.strip().rstrip(',.')
        input_text["text"] = text
        return input_text
