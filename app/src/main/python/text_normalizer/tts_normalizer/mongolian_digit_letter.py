from conjugator.detection import detect_word_gender

number_words = ['тэг', 'нэг', 'хоёр', 'гурав', 'дөрөв', 'тав', 'зургаа', 'долоо', 'найм', 'ес', "мянга", 'зуу',
                'арав', 'тэрбум', 'сая', 'их наяд', 'тунамал', 'тэг', 'арав', 'хорь', 'гуч', 'дөч', 'тавь', 'жар',
                'дал', 'ная', 'ер']


# Float numbers
def fraction2word(number_str, is_fina=True):
    float_digit_name = {'мянга': 'мянганы', 'зуу': 'зууны', 'арав': 'аравны'}
    number = number_str.replace(".", ",")
    if number.count(',') != 1:
        # invalid number
        return number_str
    parts = number.split(',')
    parts[1] = parts[1].rstrip('0')
    if len(parts[1]) == 0:
        return number2word(parts[0], is_fina)
    result = list()
    result.append(number2word(parts[0], True))
    fraction_pre = '1'
    for x in range(len(parts[1])):
        fraction_pre += '0'

    if len(fraction_pre) < 7:
        pre_part = number2word(fraction_pre, True)
        if ' ' in pre_part:
            part_one, part_two = pre_part.rsplit(' ', 1)
            pre_part = ' '.join([part_one, float_digit_name[part_two]])
        else:
            pre_part = float_digit_name[pre_part]
    else:
        pre_part = 'таслал'
    result.append(pre_part)
    result.append(number2word(parts[1].lstrip('0'), is_fina))
    return ' '.join(result)


def time2word(match):
    hour = _2_digits_2_str(match.group(1), False) + " цаг "
    minute = _2_digits_2_str(match.group(2), False)
    if minute != "тэг" and minute != "тэг тэг" and minute != "":
        minute += " минут"
    else:
        minute = ""
    return hour + minute


# For Integer numbers
def number2word(number, is_fina=True, force_one_two_ending=False):
    digit_name = {1: '', 2: 'мянга', 3: 'сая', 4: 'тэрбум', 5: 'их наяд', 6: 'тунамал'}
    digit_name_k = {1: '', 2: 'мянган'}
    if not number.isdigit():
        return number
    # Check the number consists of only zeros
    if number.strip('0') == '':
        return digit_by_one(number)
    number = number.lstrip('0')
    digit_len = len(number)
    if force_one_two_ending and number in ["1", "2"]:
        return "нэгэн" if number == "1" else "хоёрон"
    if digit_len == 0:
        return ''
    if digit_len == 1:
        return _last_digit_2_str(number) if is_fina else _1_digit_var_2_str(number)
    if digit_len == 2:
        return _2_digits_2_str(number, is_fina)
    if digit_len == 3:
        return _3_digits_to_str(number, is_fina)
    if digit_len < 7:
        preK = _3_digits_to_str(number[:-3], False, preK=True)
        if preK == 'нэг':
            preK = ''
        if number[digit_len - 3:] == '000':
            kname = digit_name[2] if is_fina else digit_name_k[2]
            return (preK + ' ' + kname).strip()
        return (preK + ' ' + digit_name[2] + ' ' + _3_digits_to_str(number[-3:], is_fina)).strip()

    digitgroup = [number[0 if i - 3 < 0 else i - 3:i] for i in reversed(range(len(number), 0, -3))]
    count = len(digitgroup)
    if count > 6:
        return digit_by_one(number)
    i = 0
    result = ''
    while i < count - 1:
        read_one = True if i != 0 else False
        res = _3_digits_to_str(digitgroup[i], False, True, read_one)
        if len(res) > 0:
            result += ' ' + (res + ' ' + digit_name[count - i])
        i += 1
    return (result.strip() + ' ' + _3_digits_to_str(digitgroup[-1], is_fina)).strip()


def digit_by_one(numstr):
    return ' '.join(_last_digit_2_str(ch) for ch in numstr)


def date2word(numstr, range):
    try:
        date_parts = numstr.split('.')
        if len(date_parts) == 4:
            if range:
                return number2word(date_parts[0], False) + ' оны ' + number2word(date_parts[1], False) + ' сарын ' + _day_number2word(date_parts[2]) + "N-GARAH " + _day_number2word(date_parts[3])
        if len(date_parts) == 3:
            if range:
                return number2word(date_parts[0], False) + " сарын " + _day_number2word(
                    date_parts[1]) + "N-GARAH " + _day_number2word(date_parts[2])
            else:
                return number2word(date_parts[0], False) + ' оны ' + number2word(date_parts[1],
                                                                                 False) + ' сарын ' + _day_number2word(
                    date_parts[2])
        if len(date_parts) == 2:
            if range:
                return " сарын " + _day_number2word(date_parts[0]) + "N-GARAH " + _day_number2word(date_parts[1])
            else:
                return number2word(date_parts[0], False) + " сарын " + _day_number2word(date_parts[1])

        return _day_number2word(numstr)
    except KeyError as e:
        return numstr



def _day_number2word(number):
    day_digit = {'1': 'нэгэн', '2': 'хоёрон', '3': 'гурван', '4': 'дөрвөн',
                 '5': 'таван', '6': 'зургаан', '7': 'долоон', '8': 'найман', '9': 'есөн'}
    day_digit2 = {'1': 'арван', '2': 'хорин', '3': 'гучин'}
    if number == "0":
        return ""
    if len(number) == 1 and int(number) > 0:
        return day_digit[number]
    if number[0] == '0':
        return day_digit[number[1]]
    if number[1] == '0':
        return day_digit2[number[0]]
    return (day_digit2[number[0]] + ' ' + day_digit[number[1]]).strip()

def dugaar(number):
    num = number2word(number)
    last_num = num.split()[-1]
    if detect_word_gender(last_num) == "feminine":
        return " дүгээр "
    else:
        return " дугаар "

def _1_digit_2_str(digit):
    return {'0': '', '1': 'нэгэн', '2': 'хоёр', '3': 'гурван', '4': 'дөрвөн', '5': 'таван', '6': 'зургаан',
            '7': 'долоон', '8': 'найман', '9': 'есөн'}[digit]


def _1_digit_var_2_str(digit):
    return {'0': '', '1': 'нэг', '2': 'хоёр', '3': 'гурван', '4': 'дөрвөн', '5': 'таван', '6': 'зургаан',
            '7': 'долоон', '8': 'найман', '9': 'есөн'}[digit]


def _last_digit_2_str(digit):
    return {'0': 'тэг', '1': 'нэг', '2': 'хоёр', '3': 'гурав', '4': 'дөрөв', '5': 'тав', '6': 'зургаа', '7': 'долоо',
            '8': 'найм', '9': 'ес'}[digit]


def _2_digits_2_str(digit, is_fina=True):
    word2 = {'0': '', '1': 'арван', '2': 'хорин', '3': 'гучин', '4': 'дөчин', '5': 'тавин', '6': 'жаран', '7': 'далан',
             '8': 'наян', '9': 'ерэн'}
    word2fina = {'00': 'тэг', '10': 'арав', '20': 'хорь', '30': 'гуч', '40': 'дөч', '50': 'тавь', '60': 'жар',
                 '70': 'дал',
                 '80': 'ная', '90': 'ер'}
    if digit[1] == '0':
        return word2fina[digit] if is_fina else word2[digit[0]]
    digit1 = _last_digit_2_str(digit[1]) if is_fina else _1_digit_2_str(digit[1])
    return (word2[digit[0]] + ' ' + digit1).strip()


def _3_digits_to_str(digit, is_fina=True, preK=False, read_one=False):
    digstr = digit.lstrip('0')
    if len(digstr) == 0:
        return ''
    if len(digstr) == 1:
        if preK:
            return _1_digit_var_2_str(digstr)
        else:
            return _last_digit_2_str(digstr)
    if len(digstr) == 2:
        return _2_digits_2_str(digstr, is_fina)
    if digit[-2:] == '00':
        if (digit[0]) == '1':
            if read_one:
                return 'нэг зуу' if is_fina else 'нэг зуун'
            else:
                return 'зуу' if is_fina else 'зуун'
        return _1_digit_var_2_str(digit[0]) + ' зуу' if is_fina else _1_digit_var_2_str(digit[0]) + ' зуун'
    if digit[0] == '1':
        return 'зуун ' + _2_digits_2_str(digit[-2:], is_fina)
    return _1_digit_var_2_str(digit[0]) + ' зуун ' + _2_digits_2_str(digit[-2:], is_fina)


# defined only for test purpose
if __name__ == '__main__':
    # Tests
    print(fraction2word('79856.00546'))
    print(fraction2word('79856.100546'))
    print(number2word('100'))
    print(number2word('111'))
    print(number2word('543', False))
    print(number2word('5432', False))
    print(number2word('2050'))
    print(fraction2word('12,975'))
    print(fraction2word('100.11'))
    print(fraction2word('1.01'))
    print(fraction2word('1.111'))
