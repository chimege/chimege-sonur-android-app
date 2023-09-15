import re

from .normalizer_interface import Normalizer


class PreProcessor(Normalizer):
    def __init__(self, name):
        super().__init__(name)

    def __call__(self, input_text):
        text = input_text["text"]
        if input_text["read_balarhai_egshig_clearly"]:
            masc_vowels = ["а", "у", "о", "и"]
            def replace12435(m):
                if m.group(2) == "г" and m.group(1) in masc_vowels and m.group(4) in masc_vowels:
                    return m.group(1) + m.group(2) + m.group(3) + m.group(5)
                else:
                    return m.group(1) + m.group(2) + m.group(4) + m.group(3) + m.group(5)

            def replace124358(m):
                if m.group(2) == "г" and m.group(1) in masc_vowels and m.group(4) in masc_vowels:
                    return m.group(1) + m.group(2) + m.group(3) + m.group(5) + m.group(8)
                else:
                    return m.group(1) + m.group(2) + m.group(4) + m.group(3) + m.group(5) + m.group(8)

            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([с]\4[н])", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([л]\4\4)", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([г][ү])(й) ([э]{2})\b", r"\1\2\4", text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([л](уу|үү)[д])", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([ж][аэоу]{2})", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([д]\4[г])", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([н])(\4)( )(уу|үү)\b", replace124358, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([х]\4[д])", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([н])([аэоуө])([ч][л]\4[х])", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([л])([аэоуө])([л](ы|ий)[н])", r"\1\2\4", text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([с][н]\4\4[р])", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([с][н](ы|ий))", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([а-яөүё])([л])([аэоуө])([с]\4\4[р])", replace12435, text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([л])([аэоуө])(дгийг)", r"\1\2\4", text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])(ын|ийн)( )(уу|үү)\b", r"\1\2\4", text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([с])([аэоуө])([н])( )(уу|үү)\b", r"\1\2\4\6", text, flags=re.IGNORECASE)
            text = re.sub(r"([а-яөүё])([аэоуө][н])( )(уу|үү)\b", r"\1\2\4", text, flags=re.IGNORECASE)

        text = text.replace("Щ", "Ш").replace("щ", "ш")
        text = re.sub(r"[\"`”“‘’]", "'", text)
        text = re.sub(r"[^А-ЯӨҮЁа-яөүёA-Za-z0-9!\'(),\.:;\?\ \-°$₮¥€£%¢+*~&()#=%№@<>\[\]{}\|~№/\n]", " ", text)
        input_text["text"] = text
        return input_text
