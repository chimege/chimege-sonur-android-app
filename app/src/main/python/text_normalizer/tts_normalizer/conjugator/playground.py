import ast
import argparse
import requests
from conjugator import Conjugator


parser = argparse.ArgumentParser()
parser.add_argument('--json', help='json file path')
args = parser.parse_args()
if args.json is None:
    raise argparse.ArgumentTypeError('Provide json file name with --json')
json_file = args.json

conjugator = Conjugator(json_file) #verb_conj.json

test_words =  ["метр", "куртка"] 

for word in test_words:
    response = ""
    conj = conjugator.form_conjugations(word, "N-hariyalah")[0]
    x = requests.post("http://localhost:8080/check", data=conj.encode("utf-8"))
    if len(x.text) > 0:
        response = ast.literal_eval(x.text.strip().strip("[]").replace("false", "False").replace("true", "True"))["is_correct"]
    print(conj, response)

# эмх
