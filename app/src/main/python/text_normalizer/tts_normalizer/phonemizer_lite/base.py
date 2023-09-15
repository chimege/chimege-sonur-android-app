import abc
from typing import List, Dict

from .wrapper import EspeakWrapper


class BaseBackend(abc.ABC):
    def __init__(self, language: str):

        # ensure the backend is installed on the system
        if not self.is_available():
            raise RuntimeError(  # pragma: nocover
                '{} not installed on your system'.format(self.name()))

        # ensure the backend support the requested language
        self._language = self._init_language(language)

    @classmethod
    def _init_language(cls, language):
        """Language initialization

        This method may be overloaded in child classes (see Segments backend)

        """
        if not cls.is_supported_language(language):
            raise RuntimeError(
                f'language "{language}" is not supported by the '
                f'{cls.name()} backend')
        return language

    @property
    def language(self):
        """The language code configured to be used for phonemization"""
        return self._language

    @staticmethod
    @abc.abstractmethod
    def name():
        """The name of the backend"""

    @classmethod
    @abc.abstractmethod
    def is_available(cls):
        """Returns True if the backend is installed, False otherwise"""

    @classmethod
    @abc.abstractmethod
    def version(cls):
        """Return the backend version as a tuple (major, minor, patch)"""

    @staticmethod
    @abc.abstractmethod
    def supported_languages() -> Dict[str, str]:
        """Return a dict of language codes -> name supported by the backend"""

    @classmethod
    def is_supported_language(cls, language: str):
        """Returns True if `language` is supported by the backend"""
        return language in cls.supported_languages()

    def phonemize(self, text: List[str], strip: bool = False) -> List[str]:
        """Returns the `text` phonemized for the given language

        Parameters
        ----------
        text: list of str
            The text to be phonemized. Each string in the list
            is considered as a separated line. Each line is considered as a text
            utterance. Any empty utterance will be ignored.

        separator: Separator
            string separators between phonemes, syllables
            and words, default to separator.default_separator. Syllable separator
            is considered only for the festival backend. Word separator is
            ignored by the 'espeak-mbrola' backend.

        strip: bool
            If True, don't output the last word and phone separators
            of a token, default to False.

        njobs : int
            The number of parallel jobs to launch. The input text is
            split in ``njobs`` parts, phonemized on parallel instances of the
            backend and the outputs are finally collapsed.

        Returns
        -------
        phonemized text: list of str
            The input ``text`` phonemized for the given ``language`` and ``backend``.

        Raises
        ------
        RuntimeError
            if something went wrong during the phonemization

        """
        if isinstance(text, str):
            # changed in phonemizer-3.0, warn the user
            raise RuntimeError(
                'input text to phonemize() is str but it must be list of str')

        phonemized = self._phonemize_aux(text, 0, strip)
        return phonemized

    @abc.abstractmethod
    def _phonemize_aux(self, text: List[str], offset: int, strip: bool) -> List[str]:
        """The "concrete" phonemization method

        Must be implemented in child classes. `separator` and `strip`
        parameters are as given to the phonemize() method. `text` is as
        returned by _phonemize_preprocess(). `offset` is line number of the
        first line in `text` with respect to the original text (this is only
        usefull with running on chunks in multiple jobs. When using a single
        jobs the offset is 0).

        """


class BaseEspeakBackend(BaseBackend):
    """Abstract espeak backend for the phonemizer

    Base class of the concrete backends Espeak and EspeakMbrola. It provides
    facilities to find espeak library and read espeak version.

    """

    def __init__(self, language: str):
        super().__init__(language)

        self._espeak = EspeakWrapper()

    @classmethod
    def set_library(cls, library):
        """Sets the espeak backend to use `library`

        If this is not set, the backend uses the default espeak shared library
        from the system installation.

        Parameters
        ----------
        library (str or None) : the path to the espeak shared library to use as
            backend. Set `library` to None to restore the default.

        """
        EspeakWrapper.set_library(library)

    @classmethod
    def library(cls):
        """Returns the espeak library used as backend

        The following precedence rule applies for library lookup:

        1. As specified by BaseEspeakBackend.set_library()
        2. Or as specified by the environment variable
           PHONEMIZER_ESPEAK_LIBRARY
        3. Or the default espeak library found on the system

        Raises
        ------
        RuntimeError if the espeak library cannot be found or if the
            environment variable PHONEMIZER_ESPEAK_LIBRARY is set to a
            non-readable file

        """
        return EspeakWrapper.library()

    @classmethod
    def is_available(cls) -> bool:
        try:
            EspeakWrapper()
        except RuntimeError:  # pragma: nocover
            return False
        return True

    @classmethod
    def is_espeak_ng(cls) -> bool:
        """Returns True if using espeak-ng, False otherwise"""
        # espeak-ng starts with version 1.49
        return cls.version() >= (1, 49)

    @classmethod
    def version(cls):
        """Espeak version as a tuple (major, minor, patch)

        Raises
        ------
        RuntimeError if BaseEspeakBackend.is_available() is False or if the
            version cannot be extracted for some reason.

        """
        return EspeakWrapper().version
