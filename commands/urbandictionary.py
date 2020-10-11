import requests, TOKENS

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"



headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    f'x-rapidapi-key': {TOKENS._URBAN_TOKEN_}
    }

def getDefinition(message):
    try:
        querystring = {"term":f"{message.text.split(' ', 1)[1]}"}
    except Exception:
        return("You must give me a word or phrase to define.")
    response = requests.request("GET", url, headers=headers, params=querystring)
    try:
        return(response.json()["list"][0]["definition"])
    except Exception:
        return("An error has occured. Try again later.")
