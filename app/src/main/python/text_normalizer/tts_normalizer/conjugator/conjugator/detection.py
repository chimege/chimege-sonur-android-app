import re

def detect_word_gender(word):
    feminine_vowels = re.findall('[эөүею]', word)
    masculine_vowels = re.findall('[аоуяё]', word)
    neutral_vowel_count = word.count("и")
    if len(masculine_vowels) >= len(feminine_vowels):
        if len(masculine_vowels) == 0 and neutral_vowel_count > 0:
            return "feminine"
        return "masculine"
    else:
        return "feminine"


def count_syllables(word):
    word_vowels = re.findall("([ыаэоүөуи])", word)
    urt = re.findall("([аэоүөу][аэоүөу])", word)
    syllables_count = len(word_vowels) - len(urt)
    return syllables_count


def get_last_syllable(word, categories):
    vowels = categories["vowels"]["all"] + categories["vowels"]["y_vowels"]
    count = count_syllables(word)
    last_vowel = -1
    for i, letter in enumerate(range(len(word)-1, 0, -1)):
        if word[letter] in vowels:
            last_vowel = i
            if word[-i+1] in vowels:
                last_vowel = i + 1
            break
    return word[-last_vowel - 1:]

# def split_into_syllables(word):
#     count = count_syllables(word)
#     if count < 2:
#         return [word]
#     else:
#         last_vowel = 0
#         for i, letter in enumerate(range(len(word)-1, 0, -1)):
#             if letter in vowels:
#                 last_vowel = i
#                 if word[-i+1] in vowels:
#                     last_vowel = i + 1
#                 break
#         print(word[-last_vowel + 1:])
#         return word[-last_vowel + 1:]

def detect_dominating_vowel(word, categories, word_lists, is_foreign):
    all_vowels = []
    if is_foreign:
        if word in word_lists["foreign_odd_words"]:
            return "a"
        last_syl = get_last_syllable(word, categories)
        
        if last_syl[-1] == "и":
            last_syl = get_last_syllable(word[:-1], categories)
            # word = get_last_syllable(word, categories)
        all_vowels = re.findall('[аэиоөуүяеёю]', last_syl)

        vowels_without_duplicate = list(set(re.findall('[аэиоөуүяеёю]', last_syl)))
        if len(vowels_without_duplicate) == 1 and vowels_without_duplicate[0] == "у":
            without_duplicate = list(set(re.findall('[аэиоөуүяеёю]', word)))
            if len(without_duplicate) == 1:
                return "e"
            else:
                without_duplicate.remove("у")
                word = word.replace("у", "")
                all_vowels = without_duplicate

    else:
        all_vowels = re.findall('[аэиоөуүяеёю]', word)

    if detect_word_gender(word) == "feminine":
        if len(all_vowels) == 1 and "е" in all_vowels:
            if is_foreign:
                return "e"
            else:
                return "u"
        if "э" not in all_vowels and "ө" in all_vowels: 
            return "u"
        else:
            return "e"
    else:
        if "а" not in all_vowels and "о" in all_vowels:
            if "у" in all_vowels:
                return "a"
            else:
                return "o"
        else:
            return "a"


def detect_pad_vowel(word):
    if word.endswith(("ж", "ч", "ш")):
        return "и"
    all_vowels = re.findall('[аэиоөуү]', word)
    if detect_word_gender(word) == "feminine":
        if "э" not in all_vowels and "ө" in all_vowels:
            return "ө"
        else:
            if word.endswith("с"):
                return "ө"
            else:
                return "э"
    else:
        if "а" not in all_vowels and "о" in all_vowels:
            if "у" in all_vowels:
                return "а"
            else:
                return "о"
        else:
            return "а"


def has_vowels(text, vowels):
    for char in text:
        if char in vowels:
            return True
    return False


def provides_condition(word, sp_obj, categories, word_lists, is_foreign):
    gliding_vowels = categories["vowels"]["gliding"]
    long_vowels = categories["vowels"]["long"]
    provides_end, provides_cond = False, False
    n_word, end = False, False

    if len(sp_obj["after"]) > 0 or "word_lists" in sp_obj.keys():
        endings = sp_obj["after"]
        if True in [word.endswith(ending) for ending in endings]:
            end = True
        if end:
            provides_end = True    
        if "word_lists" in sp_obj.keys():
            word_list = []
            for l in sp_obj["word_lists"]:
                word_list += word_lists[l]
            if word in word_list:
                provides_end = True
        
            
    else:
        provides_end = True

    if "conditions" in sp_obj and len(sp_obj["conditions"]) > 0:
        # some special suffixes have multiple different condition strings :)
        # ["syllables=1&vowels=long", "syllables=2"]
        for cond_str in sp_obj["conditions"]:
            # and the condition strings can have multiple conditions that have
            # to be provided at the same time seperated by "&" sign like url paramters
            conds = cond_str.split("&")
            cond_bools = []
            for cond in conds:
                key = cond.split("=")[0]
                cond = cond.split("=")[1]
                if key == "syllables":
                    if count_syllables(word) == cond[0]:
                        cond_bools.append(True)
                elif key == "vowels":
                    if key == "gliding_or_long":
                        if len(word) > 3 and word[-3:-1] in gliding_vowels or word[-3:-1] in long_vowels:
                            cond_bools.append(True)
                elif key == "is_foreign" and is_foreign:
                    cond_bools.append(True)
            if len(cond_bools) > 0 and False not in cond_bools:
                provides_cond = True
                break
    else:
        provides_cond = True
    return provides_end and provides_cond
