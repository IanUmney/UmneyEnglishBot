import requests, json, TOKENS


payload = {}
headers= {
  "apikey": TOKENS._SPELL_TOKEN_

}
def correct_spelling(word):
    url = f"https://api.promptapi.com/spell/spellchecker?q={word}"

    response = requests.request("GET", url, headers=headers, data = payload)
    status_code = response.status_code
    result = json.loads(response.text)

    if status_code == 200 and bool(result['corrections']):
        correction = result['corrections'][0]['best_candidate']
        return correction
    else:
        return word
