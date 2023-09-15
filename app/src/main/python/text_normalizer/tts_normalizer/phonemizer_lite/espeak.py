import re
from typing import Optional, Union

from .base import BaseEspeakBackend
from .wrapper import EspeakWrapper


class EspeakBackend(BaseEspeakBackend):
    """Espeak backend for the phonemizer"""
    # a regular expression to find phonemes stresses in espeak output
    _ESPEAK_STRESS_RE = re.compile(r"[ˈˌ'-]+")

    # pylint: disable=too-many-arguments
    def __init__(self, language: str,
                 with_stress: bool = False,
                 tie: Union[bool, str] = False):
        super().__init__(language)

        self._espeak.set_voice(language)
        self._with_stress = with_stress
        self._tie = self._init_tie(tie)

    @staticmethod
    def _init_tie(tie) -> Optional[str]:
        if not tie:
            return None

        if tie is True:  # default U+361 tie character
            return '͡'

        # non default tie charcacter
        tie = str(tie)
        if len(tie) != 1:
            raise RuntimeError(
                f'explicit tie must be a single charcacter but is {tie}')
        return tie

    @staticmethod
    def name():
        return 'espeak'

    @classmethod
    def supported_languages(cls):
        return {
            voice.language: voice.name
            for voice in EspeakWrapper().available_voices()}

    def _phonemize_aux(self, text, offset, strip):
        output = []
        for num, line in enumerate(text, start=1):
            line = self._espeak.text_to_phonemes(line, self._tie)
            line = self._postprocess_line(line, num, strip)
            output.append(line)
        return output

    def _process_stress(self, word):
        if self._with_stress:
            return word
        # remove the stresses on phonemes
        return re.sub(self._ESPEAK_STRESS_RE, '', word)


    def _postprocess_line(self, line: str, num: int, strip: bool) -> str:
        line = line.strip().replace('\n', ' ').replace('  ', ' ')
        line = re.sub(r'_+', '_', line)
        line = re.sub(r'_ ', ' ', line)

        if not line:
            return ''

        out_line = ''
        for word in line.split(' '):
            word = self._process_stress(word.strip())
            if not strip and self._tie is None:
                word += '_'
            word = word.replace('_', '')
            out_line += word

        return out_line
