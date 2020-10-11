import requests, json, TOKENS



def get_synonyms(word, max_results = 10):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/typeOf"
    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        f'x-rapidapi-key': {TOKENS._SYNONYM_TOKEN_}
        }
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        # for x in response.json()['typeOf']:
        return '\n'.join(response.json()['typeOf'])



    else:
        return f'Sorry. No Synonyms found for "{word}"'
