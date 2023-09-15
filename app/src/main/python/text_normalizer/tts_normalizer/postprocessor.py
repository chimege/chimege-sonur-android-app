import re

from .normalizer_interface import Normalizer


class PostProcessor(Normalizer):
    def __init__(self, name, symbols_file):
        super().__init__(name)
        self.symbols_file = symbols_file

    def __call__(self, input_text):
        text = input_text["text"]
        if input_text["read_symbols"] != "unshihgui_custom_temdegt":
            chars_to_keep = "".join(self.symbols_file[input_text["read_symbols"]].keys())
        else:
            chars_to_keep = "".join([s for s in self.symbols_file["buh_temdegt"].keys() if
                                     s not in self.symbols_file["unshihgui_custom_temdegt"]])

        text = re.sub(r"[^-_.,!?:\"'Σ \-А-ЯӨҮЁа-яөүёA-Za-z" + re.escape(chars_to_keep) + "]", " ", text)
        text = re.sub(r"\s+", " ", text)

        text = re.sub(rf"([!',.:;?\-{re.escape(chars_to_keep)}] *)\1+", r"\1", text)
        input_text["text"] = text.strip()
        return input_text
