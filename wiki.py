import urllib.parse
import requests
import json

def convert_to_url(term):
    return "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&redirects=1&exintro=&explaintext=&titles=" + urllib.parse.quote(term)

# TODO redirect based on term
def fetch_extract(term):
    text = []
    rs = requests.get(convert_to_url(term))

    articles = rs.json()["query"]["pages"]
    for key in articles.keys():
        if key == "-1":
            return "No results found"
        text.extend([articles[key]["extract"],  "see more at https://en.wikipedia.org/?curid=" + key])

    return "\n".join(text)