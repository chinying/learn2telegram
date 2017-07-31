import re
import urllib.parse
import bot.utils as utils
import bot.greq_pre
import grequests

def convert_to_url(term):
    return "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&redirects=1&exintro=&explaintext=&titles=" + urllib.parse.quote(term.title())

def cleanup(s):
    pat = re.compile("(\s\s+)|(\\n\s+)")
    s = re.sub(pat, " ", s)
    return s

def fetch_extract(term):
    text = []
    rs = [grequests.get(convert_to_url(term))]
    grequests.map(rs, utils.exception_handler)

    articles = rs[0].response.json()["query"]["pages"]
    for key in articles.keys():
        if key == "-1":
            return "No results found"
        text.extend([cleanup(articles[key]["extract"]),  "see more at https://en.wikipedia.org/?curid=" + key])
    return "\n".join(text)
