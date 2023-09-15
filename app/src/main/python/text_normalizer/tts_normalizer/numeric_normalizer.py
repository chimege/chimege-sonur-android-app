import re

from .mongolian_digit_letter import *
from .normalizer_interface import Normalizer

NUM_ENDED = r' *([^a-zA-Zа-яА-ЯөӨүҮ0-9%°\$₮ ]|$|дугаар|дүгээр|орчим|хавьцаа|N-HARIYALAH|N-UGUH_ORSHIH|N-ZAAH|N-GARAH|N-UILDEH|N-HAMTRAH|N-CHIGLEH|нэмэх|хасах|үржих|хуваах|тэнцүү|хүртэлх|хүртэл|илүүтэй|илүү|гаруй|хүрнэ|дахь|дэх|уулаа|үүлээ|байна|бол*)'

suffix_code_map = {
    "N-HARIYALAH ": ["ийн", "ын", "ий", "ы"],
    "n-hariyalah ": ["ний", "ны"],
    "N-UGUH_ORSHIH ": ["д", "т"],
    "n-uguh_orshih ": ["нд"],
    "N-ZAAH ": ["ыг", "ийг", "г"],
    "N-GARAH ": ["с", "ээс", "өөс", "аас", "оос", "нээс", "нөөс", "наас", "ноос"],
    "N-UILDEH ": ["р", "ээр", "өөр", "аар", "оор"],
    "N-HAMTRAH ": ["тэй", "тай", "той"],
    "N-CHIGLEH ": [" руу", " рүү"]
}


class NumericNormalizer(Normalizer):
    def __init__(self, name, conjugator):
        super().__init__(name)

        self.l = [
            (r'([0-9]+)(-р|р)\b', 2, lambda x, options: dugaar(x.group(1))),
            (r'( {0,1}(#|№) {0,1})([0-9]+)', 1, lambda x, options: dugaar(x.group(2))),
            (r'([0-9]+)(-*(ы|ий)*г)\b', 2, lambda x, options: "N-ZAAH "),
            (r'([0-9]+)(-*(ийн|ын|ий|ы))\b', 2, lambda x, options: "N-HARIYALAH "),
            (r'([0-9]+)(-*(ний|ны))\b', 2, lambda x, options: "n-hariyalah "),
            (r'([0-9]+)(-*т(а|э|о|ө)й)\b', 2, lambda x, options: "N-HAMTRAH "),
            (r'([0-9]+)(-*(д|т))\b', 2, lambda x, options: "N-UGUH_ORSHIH "),
            (r'([0-9]+)(-*(нд))\b', 2, lambda x, options: "n-uguh_orshih "),
            (r'([0-9]+)(-*н*(аа|ээ|оо|өө)*с)\b', 2, lambda x, options: "N-GARAH "),
            (r'([0-9]+)(-*(аа|ээ|оо|өө)*р)\b', 2, lambda x, options: "N-UILDEH "),
            (r'([0-9]+)(-*(руу|рүү))\b', 2, lambda x, options: "N-CHIGLEH "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*(ы|ий)*г)\b', 1, lambda x, options: "N-ZAAH "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-(ийн|ын|ий|ы))\b', 1, lambda x, options: "N-HARIYALAH "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*(ний|ны))\b', 1, lambda x, options: "n-hariyalah "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*т(а|э|о|ө)й)\b', 1, lambda x, options: "N-HAMTRAH "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*(д|т))\b', 1, lambda x, options: "N-UGUH_ORSHIH "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*(нд))\b', 1, lambda x, options: "n-uguh_orshih "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*н*(аа|ээ|оо|өө)*с)\b', 1, lambda x, options: "N-GARAH "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*(аа|ээ|оо|өө)*р)\b', 1, lambda x, options: "N-UILDEH "),
            (r'[^A-Za-zА-ЯӨҮЁа-яөүё0-9▁\- ](-*(руу|рүү))\b', 1, lambda x, options: "N-CHIGLEH "),

            (r'(-(ы|ий)*г)\b', 1, lambda x, options: "N-ZAAH "),
            (r'(-(ийн|ын|ий|ы))\b', 1, lambda x, options: "N-HARIYALAH "),
            (r'(-(ний|ны))\b', 1, lambda x, options: "n-hariyalah "),
            (r'(-т(а|э|о|ө)й)\b', 1, lambda x, options: "N-HAMTRAH "),
            (r'(-(д|т))\b', 1, lambda x, options: "N-UGUH_ORSHIH "),
            (r'(-(нд))\b', 1, lambda x, options: "n-uguh_orshih "),
            (r'(-н*(аа|ээ|оо|өө)*с)\b', 1, lambda x, options: "N-GARAH "),
            (r'(-(аа|ээ|оо|өө)*р)\b', 1, lambda x, options: "N-UILDEH "),
            (r'(-(руу|рүү))\b', 1, lambda x, options: "N-CHIGLEH "),
            (r"\b([0-9]{1,3}[.])([0-9]{1,3}[.])([0-9]{1,3}[.])([0-9]{1,3})([:][0-9]{1,5}|)\b", 0, lambda x, options: self.ip_address(x)),
            (r'\b([0-9]{3})-([0-9]{8})\b',
             lambda x, options: number2word(x.group(1).strip()) + " " + self.eight_digit(x.group(2).strip())),
            (
                r'([0-9]{4}|\b[А-ЯӨҮЁа-яөүё]+\b) *оны *([0-1]{0,1}[0-9]|\b[А-ЯӨҮЁа-яөүё]+\b) *сарын *([0-3]{0,1}[0-9])( өдөр|)',
                0,
                lambda x, options: self.date(x.group(1), x.group(2), x.group(3), end=x.group(4))),
            (r'\b([0-3]{0,1}[0-9])(/|\\|\.)([0-1]{0,1}[0-9])(\2)([0-9]{4})( өдөр|)',
             lambda x, options: self.date(x.group(5), x.group(3), x.group(1), end=x.group(6))),
            (r'\b([0-9]{4})(/|\\|\.)([0-1]{0,1}[0-9])(\2)(([0-3]{0,1}[0-9])-([0-3]{0,1}[0-9]))( өдөр|)',
             lambda x, options: self.date(x.group(1), x.group(3), x.group(6), x.group(7), end=x.group(6),
                                          range=True)),
            (r'\b([0-9]{4})(/|\\|\.|-)([0-1]{0,1}[0-9])(\2)([0-3]{0,1}[0-9])( өдөр|)',
             lambda x, options: self.date(x.group(1), x.group(3), x.group(5), end=x.group(6))),
            (r'([0-1]{0,1}[0-9]) *(сарын) *(([0-3]{0,1}[0-9])-([0-3]{0,1}[0-9]))( өдөр|)',
             lambda x, options: self.date(x.group(1), x.group(4), x.group(5), end=x.group(6), range=True)),
            (r'([0-1]{0,1}[0-9]) *(сарын) *([0-3]{0,1}[0-9])( өдөр|)',
             lambda x, options: self.date(x.group(1), x.group(3), end=x.group(4))),
            (r'\b(сарын) *(([0-3]{0,1}[0-9])-([0-3]{0,1}[0-9]))( өдөр|)',
             lambda x, options: self.date(x.group(3), x.group(4), end=x.group(5), range=True)),
            (r'\b(сарын) *([0-3]{0,1}[0-9]) *[Nn]', 2,
             lambda x, options: number2word(x.group(2), False, force_one_two_ending=True)),
            (r'харьцаа (([0-9]+)[:]([0-9]+[\.,][0-9]+))\b', 1, lambda x, options: self.ratio(x, True)),
            (r'харьцаа (([0-9]+)[:]([0-9]+))\b', 1, lambda x, options: self.ratio(x)),
            (
                r'([0-9]{1,2}:[0-9]{1,2})-([0-9]{1,2}:[0-9]{1,2})',
                lambda x, options: x.group(1) + "N-GARAH " + x.group(2)
            ),
            (
                r'([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})( *секунд|)',
                lambda x, options: self.time_writer(x.group(1), x.group(2), x.group(3))
            ),
            (
                r'([0-9]{1,2}):([0-9]{1,2})( *минут|)',
                lambda x, options: self.time_writer(x.group(1), x.group(2))
            ),
            (r'\b[0-9]{2}\-[0-9]{6}\b',
             lambda x, options: x.group().replace("-", "").strip()),
            (r'\b(88|81|85|89|77|75|95|99|91|11|98|96|94|65|80)[0-9]{2}\-[0-9]{4}\b',
             lambda x, options: x.group().replace("-", "").strip()),
            (r'\b(([0-9]{4})-([0-9]{4})) *(он|онуудад|онд)', 1,
             lambda x, options: number2word(x.group(2)) + "N-GARAH " + number2word(x.group(3), is_fina=False)),
            (r'([0-9]+)( {0,1}\* {0,1})', 2, lambda x, options: " үржих нь "),
            (r'([0-9]+)( {0,1}\+ {0,1})', 2, lambda x, options: " нэмэх нь "),
            (r'([А-ЯӨҮЁа-яөүё]+|^) ([-])[0-9]+', 2, lambda x, options: " хасах "),
            (r'([0-9]+[\.,]*[0-9]*)( {0,1}[А-ЯӨҮЁа-яөүё]*)( {0,1}- {0,1})([0-9]+[\.,]*[0-9]*)(\2)', 3,
             lambda x, options: "N-GARAH "),
            (r'\b[A-ZА-ЯӨҮЁ]{2} [0-9]{8}\b',
             lambda x, options: self.register(x.group().strip())),
            (r'\b([0-9]{2}):([0-9]{2})', lambda x, options: time2word(x)),
            (r'\b([0-9]{4})([А-ЯӨҮЁ]{3})', lambda x, options: self.car_plate_num(x)),
            (r'\+([0-9]{2,3})[ -][0-9]{8}', 1, lambda x, options: number2word(x.group(1).strip())),
            (r'\b([0-9]{8})' + NUM_ENDED, 1, lambda x, options: self.eight_digit(x.group(1).strip())),
            (r'\b([0-9]{8})\b', 1, lambda x, options: self.eight_digit(x.group(1).strip())),
            (r"[0-9]{1,3}(,[0-9]{3,3})+",
             lambda x, options: x.group().replace(",", "")),
            (r"[0-9]{1,2}(\.[0-9]{1,2}){2,}", lambda x, options: self.law_zuil(x.group())),
            (r'\b(зүйл|зүйлийн|дүрмийн|дүрэм) ?(\b[0-9]+(\.|,)[0-9]+)',
             2, lambda x, options: self.law_zuil(x.group(2))),
            (r"([0-9]+)/([0-9]+)", lambda x, options: self.proper_fraction(x)),
            (r'\b([0-9]+[\.,][0-9]+)' + NUM_ENDED, 1,
             lambda x, options: self.law_zuil(x.group(1)) if options["read_legal_number"] else fraction2word(
                 x.group(1).strip()) + ""),
            (r'\b[0-9]+(\.|,)[0-9]+',
             lambda x, options: self.law_zuil(x.group()) if options["read_legal_number"] else fraction2word(
                 x.group().strip(), False) + ""),
            (r'(^|\n)\s*([0-9]{1,2}\.) (.*)', 2,
             lambda x, options: x.group(2) if re.search(r'\s([0-9]{1,2}\.)\s', x.group(3)) else number2word(
                 x.group(2)[:-1]) + '-т'),
            (r'\b([0-9]+)' + NUM_ENDED, 1, lambda x, options: " " + number2word(x.group(1).strip()) + ""),
            (r'\b(шинийн|Шинийн|билгийн|Билгийн) *([0-9]{1,2})', 2,
             lambda x, options: number2word(x.group(2), False, force_one_two_ending=True)),
            (r'(?=\b([0-9]+) +([0-9]+|нэг|хоёр|гурав|дөрөв|тав|зургаа|долоо|найм|ес)(\b|$))', 1, lambda x, options: number2word(x.group(1).strip())),
            (r'\b[0-9]+', 0, lambda x, options: number2word(x.group().strip(), options["dont_read_number_n"]) + " "),
            (r'([0-9]+)', 1, lambda x, options: " " + number2word(x.group(1).strip()) + " ")
        ]

        self.conjugation_codes = [
            "N-HARIYALAH", "N-UGUH_ORSHIH", "N-ZAAH", "N-GARAH", "N-UILDEH", "N-HAMTRAH", "N-CHIGLEH"]
        self.conjugation_merger_regex = r"(\w+) *(N-HARIYALAH|n-hariyalah|N-UGUH_ORSHIH|n-uguh_orshih|N-ZAAH|N-GARAH|N-UILDEH|N-HAMTRAH|N-CHIGLEH)"
        self.conjugator = conjugator
        self.current_option = None

    def __call__(self, input_text):
        text = input_text["text"]
        self.current_option = input_text

        if input_text["number_chunker"] == "single":
            text = re.sub(r"([0-9]{1}|[.,])", r" \1 [CHUNK_SEP]", text).strip("[CHUNK_SEP]")
        elif input_text["number_chunker"] == "double":
            text = re.sub(r"([0-9]{2}|[.,])", r" \1 [CHUNK_SEP]", text).strip("[CHUNK_SEP]")
            input_text["dont_read_number_n"] = True
        elif input_text["number_chunker"] == "whole":
            text = re.sub(r"\b([0-9]+)\b", lambda x: number2word(x.group(1)), text)
        elif input_text["number_chunker"] == "default":
            pass
        else:
            raise ValueError("Unsupported number chunking option")

        text = re.sub(r"([.,])[ ]\[CHUNK_SEP\]", r"\1", text)
        text = re.sub(r"\[CHUNK_SEP\]([^0-9 ]|[ ][^0-9])", r"\1", text)
        if input_text["read_symbols"] != "no_temdegt":
            text = text.replace("[CHUNK_SEP]", "ΣSKIPCOMMAΣ")
        else:
            text = text.replace("[CHUNK_SEP]", ",")

        text = re.sub(r" +", " ", text)
        text = re.sub(r"(\bсарын[ ]+[0-9]{1,2})[ ]+([0-9]{2}:[0-9]{2})", r"\1 N-HARIYALAH \2", text)
        text = re.sub(r"([А-ЯӨҮЁа-яөүё])-([0-9]+) ", r"\1 \2[END] ", text)

        heading_zero_matches = list(re.finditer(r"([ ]|^)([0]+)([0-9]+)\b", text))[::-1]
        for m in heading_zero_matches:
            text = text[:m.start(2)] + m.group(2).replace("0", "~ZERO~") + text[m.end(2):]

        text = re.sub(
            r"( доллар| төгрөг| евро| иен| фунт)(([0-9]+[.][0-9]+|[0-9]+) *(сая|мянга|зуу|тэрбум|))(-)\1([0-9]+ *(сая|мянга|зуу|тэрбум|))",
            r"\2\5\6 \1", text)
        text = re.sub(r"( доллар| төгрөг| евро| иен| фунт)(([0-9]+[.][0-9]+|[0-9]+) *(сая|мянга|зуу|тэрбум|)([а-яөүё]+\b))", r"\2\1", text)


        text = self.pad(text)
        for z in self.l:
            log = False
            if len(z) == 4:
                reg, g, repl, log = z
            elif len(z) == 3:
                reg, g, repl = z
            else:
                reg, repl = z
                g = 0
            if log:
                print("INPUT", text)
            matches = list(re.finditer(reg, text))
            matches.sort(key=lambda y: -y.end())
            for m in matches:
                text = text[:m.start(g)] + repl(m, input_text) + text[m.end(g):]

        text = self.resolve_conjugations(text)

        text = re.sub(r"\s+", " ", text)
        text = text.replace("цаг цаг", "цаг").replace("минут минут", "минут")
        input_text["text"] = text.strip().replace("[END]", "").replace("~ZERO~", "тэг ")
        return input_text

    def resolve_conjugations(self, text):
        conjugation_matches = list(re.finditer(self.conjugation_merger_regex, text))
        for match in conjugation_matches[::-1]:
            if len(match.group(1)) > 1:
                conjugated_word = self.conjugator.form_conjugations(
                    match.group(1), match.group(2))[0] + " "
                text = text[:match.start()] + conjugated_word + text[match.end():]

        suffix_match_after_metrics = list(re.finditer("([А-ЯӨҮЁа-яөүё]+)-([а-яөүё]+)", text))
        for match in suffix_match_after_metrics[::-1]:
            word = match.group(1)
            suffix = match.group(2)
            if len(word) > 1:
                if suffix not in number_words:
                    conjugated = self.combine_suffix(word, suffix)
                    text = text[:match.start()] + conjugated + text[match.end():]
        return text

    def pad(self, txt):
        txt = re.sub(r"([А-ЯӨҮЁа-яөүё])([0-9])", r"\1 \2", txt)
        return " " + txt + " "

    def combine_suffix(self, word, suffix):
        suffix_code = ""
        for code in suffix_code_map:
            if re.sub("[,.!?]", "", suffix) in suffix_code_map[code]:
                suffix_code = code
                break
        if suffix_code != "":
            conjugated = self.conjugator.form_conjugations(
                word, suffix_code.strip())[0]
        else:
            conjugated = self.conjugator.conjugate(word, suffix)
        return conjugated

    def date(self, *args, end, range=False):
        text = date2word(".".join(args), range)
        if end != "":
            text = text + "n-hariyalah өдөр"
        return text

    def time_writer(self, hour="00", minute="00", second="00"):
        result = number2word(hour, False) + " цаг"
        if minute != "00":
            result += " " + number2word(minute, False) + " минут"
        if second != "00":
            result += " " + number2word(second, False) + " секунд"
        return result

    def four_digit(self, txt):
        tmp = []
        for i in range(2):
            if txt[i * 2] == "0":
                t = "тэг " + number2word(txt[(i * 2 + 1):(i * 2 + 2)])
            else:
                t = number2word(txt[i * 2:(i * 2 + 2)])
            tmp.append(t)
        return " ".join(tmp)

    def eight_digit(self, txt):
        tmp = []
        for i in range(4):
            if txt[i * 2] == "0":
                t = "тэг " + number2word(txt[(i * 2 + 1):(i * 2 + 2)])
            else:
                t = number2word(txt[i * 2:(i * 2 + 2)])
            if i == 3:
                tmp.append(t)
            else:
                if self.current_option["read_symbols"] != "no_temdegt":
                    tmp.append(t + "ΣSKIPCOMMAΣ")
                else:
                    tmp.append(t + ",")
        return " ".join(tmp)

    def ratio(self, match, second_fraction=False):
        first_num = number2word(match.group(2))
        if not second_fraction:
            second_num = number2word(match.group(3))
        else:
            second_num = fraction2word(match.group(3))
        return first_num + "N-ZAAH харьцах нь " + second_num

    def register(self, txt):
        return " ".join(txt.split()[0]) + " " + self.eight_digit(txt.split()[1])

    def law_zuil(self, zuil):
        if "." in zuil:
            zuils = zuil.split(".")
            need_suffix = zuils[:-1]
            attached_suffix = []
            for zuil in need_suffix:
                zuil_str = number2word(zuil)
                attached_suffix.append(zuil_str + "-ын")
            attached_suffix.append(number2word(zuils[-1]))
            return " ".join(attached_suffix)
        else:
            return zuil

    def car_plate_num(self, plate):
        numbers = plate.group(1)
        chars = plate.group(2)
        numbers = " ".join(number2word(numbers[i * 2:(i * 2 + 2)]) for i in range(2))
        return numbers + " " + chars

    def proper_fraction(self, fraction):
        numerator = number2word(fraction.group(1))
        dominator = number2word(fraction.group(2), False)
        if dominator == "нэг":
            dominator = "нэгн"
        if dominator == "хоёр":
            dominator = "хоёрон"
        return dominator + "n-hariyalah  " + numerator

    def ip_address(self, match):
        replacement = ""
        ips = [match.group(1), match.group(2), match.group(3)]
        port = match.group(5)
        for ip in ips:
            ip = re.sub(r"[.]", "", ip)
            replacement += number2word(ip) + " N-HARIYALAH "

        last_ip = match.group(4)
        replacement += number2word(last_ip)

        if port != "":
            replacement += " N-HARIYALAH "
            port = re.sub(r"[:]", "", port)
            replacement += number2word(port) + " порт"
        return replacement