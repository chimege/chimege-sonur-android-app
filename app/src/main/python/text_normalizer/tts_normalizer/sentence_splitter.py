import re

from .normalizer_interface import Normalizer

letter_vocal_map = {
    "Е": "ЕЕ",
    "Щ": "ИШ",
    "Ъ": "ХАТУУГИЙН ТЭМДЭГ",
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
    "Ф": "ФЭ",
    "Й": "ХАГАС ИЙ",
    "Ы": "ЭР ҮГИЙН ИЙ",
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
    "Ь": "ЗӨӨЛНИЙ ТЭМДЭГ",
    "Т": "ТЭ",
    "И": "ИЙ",
    "М": "ИМ",
    "С": "ЭС",
    "Ё": "ЁО",
    "Ч": "ЧЭ",
    "Я": "ЯА",
}


class SentenceSplitter(Normalizer):
    def __init__(self, name, config, symbols_file, conjugator):
        super().__init__(name)
        self.soft_threshold = config["soft_threshold"]
        self.hard_threshold = config["hard_threshold"]
        self.symbols_file = symbols_file
        self.conjugation_merger_regex = r"(\w+) *(N-HARIYALAH|n-hariyalah|N-UGUH_ORSHIH|n-uguh_orshih|N-ZAAH|N-GARAH|N-UILDEH|N-HAMTRAH|N-CHIGLEH)"
        self.conjugator = conjugator

    def after_split(self, text, options):
        text = text.replace("●", " ")
        text = text.replace("[QUOTA]", ".'")

        if options["abbreviation_level"] != "word":
            for match in reversed(list(re.finditer(r'\b[А-ЯӨҮЁ]+\b', text))):
                if len(match.group()) < 5:
                    text = text[:match.start()] + " ".join(letter_vocal_map[letter] for letter in match.group()) + text[
                                                                                                                   match.end():]
        if options["read_symbols"] == "unshihgui_custom_temdegt":
            symbols = {k: v for k, v in self.symbols_file["buh_temdegt"].items() if
                       k not in self.symbols_file["unshihgui_custom_temdegt"]}.items()
        else:
            symbols = self.symbols_file[options["read_symbols"]].items()

        for symbol, string in symbols:
            if symbol == "-" or symbol == "_":
                continue
            text = text.replace(symbol, " " + string + " ")

        text = text.replace("ΣSKIPCOMMAΣ", ",")
        text = text.replace("Σ", "")

        text = re.sub(r'(\([А-ЯӨҮЁа-яөүё ]+\))(N-[A-Za-z]+)', r'\2 \1', text)
        conjugation_matches = list(re.finditer(self.conjugation_merger_regex, text))
        for match in conjugation_matches[::-1]:
            conjugated_word = self.conjugator.form_conjugations(match.group(1), match.group(2))[0] + " "
            text = text[:match.start()] + conjugated_word + text[match.end():]
        text = re.sub(
            "(N-HARIYALAH|n-hariyalah|N-UGUH_ORSHIH|n-uguh_orshih|N-ZAAH|N-GARAH|N-UILDEH|N-HAMTRAH|N-CHIGLEH)", "",
            text)
        if "-" in text and "-" in dict(symbols):
            text = text.replace("-", " хасах ")
        if "_" in text and "_" in dict(symbols):
            text = text.replace("_", "доогуур зураас")

        for match in reversed(list(re.finditer(r"(^|\b[А-ЯӨҮЁа-яөүё]{1} |\s{2,})([а-яөүё]{1})(?![-])\b", text))):
            text = text[:match.start(2)] + letter_vocal_map[match.group(2).upper()] + text[match.end(2):]

        chars_to_keep = "A-Za-z" if not options["use_phonemizer"] else ""
        text = re.sub(r"^[^а-яөүёА-ЯӨҮЁ" + chars_to_keep + "]+(.*)", r"\1", text).strip()
        text = re.sub("( )+", " ", text).strip()
        text = re.sub(r"(\w) ([!,\.:;\?\-])", r"\1\2", text)
        return text

    def can_add(self, current_buffer, new_buffer, sentence):
        before_join_distance = self.soft_threshold - len(current_buffer)
        after_join_distance = len(new_buffer) - self.soft_threshold
        if re.search(r"[\.!\?]", sentence) and re.search(r"[\.!\?]", current_buffer) is None:
            should_join = True  # must join
        else:
            should_join = after_join_distance < before_join_distance
        return should_join and len(new_buffer) < self.hard_threshold

    def join_to_optimal_val(self, elements):
        optimal_splits = []
        buffer = ""
        for sentence in elements:
            sentence = re.sub(r"^[\.!\?:;,]+", "", sentence)
            new_buffer = buffer + sentence
            if self.can_add(buffer, new_buffer, sentence):
                buffer = new_buffer
            else:
                optimal_splits.append(buffer)
                buffer = sentence
        optimal_splits.append(buffer)
        return optimal_splits

    def __call__(self, input_text):
        text = input_text["text"]
        while re.search(r"([А-ЯӨҮЁ])\.([А-ЯӨҮЁ])", text):
            text = re.sub(r"([А-ЯӨҮЁ])\.([А-ЯӨҮЁ])", r"\1●\2", text)
        text = re.sub(r"\.['\"]", "[QUOTA]", text)
        text = re.sub(r"([А-ЯӨҮЁ][а-яөүё]+)[\-]([А-ЯӨҮЁ])", r"\1 \2", text)
        sentences = [text]

        if input_text["split_sentences"]:
            for pattern in ".!?'\"():;, ":
                splitted_sentences = []
                for sentence in sentences:
                    if len(sentence) > self.hard_threshold and pattern in sentence:
                        arr = [s + pattern for s in sentence.split(pattern)]
                        arr[-1] = arr[-1][:-1]
                        if pattern == " ":
                            arr = self.join_to_optimal_val(arr)
                        splitted_sentences.extend(arr)
                    else:
                        splitted_sentences.append(sentence)
                sentences = splitted_sentences

            splitted_sentences = []
            for sentence in sentences:
                if len(sentence) > self.hard_threshold:
                    splitted_sentences.extend([
                        sentence[i:i + self.soft_threshold] for i in range(0, len(sentence), self.soft_threshold)])
                else:
                    splitted_sentences.append(sentence)

            new_sentences = self.join_to_optimal_val(splitted_sentences)
            new_sentences = [self.after_split(s, input_text) for s in new_sentences if re.search(r"[A-Za-zА-ЯӨҮЁа-яөүё]", s)]
            validated = []
            for s in new_sentences:
                if len(s) < self.hard_threshold:
                    validated.append(s)
                else:
                    validated.extend([s[:self.hard_threshold], s[self.hard_threshold:]])
            validated = [v for v in validated if re.search(r"[A-Za-zА-ЯӨҮЁа-яөүё]", v)]
            return validated
        else:
            return [self.after_split(text, input_text)]
