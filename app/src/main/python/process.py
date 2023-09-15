from text_normalizer.tts_normalizer import normalize_tts_text, init_normalizers
import unicodedata as ud
import yaml
from os.path import join, dirname
config = yaml.safe_load(open(dirname(__file__) + "/text_normalizer/config.yaml", encoding="utf-8"))
init_normalizers(config["runtime_config"]["initial_config"])


def _get_char_lang(c):
    try:
        char_name = ud.name(c)
        if 'LATIN' in char_name:
            return 'en'
        if 'HANGUL' in char_name:
            return 'ko'
        if 'CJK' in char_name:
            return 'ja'
        if 'HIRAGANA' in char_name:
            return 'ja'
        if 'KATAKANA' in char_name:
            return 'ja'
        if 'KATAKANA' in char_name:
            return 'ja'
        if 'CYRILLIC' in char_name:
            return 'mn'
        return 'other'
    except Exception:
        return 'other'


def segment_text_by_language(text):
    current_lang = 'other'
    current_segment = ''
    segments = []
    for c in text:
        c_lang = _get_char_lang(c)
        if c_lang == 'other':
            current_segment += c
        else:
            if current_lang == 'other':
                current_lang = c_lang
                current_segment += c
            elif current_lang == c_lang:
                current_segment += c
            else:
                segments.append((current_lang, current_segment))
                current_lang = c_lang
                current_segment = '' + c
    if current_lang == 'other':
        current_lang = 'mn'
    segments.append((current_lang, current_segment))
    return segments


def process(
            text,
            read_emoji,
            abbreviation_level,
            number_chunk_size,
            dont_read_number_junction,
            read_dot_numbers_as_list_index,
            symbol_read_option,
            foreign_character_option,
            soft_threshold
        ):
    if text.strip() == "":
        return []
    if foreign_character_option == "leave":
        text_segments = segment_text_by_language(text)
    else:
        text_segments = [["mn", text]]
    normalized_segments = []
    for lang, segment in text_segments:
        if lang == "mn":
            options = dict(config["runtime_config"]["default_options"])
            options["read_emojis"] = read_emoji
            options["abbreviation_level"] = abbreviation_level
            options["number_chunker"] = number_chunk_size
            options["dont_read_number_n"] = dont_read_number_junction
            options["read_legal_number"] = read_dot_numbers_as_list_index
            options["read_symbols"] = symbol_read_option
            options["use_phonemizer"] = foreign_character_option
            options["text"] = segment
            segments = normalize_tts_text(options)
            for normed_segment in segments:
                if normed_segment.strip() != "":
                    if normed_segment[-1] not in ",.!?":
                        normed_segment = normed_segment + '.'
                    if normed_segment[-5:-1] == "тсүх":
                        normed_segment = normed_segment[:-5] + 'тсүхь' + normed_segment[-1]
                    normalized_segments.append([lang, normed_segment.lower()])
        else:
            if segment.strip() != "":
                normalized_segments.append([lang, segment])
    print(normalized_segments)
    return normalized_segments
