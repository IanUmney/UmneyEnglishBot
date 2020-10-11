import requests, json, TOKENS
from utils import spell_check

APP_ID = TOKENS._OXFORD_ID_
API_KEY = TOKENS._OXFORD_TOKEN_
headers = {'app_id': APP_ID, 'app_key': API_KEY}
language = 'en-gb'

def define(word):
    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word.lower()
    r = requests.get(url, headers = headers)
    result = r.json()
    phoneticSpelling= ""
    definition = ""
    syns = ""
    lexicalCategory = ''
    try:
        phoneticSpelling = result["results"][0]["lexicalEntries"][0]["entries"][0]["pronunciations"][0]["phoneticSpelling"]
    except Exception as e:
        phoneticSpelling = "No phoneticSpelling"
    try:
        definition = result["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
    except:
        return f'No Definition found for "{word}"'
    try:
        for x in result["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["subsenses"][0]["synonyms"]:
            syns = syns + f"{x['text']}, "
    except Exception as e:
        syns = "None Available"
    try :
        lexicalCategory = result["results"][0]["lexicalEntries"][0]["lexicalCategory"]["text"]
    except Exception as e:
        lexicalCategory = "No category found"
    return(f'<b>{word}</b> <i>{phoneticSpelling}</i>\n<i>{lexicalCategory}</i>\n\n<b>Definition:</b> {definition}\n\n<b>Synonyms: </b>{syns}\n<i><u>Powered by Oxford Dictionaries</u></i>')
