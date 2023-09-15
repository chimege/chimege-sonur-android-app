import re


def exclude_condition(exclusion, source):
    new_condition = re.sub(exclusion, r"", source)
    new_condition = re.sub(r"(\|+)", r"|", new_condition)
    new_condition = re.sub(r"(^\||\|$)", r"", new_condition)
    return new_condition


# region For number chunk validating ([ерэн ес] [арван нэг] [хорин хоёр] [гучин зургаа] [арван нэг зууны гурван зуун хорин хоёр])
connectors = 'нэг|хоёр|нэгэн|хоёрон|гурван|дөрвөн|таван|зургаан|долоон|найман|есөн|арван|хорин|гучин|дөчин|тавин|жаран|далан|наян|ерөн|ерэн|зуун|мянга|сая|тэрбум'
connector_digits = 'нэгэн|хоёрон|гурван|дөрвөн|таван|зургаан|долоон|найман|есөн'
connector_decimal = 'арван|хорин|гучин|дөчин|тавин|жаран|далан|наян|ерөн|ерэн'
fraction_connector = 'арваны|аравны|зууны|мянганы|саяны|саяын|тэрбумны|тэрбумын'

stoppers = 'нойл|ноль|тэг|нэг|хоёр|гурав|дөрөв|тав|зургаа|долоо|найм|ес|арав|хорь|гуч|дөч|тавь|жар|дал|ная|ер|зуу|мянга|сая|тэрбум'
stopper_digits = 'нойл|ноль|тэг|нэг|хоёр|гурав|дөрөв|тав|зургаа|долоо|найм|ес'
stopper_decimals = 'арав|хорь|гуч|дөч|тавь|жар|дал|ная|ер'
stopper_powero_tens = 'зуу|мянга|сая|тэрбум'
special_stoppers = 'хоё|гурв|дөрв|арва|хори|мянг|арв|дол|зург|хоёроны|гурваны|дөрвөний|долооны|хорийн|хориор|хориод|хориос|наяад|наяар|наяас|тавиад|тавиар|тавиас|тавинаас|долоогоороо|зургаагаараа'

number_suffix_reg = 'ан|өн|эн|он|ний|ны|ын|гийн|ийг|ийн|ыг|онд|анд|өнд|энд|инд|нд|ид|ин|н|д|аас|наас|нээс|ээс|ас|ос|ноос|оос|өөс|нөөс|наар|аар|нээр|ээр|нөөр|өөр|ноор|оор|г|т|тай|тэй|той|рүү|руу|уул|ул|үүл|даа|улаа|уулаа|үүлээ|улаа|дугаар|дүгээр|гаар|гоор|гаас|гоос|дугаарт|дүгээрт|тэйгээ|тайгаа|аараа|ээрээ|оороо|өөд|аад|ээд|хан|хэн|хөн|хон'
# endregion

multiplier_prohibiters = stopper_digits + "|" + stopper_decimals + "|" + connector_decimal + "|" + connector_digits + "|зуу|зуун"

# for inserting percentage sign, and accompanying suffixes
percentage = [("хувь", "%"), ("хувийн", "%-ийн"), ("хувийг", "%-ийг"), ("хувиас", "%-аас"), ("хувиар", "%-аар"),
              ("хувьтай", "%-тай"), ("хувиа", "%-аа")]

# for abbreviating metrics that goes after numbers
number_tailers = [("метр квадрат", "м2"), ("метр куб", "м3"), ("грамм", "гр"), ("центнер", "ц"),
                  ("килограмм", "кг"), ("километр", "км"), ("миллиметр", "мм"), ("сантиметр", "см"),
                  ("миллиграмм", "мг"), ("миллилитр", "мл"), ("киловатт", "квт"), ("мегаватт", "мвт"),
                  ("дециметр куб", "дм3"), ("дециметр квадрат", "дм2"), ("дециметр", "дм"),
                  ("америк доллар", "ам.доллар")]

# to keep -иад ending repeated 10, 20, 30, ... 90 numbers. Ex: арав хориод
iad_ending_numbers = "арваад|хориод|гучаад|дөчөөд|тавиад|жараад|далаад|наяад|ерээд|зуугаад"
# to keep хоёул гурвуул, хоёр гурваараа as numbers
uul_aaraa_ending_number_roots = "хоёул|гурвуул|дөрвүүл|тавуул|зургуул|долуул|наймуул|есүүл|арвуул|хоёроороо|гурваараа|дөрвөөрөө|таваараа|зургаагаараа|долоогоороо|наймаараа|есөөрөө|арваараа"

everything = stoppers + "|" + connectors + "|их наяд|" + "|".join([t[0] for t in number_tailers])

# for prohibiting fractions to not end with power of tens + hariyalah. Without this limitation, it would split "долоо аравны зургаан сая нэг арваны таван тэрбум гурав арваны таван" to ["долоо аравны зургаан сая нэг арваны","таван тэрбум гурав арваны таван"]
everything_wo_ptens = exclude_condition(r"\b(арав|арван|зуу|мянга|сая|тэрбум)\b", everything)
suffix_wo_hariyalah = exclude_condition(r"\b(ний|ны)\b", number_suffix_reg)

everything_wo_tsnd_mil_bil = exclude_condition(r"\b(мянга|сая|тэрбум)\b", everything)

everything_negative_lookbehind = ''.join([f'(?<!{d})' for d in everything.split('|')])

# Cases to keep as words. (case pattern, match group id to decode into)
cases_to_keep = [
    [rf"{everything_negative_lookbehind}([ ]+|^)(дал[^ ]*)\b(?![ ]+({everything + '|' + special_stoppers}))(?![ ]+(хувь|хуви)[^ ]*\b)", 2], # keep 'дал' with no numbers around it as word
    [rf"{everything_negative_lookbehind}(?<!ны)(?<!ний)(?<!ын)(?<!ийн)([ ]+|^)(зургаа)\b(?!([ ]+({everything})))", 2], # keep 'зургаа' with no numbers around it
    [rf"({iad_ending_numbers})([ ]+|^])({iad_ending_numbers})", 2], # keep '-иад' ending repeated numbers as words. Ex: хориод гучаад
    [rf"{everything_negative_lookbehind}([ ]+|^)({iad_ending_numbers})\b", 2], # keep '-иад' ending numbers with no number in front
    [rf"{everything_negative_lookbehind}([ ]+|^)({uul_aaraa_ending_number_roots}|{stopper_digits.replace('нойл|ноль|тэг|', '')}|)([ ]+|)(({uul_aaraa_ending_number_roots})(аа|ээ|))\b", [2, 4]], # keep '-уул', '-аараа' ending repeating numbers
    [rf"(({everything + '|' + uul_aaraa_ending_number_roots})[ ]+){2, 4}(({uul_aaraa_ending_number_roots})(аа|ээ|))", 3], # keep 'хоёр гурав дөрвүүлээ'
    [rf"(({everything_negative_lookbehind})[ ]+|^)\b(ер)\b(?![ ]+({everything}))", 3], # keep 'ер' with no numbers around it
    [rf"(([а-яөүё]+)[ ]+|^)(?<!сарын )\b((нэг)(?!(дүгээр|дүгээрт|т))([а-яөүё]*))\b(?![ ]+({everything}|сарын|дүгээр))",
     9999], # keep 'нэг' that is not in date
    [rf"\b({everything_negative_lookbehind}(?<!сарын)( |^)(нэгэн)\b)(?!([ ]+({everything_wo_tsnd_mil_bil})))", 3], # keep 'нэгэн' that is not in date
    [rf"\b(их наяд)\b", 1],
    [rf"\b(тэгээд)\b", 1],
    [rf"\b(хориг)\b", 1],
    [rf"\bач[ ]+(гуч[^ ]*)\b", 1], # keep 'ач гуч'
    [rf"\b((тав)(гаар|тай))\b", 1], # keep 'тавгаар', 'тавтай'
    [rf"(дугаар|дүгээр) (зуунаас)\b", 2], # keep 'дугаар зуунаас'
    [rf"((({everything_negative_lookbehind})[ ]+|^)\b(((зуу|мянга|сая|тэрбум)[ ]+)+)(\5))\b(?![ ]+({everything}))", 1], # keep 'зуу зуу' or 'мянга мянга' or so on
    [rf"((({everything_negative_lookbehind})[ ]+|^)\b(зуу )+(зуу[а-яөүё]*))\b(?![ ]+({everything}))", 1], # keep 'зуу зуун' or 'зуу зуугаар' or so on
    [
        rf"(({everything_negative_lookbehind})[ ]+|^)\b(зуун зуун)\b(?![ ]+({everything.replace('|мянга|сая|тэрбум', '')}))",
        3], # keep 'зуун зуун' that has no numbers around it, except leading 'мянга', 'сая', 'тэрбум'
    [rf"(({everything_negative_lookbehind})[ ]+|^)\b(зууны)\b(?![ ]+({everything.replace('|мянга|сая|тэрбум', '')}))",
     3], # keep 'зууны' that has no numbers around it, except leading 'мянга', 'сая', 'тэрбум'
    [rf"((({everything_negative_lookbehind})[ ]+|^)\b(мянга )+(мянга))\b(?![ ]+({everything}))", 1], # keep repeating 'мянга'-s that has no numbers around it
    [rf"((({everything_negative_lookbehind})[ ]+|^)\b(сая )+(сая))\b(?![ ]+({everything}))", 1], # keep repeating 'сая'-s that has no numbers around it
    [rf"((({everything_negative_lookbehind})[ ]+|^)\b(тэрбум )+(тэрбум))\b(?![ ]+({everything}))", 1], # keep repeating 'тэрбум'-s that has no numbers around it
    [rf"((({everything_negative_lookbehind})[ ]+|^)\b(тэг))\b(?![ ]+({everything}))", 1], # keep 'тэг' that has no numbers around it
    [
        rf"\b((({everything})[ ]+){0, 4}(тэрбум) (({everything})[ ]+){0, 4}(сая([^ ]*|$)) (({everything})[ ]+){0, 4}(мянг([^ ]*|$)))\b(?![ ]+({everything}))",
        [4, 7, 11]], # keep 'тэрбум', 'сая', 'мянга' in numbers that has no numbers less than a thousand. Ex: 'хоёр тэрбум гурван зуун хорин долоон сая дөрвөн зуун хорин мянга' ==> '2 тэрбум 327 сая 420 мянга'. 'сая' is optional
    [rf"\b((({everything})[ ]+){0, 4}(тэрбум) (({everything})[ ]+){0, 4}(сая([^ ]*|$)))\b(?![ ]+({everything}))",
     [4, 7]], # keep 'тэрбум', 'сая' in numbers that has no numbers less than a thousand.
    [rf"\b((({everything})[ ]+){0, 4}(сая) (({everything})[ ]+){0, 4}(мянг([^ ]*|$)))\b(?![ ]+({everything}))", [4, 7]], # keep 'сая', 'мянг.*' in numbers that has no numbers less than a thousand.
    [rf"\b(мянга([^ ]*|$))\b(?!([ ]+({everything_wo_tsnd_mil_bil}|мянга|он)))", 1], # keep 'мянга' that has no numbers behind it except 'мянга' or 'он'
    [rf"(зуун[ ]+)\b(мянга)\b([ ]+({multiplier_prohibiters})\b){0, 2}(?![ ]+({everything}))", 2], # keep 'мянга' that has 'зуун' in front of it and very small number behind. Ex: 'таван зуун мянга нэг' ==> '500 мянга 1'
    [rf"\b(сая([^ ]*|$))\b(?![ ]+({everything_wo_tsnd_mil_bil}|сая))", 1], # # keep 'мянга' that has no numbers behind it except 'сая'
    [rf"\b(сая)\b([ ]+({multiplier_prohibiters})\b){0, 2}(?![ ]+({everything}))", 1], # keep 'сая' that has very small number behind. Ex: 'сая долоо' ==> 'сая 7'
    [
        rf"\b({everything_negative_lookbehind}(?<!^)([ ]+|^)(сая([^ ]*|$)))\b(?!(({everything_wo_tsnd_mil_bil})))",
        3], # keep 'сая' that has no numbers around it
    [rf"\b(тэрбум([^ ]*|$))\b(?!([ ]+({everything_wo_tsnd_mil_bil}|тэрбум)))", 1], # keep 'тэрбум.*' that has no numbers around it.
    [rf"\b(тэрбум)\b([ ]+({multiplier_prohibiters})\b){0, 2}(?![ ]+({everything}))", 1], # keep 'тэрбум' that has no numbers in front of it and very small number behind it.
    [rf"\b(зург(аас|аар|ийн|ийг)[^ ]*)", 1], # keep 'зургаас' etc.
    [rf"\b(ганц нэг)\b", 1], # keep 'ганц нэг'
    [rf"\b(таваг)\b", 1], # keep 'таваг'
    [rf"\b(гурван)[ ]+(тэс|тамир)\b", 1], # keep 'гурван тэс', 'гурван тамир'
    [rf"\b(гучин)[ ]+ус\b", 1] # keep 'гучин ус'
]

cases_to_keep = [[c[0].replace("(0, 4)", "{0,4}").replace("(0, 2)", "{0,2}").replace("(2, 4)", "{2,4}").replace("(2, 2)", "{2}"), c[1]] for c in cases_to_keep]

slip_one_before_lone_multipliers = rf"\b{''.join([f'(?<!{m}[ ])' for m in (stopper_digits + '|' + connector_digits + '|' + connector_decimal + '|зуун').split('|')])}(зуун|мянга|сая|тэрбум)\b(?![ ]+[a-zA-Z])"
# cases to keep after number validation
local_cases = [
    [rf"(.*(хан|хэн|хөн|хон))", 1],
    [rf'''\b(сая([^ ]*|$))\b(?![ ]+({everything_wo_tsnd_mil_bil}|сая))''', 1],
    [rf"\b(тэрбум([^ ]*|$))\b(?!([ ]+({everything_wo_tsnd_mil_bil}|тэрбум)))", 1],
    [rf"\b(мянга([^ ]*|$))\b(?!([ ]+({everything_wo_tsnd_mil_bil}|мянга|он)))", 1],
]

# validate numbers and split them to process clearly. Ex: 'арван гурван сая дөрвөн сая дөчин тэрбум' ==> ['арван гурван сая', 'дөрвөн сая', 'дөчин тэрбум']
# it declares some sort of rules for numbers like, words after a certain multiplier (аравт, зуут, мянгат ...) should be greater than current.
number_validators = [
    fr'''
    \b(
        (
            (
                ({connectors})[ ]+
            )*
            (({stoppers})|((нэгэн|{connectors})[ ]+бүхэл))|
        )
        (
            ([ ]+|^)
            (({fraction_connector})|((арван|зуун)[ ]+(мянганы|саяны|саяын|тэрбумны|тэрбумын)))[ ]+
        )
        (({connectors.replace("нэг|хоёр|", "")})[ ]+)*
        (
            ((нэг|хоёр)([ ]+зуун[ ]+({connector_decimal}|)[ ]*(нэг|хоёр|гурав|дөрөв|тав|зургаа|долоо|найм|ес|хоё|гурв|дөрв|дол|зург|хоёроны|гурваны|дөрвөний)({suffix_wo_hariyalah}|)))|
            ((нэг|хоёр)([ ]+(зуу|мянга|сая|тэрбум)|))|
            ({everything_wo_ptens} + '|' + {special_stoppers})({suffix_wo_hariyalah}|)|
            (арав|арван|зуу|мянга|сая|тэрбум)
        )
        (?!([ ]+({fraction_connector})))
    )\b''', # validator for fractions
    fr'''(\b
    (
        (({connectors.replace('|мянга|сая|тэрбум', '')})[ ]+)*(тэрбум)
    )
    (
        ([ ]+({connectors.replace('|мянга|сая|тэрбум', '')})){0, 4}([ ]+сая)|
    )
    (
        ([ ]+({connectors.replace('|мянга|сая|тэрбум', '')})){0, 4}([ ]+мянга)|
    )
    (
        ([ ]+({connectors.replace('|зуун|мянга|сая|тэрбум', '')})){0, 1}([ ]+зуун)|
    )
    (
        ([ ]+({connectors.replace('|зуун|мянга|сая|тэрбум', '')})){0, 1}
        ([ ]+({stoppers.replace('|мянга|сая|тэрбум', '') + '|' + special_stoppers})({number_suffix_reg}|))|
    )\b)
    (?![ ]+(тэрбум))
    (?![ ]+[A-Za-z])''', # validator for biggest numbers that include 'тэрбум', 'сая'*, 'мянга'*, 'зуун'*, 'аравт'*, 'нэгж'* (*-are optional)

    fr'''(\b
    (
        (({connectors.replace('|мянга|сая|тэрбум', '')})[ ]+)*(сая[ ]+)
    )
    (
        (({connectors.replace('|мянга|сая|тэрбум', '')})[ ]+){0, 4}(мянга[ ]+)|
    )
    (
        (({connectors.replace('|зуун|мянга|сая|тэрбум', '')})[ ]+){0, 1}(зуун[ ]+)|
    )
    (
        (({connectors.replace('|зуун|мянга|сая|тэрбум', '')})[ ]+){0, 1}
        ({stoppers.replace('|сая|тэрбум', '') + '|' + special_stoppers})({number_suffix_reg}|)|
    )\b)
    (?![ ]+(сая|тэрбум))
    (?![ ]+[A-Za-z])''', # validator for numbers that include 'сая', 'мянга'*, 'зуун'*, 'аравт'*, 'нэгж'* (*-are optional)

    fr'''(\b
    (
        (({connectors.replace('|мянга|сая|тэрбум', '')})[ ]+)*(мянга[ ]+)
    )
    (
        (({connectors.replace('|зуун|мянга|сая|тэрбум', '')})[ ]+){0, 1}
        (зуун[ ]+)|
    )
    (
        (({connectors.replace('|зуун|мянга|сая|тэрбум', '')})[ ]+)*
        (({stoppers.replace('|мянга|сая|тэрбум', '') + '|' + special_stoppers})({number_suffix_reg}|))|
    )\b)
    (?![ ]+(мянга|сая|тэрбум))
    (?![ ]+[A-Za-z])''', # validator for numbers that include 'мянга', 'зуун'*, 'аравт'*, 'нэгж'* (*-are optional)

    fr'''(\b
    (?<!зуун )
    (({connector_decimal})[ ]+)
    (
        ({stopper_digits + '|' + special_stoppers.replace('арва|хори|мянг|арв|', '') + '|' + connector_digits}|хоёроны)
        ({number_suffix_reg}|)
    )
    \b)''', # validator for numbers that include 'зуун', 'аравт'*, 'нэгж'* (*-are optional)

    fr'''(\b
    (
        (
            ([ ]+|)({connectors.replace('|арван|хорин|гучин|дөчин|тавин|жаран|далан|наян|ерөн|ерэн|зуун|мянга|сая|тэрбум', '')})[ ]+
        ){0, 1}(зуун)
    )
    (
        ([ ]+({connectors.replace('|зуун|мянга|сая|тэрбум', '')})){0, 1}
        ([ ]+({stoppers.replace('|зуу|мянга|сая|тэрбум', '') + '|' + special_stoppers})({number_suffix_reg}|)|)|
    )\b)''', # validator for numbers that include 'X зуун', 'аравт'*, 'нэгж'* (*-are optional)
    fr'''(\b
    (
        (
            ([ ]+|)({connectors.replace('|арван|хорин|гучин|дөчин|тавин|жаран|далан|наян|ерөн|ерэн|зуун|мянга|сая|тэрбум', '')})[ ]+
        ){0, 4}(мянган)
    )
    (
        ([ ]+({connectors.replace('|зуун|мянга|сая|тэрбум', '')})){0, 1}
        ([ ]+({stoppers.replace('|зуу|мянга|сая|тэрбум', '') + '|' + special_stoppers})({number_suffix_reg}|)|)|
    )\b([ ]+он[а-яөүё]{0, 4}|)\b)''', # validator for numbers that include 'X мянган', 'аравт'*, 'нэгж'* (*-are optional)
    fr'''(\b
    (
        ({connectors.replace('|арван|хорин|гучин|дөчин|тавин|жаран|далан|наян|ерөн|ерэн|зуун|мянга|сая|тэрбум', '')})[ ]+){0, 4}
        ((зуу)({number_suffix_reg.replace('|н|', '|')}|)
    )\b)''', # validator for numbers that include 'X* зуу'
    fr'''(\b({stopper_decimals}|арва|арв|хори|хорийн)({number_suffix_reg}|)\b)''', # validator for numbers that include 'аравт', 'нэгж'* (*-are optional)
    fr'''(\b({stopper_digits + '|' + special_stoppers.replace('арва|хори|мянг|арв|', '')})({number_suffix_reg}|)\b)''', # validator for numbers that include 'аравт'*, 'нэгж'* (*-are optional)
]

number_validators = [
    n.replace("\n", "").replace("    ", "").replace("(0, 4)", "{0,4}").replace("(0, 3)", "{0,3}").replace("(0, 1)",
                                                                                                          "{0,1}") for n
    in number_validators]

relative_period_keywords = "өнөөдөр|маргааш|нөгөөдөр|өчигдөр|уржигдар|өглөө|орой|үд дунд|үдээс хойш|үдээс өмнө|өдөр|шөнө|үүрээр|оройн"
relative_period_keywords_w_suffix = "өнөөдр|маргааш|нөгөөдр|өчигдр|уржигдр|өглөө|орой|үд дунд|өдр|шөн|үүр"
# to convert time with format. The numbers should be surrounded with context words. Ex: 'маргааш таван цаг гучин минутад' ==> "маргааш 5:30-д"
time_catchers = [
    [rf"\b({relative_period_keywords})[ ]+([0-9]{1, 2})[ ]+([0-9]{1, 2})(-([^ ]+)|)\b", [2, 3]],
    [rf"\b({relative_period_keywords_w_suffix})(ийн|ын|ний|ны)[ ]+([0-9]{1, 2})[ ]+([0-9]{1, 2})(-([^ ]+)|)\b", [3, 4]],
    [rf"\bсарын[ ]+[0-9]{1, 2}[ ]+-(нд|ны|ний)[ ]+(өдөр[ ]+|өдрийн[ ]+|)([0-9]{1, 2})[ ]+([0-9]{1, 2})(-д|-т)", [3, 4]]
]

time_catchers = [[p[0].replace("(1, 2)", "{1,2}"), p[1]] for p in time_catchers]

manual_suffix_fix = [
    ("хорийн", "хорь -ийн"),
    ("хориор", "хорь -оор"),
    ("хориод", "хорь -оод"),
    ("хориос", "хорь -оос"),
    ("наяад", "ная -аад"),
    ("наяар", "ная -аар"),
    ("наяас", "ная -аас"),
    ("тав -ийн", "тавь -ийн"),
    ("тавиад", "тавь -аад"),
    ("тавиар", "тавь -аар"),
    ("тавиас", "тавь -аас"),
    ("тавинаас", "тавь -наас"),
    ("долоогоороо", "долоо -оороо"),
    ("зургаагаараа", "зургаа -аараа")
]
