import ast
import requests
from src.conjugator import Conjugator
from src.detection import detect_word_gender, detect_dominating_vowel, count_syllables

with open("o_excluded.pkl", "rb") as pickle_file:
    words = pickle.load(pickle_file)

conjugator = Conjugator("json/noun_conj.json")
cats = conjugator.categories
vowels = cats["vowels"]["all"]
long_vowels = cats["vowels"]["long"]
gliding_vowels = cats["vowels"]["gliding"]
y_vowels = cats["vowels"]["y_vowels"]
vocalized = cats["consonants"]["vocalized"]
non_vocalized = cats["consonants"]["nonvocalized"]
endings = ["single_vowel", "gliding_vowel", "long_vowel", "y_vowel", "vocalized", "non_vocalized"]

one_syllable = {"single_vowel": [], "long_vowel": [], "gliding_vowel": [], "y_vowel": [], "vocalized": [], "non_vocalized": [], "rest": []}
more_syllables = {"single_vowel": [], "long_vowel": [], "gliding_vowel": [], "y_vowel": [], "vocalized": [], "non_vocalized": [], "rest": []}

for word in words:
    if len(word) < 2 or " " in word:
        continue
    x = requests.post("http://localhost:8080/check", data=word.strip().encode("utf-8"))
    if len(x.text) > 0:
        response = ast.literal_eval(x.text.strip().strip("[]").replace("false", "False").replace("true", "True"))["is_correct"]
        if response:
            syllable = count_syllables(word)
            gender = detect_word_gender(word)
            dom_vowel = detect_dominating_vowel(word)
            for end in endings:
                if word.endswith(tuple(vowels)) and word[-2] :
                    if syllable == 1:
                        one_syllable["single_vowel"].append(word)
                    else:
                        more_syllables["single_vowel"].append(word)

                elif word.endswith(tuple(long_vowels)):
                    if syllable == 1:
                        one_syllable["long_vowel"].append(word)
                    else:
                        more_syllables["single_vowel"].append(word)

                elif word.endswith(tuple(gliding_vowels)):
                    if syllable == 1:
                        one_syllable["gliding_vowel"].append(word)
                    else:
                        more_syllables["gliding_vowel"].append(word)

                elif word.endswith(tuple(y_vowels)):
                    if syllable == 1:
                        one_syllable["y_vowel"].append(word)
                    else:
                        more_syllables["y_vowel"].append(word)
                elif word.endswith(tuple(vocalized)):
                    if syllable == 1:
                        one_syllable["vocalized"].append(word)
                    else:
                        more_syllables["vocalized"].append(word)
                elif word.endswith(tuple(non_vocalized)):
                    if syllable == 1:
                        one_syllable["non_vocalized"].append(word)
                    else:
                        more_syllables["non_vocalized"].append(word)
                else:
                    if syllable == 1:
                        one_syllable["rest"].append(word)
                    else:
                        more_syllables["rest"].append(word)


