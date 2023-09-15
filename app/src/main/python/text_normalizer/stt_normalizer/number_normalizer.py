from .utils import *
from .definitions import *


def normalize_numbers(text, mode):
    text, local_encodings = encode_special_cases(text, local_cases)
    text, replaced = suffix_separator(text)
    s = {
        "num": 0,
        "may_see_digit": True,
        "may_see_decimal": True,
        "may_see_multiplier": True,
        "may_see_cent": True,
        "multiplied_val": 0,
        "cent_val": 0,
        "tricky_buffer": "",
        "tricky_buffer_num": "",
        "processing_number": False,
    }

    def stop(s):
        s['may_see_digit'] = False
        s['may_see_decimal'] = False
        s['may_see_multiplier'] = False
        s['may_see_cent'] = False
        return s

    def publish(s):
        result = ""
        s['tricky_buffer_num'] += " " + str(s['multiplied_val'] + s['num']) if s['num'] is not None else ""
        if not s['processing_number']:
            result = s['tricky_buffer_num'].strip()
            s['tricky_buffer_num'] = ""
            s['tricky_buffer'] = ""
        s['may_see_digit'] = True
        s['may_see_decimal'] = True
        s['may_see_multiplier'] = True
        s['may_see_cent'] = True
        s['num'] = None
        s['multiplied_val'] = 0
        s['done_processing_fraction'] = False
        return result, s

    text = text.split(" ")
    result = []
    for i, word in enumerate(text):
        is_number = False
        if word in digits:
            if s['may_see_digit']:
                s['may_see_digit'] = False
                s['may_see_multiplier'] = True
                s['may_see_cent'] = True
                s['may_see_decimal'] = False
            else:
                r, s = publish(s)
                result.append(r)
                s['may_see_digit'] = False
                s['may_see_decimal'] = False
            num, continuing = digits[word]
            if word in ["нэг", "хоёр"]:
                if i < len(text) - 1 and text[i + 1] in stopper_powero_tens + "зуун" and mode != "fr":
                    continuing = True
                elif i != 0 and i < len(text) - 1 and text[i - 1] in everything and text[i + 1] not in everything:
                    continuing = False
                elif i < len(text) - 2 and text[i + 1] in stopper_powero_tens and text[i + 2] in ["-ын",
                                                                                                  "-ны"] and mode == "fr":
                    continuing = False
            elif word in ["нэгэн"]:
                if i < len(text) - 1 and text[i + 1] in multiplier:
                    continuing = True
            if s['num'] is not None:
                s['num'] += num
            else:
                s['num'] = num
            is_number = True
            if not continuing:
                s = stop(s)
        if word in multiplier:
            if s['may_see_multiplier']:
                if mode == "fr" and i < len(text) - 2 and text[i + 2] in ["-ны", "-ний"]:
                    s = stop(s)
                else:
                    s['may_see_decimal'] = True
                    s['may_see_digit'] = True
                    s['may_see_multiplier'] = False
                    s['may_see_cent'] = True
            else:
                r, s = publish(s)
                result.append(r)
                s['may_see_multiplier'] = False
            num, continuing = multiplier[word]
            if s['num'] is not None:
                s['multiplied_val'] += max(s['num'], 1) * num
            else:
                s['multiplied_val'] += 1 * num
            s['num'] = 0
            is_number = True
            if not continuing:
                s = stop(s)
        if word in decimals:
            if s['may_see_decimal']:
                s['may_see_decimal'] = False
                s['may_see_digit'] = True
                s['may_see_multiplier'] = True
                s['may_see_cent'] = True
            else:
                r, s = publish(s)
                result.append(r)
                s['may_see_decimal'] = False
            num, continuing = decimals[word]

            if i < len(text) - 1 and text[i + 1] in ["зуу"]:
                continuing = False

            if s['num'] is not None:
                s['num'] += num
            else:
                s['num'] = num
            is_number = True
            if not continuing:
                s = stop(s)
        if word in centier:
            if s['may_see_cent']:
                if mode == "fr" and i < len(text) - 2 and text[i + 2] in ["-ны", "-ний"]:
                    s = stop(s)
                else:
                    s['may_see_cent'] = False
                    s['may_see_decimal'] = True
                    s['may_see_multiplier'] = True
            else:
                r, s = publish(s)
                result.append(r)
                s['may_see_cent'] = False
            num, continuing = centier[word]
            if not s['may_see_digit'] and not s['may_see_decimal'] and not s['may_see_multiplier'] and not s[
                'may_see_cent']:
                if s["num"] != "" and s["num"] != None and s["num"] != 0:
                    s["num"] *= num
                else:
                    s['num'] = num
            elif not s['may_see_digit']:
                if s['num'] is not None:
                    s['num'] *= num
                else:
                    s['num'] = 0
            else:
                if s['num'] is not None:
                    s['num'] += num
                else:
                    s['num'] = num
            s['may_see_digit'] = True
            is_number = True
            if not continuing:
                s = stop(s)
        if is_number:
            if not s['processing_number']:
                s['tricky_buffer'] = ""
            s['processing_number'] = True
            s['tricky_buffer'] += " " + word
        else:
            if s['processing_number']:
                s['processing_number'] = False
                r, s = publish(s)
                result.append(r)
            result.append(word)
    if s['processing_number']:
        s['processing_number'] = False
        r, s = publish(s)
        result.append(r)

    result = " ".join(result)
    result = re.sub(r"[ ]+", " ", result.replace("|", " ").replace(" -", "-")).strip()

    # region format fractions
    for match in re.findall(r'([0-9]+)( бүхэл | )([0-9]+|зуу)(-ны|-ний|-ын)( [0-9]+)', result):
        dec = 0 if len(match[0]) == 0 else int(match[0])
        if match[2] == "зуу":
            div = 100
        else:
            div = int(match[2])
        frac = int(match[4])
        if div > frac and div in [10, 100, 1000, 10000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]:
            number = dec + (frac / div)
            len_div = len(str(div))
            number = f"{number:.{len_div}f}".rstrip("0").replace(".", ",")
            result = result.replace("".join(match), f"{number}".rstrip("0"))
        elif div not in [10, 100, 1000, 10000, 10000, 100000, 1000000]:
            number = dec + (frac / div)
            len_div = len(str(div))
            number = f"{number:.{len_div}f}".rstrip("0").replace(".", ",")
            result = result.replace("".join(match), f"{number}".rstrip("0"))
    # endregion

    an_match = re.search(r"(ан|өн|эн|он)$", text[-1])
    if an_match and len(result.split()) > 0 and re.search(r"[0-9]", result.split()[-1]):
        result += "-" + an_match[0]

    return result, local_encodings


def validate_and_normalize(text):
    encodings = []
    for i, r in enumerate(number_validators):
        mode = "fr" if i == 0 else "nm"
        matches = list(re.finditer(r, text))
        for m in matches[::-1]:
            normalized, local_enc = normalize_numbers(m.group(), mode)
            encodings.append(local_enc)
            text = text[:m.start()] + " " + normalized + " " + text[m.end():]
    return text, encodings


def handle_numbers(text):
    text, encodings = encode_special_cases(text, cases_to_keep) # replace words to keep with unique ids
    text = inject_one_before_lone_multiplier(text) # insert 'нэг' before multipliers that have no quantifier before it. Ex: 'мянга таван зуу' ==> '1 мянга таван зуу'

    text, local_encodings = validate_and_normalize(text) # normalize
    global_encodings = local_encodings + [encodings]
    text = decode_special_cases(text, global_encodings) # replace unique ids with kept words
    text = re.sub(r"[ ]+", " ", text)

    text = manual_fixer(text) # fixes that are cannot be done automatically

    # region concat numbers of more than 4 groups. Ex: "99 11 22 33" ==> "99112233"
    new_result = ""
    buffer = []
    split_text = text.strip().split()
    for i, word in enumerate(split_text):
        if word.isdigit():
            buffer.append(word)
        elif re.search(r"^[0-9]+", word) and (
                i == len(split_text) - 1 or (i < len(split_text) - 1 and not re.search(r"^[0-9]+", split_text[i + 1]))):
            buffer.append(word)
        else:
            if len(buffer) >= 4:
                new_result += " " + "".join(buffer) + " " + word
            else:
                new_result += " " + " ".join(buffer) + " " + word
            buffer = []
    if len(buffer) >= 4 and sum([int(len(re.search(r"^[0-9]+",b).group()) > 4) for b in buffer]) < 1:
        new_result += " " + "".join(buffer)
    else:
        new_result += " " + " ".join(buffer)
    # endregion

    new_result = re.sub(r"[ ]+", " ", new_result)
    new_result = new_result.strip()
    return new_result
