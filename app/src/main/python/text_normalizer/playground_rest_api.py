import os
import json
import requests


def synthesize(text, output_file, voice_id=1):
    url = "https://api.chimege.com/v1.2/synthesize"
    headers = {
        'Content-Type': 'plain/text',
        # orgio token
        'Token': 'b27b45d91c5f32fd663503b11cfc1e6733b971c274fc59b9e7da99e7c83cba57',
        'voice-id': "%d" % voice_id
    }
    r = requests.post(url, data=text.lower().encode('utf-8'), headers=headers)
    with open(output_file, 'wb', encoding="utf-8") as out:
        out.write(r.content)


r = requests.post(
    'http://localhost:6969/tts_normalize',
    json={'data': open('misc/rest_use_case.txt', 'rt', encoding="utf-8").read(),
          "options": {
              "split_sentences": True,
              # letter, word
              "abbreviation_level": "abbreviation",
              # buh_temdegt, tugeemel_temdegt, no_temdegt, unshih_custom_temdegt, unshihgui_custom_temdegt
              "read_symbols": "no_temdegt",
              "read_emojis": True,
              "use_phonemizer": True
              }
          },
    headers={
        "Key": "9XZiFiU7z05pba6yMz8bnlTTQN1IjOx6GxMFHzU"
    }
)
response = json.loads(r.content)
normalized = response['normalized']
for i, text in enumerate(normalized):
    print("synth: len=%d %s" % (len(text), text))
    synthesize(text, '%d.wav' % i, voice_id=2)

# play with play command
os.system('play %s' % (" ".join(['%d.wav' % i for i in range(len(normalized))])))
