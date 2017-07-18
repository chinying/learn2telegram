import os
import re
import html
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
MERCURY_KEY = os.environ.get("MERCURY_KEY")

def mercury(url, flag="full"):
    _url = "https://mercury.postlight.com/parser?url=" + url
    headers = {'x-api-key': MERCURY_KEY}
    res = requests.get(_url, headers=headers).json()
    if flag == "excerpt":
        return res["excerpt"]
    else: # this is default
        return strip_html(res["content"])
    
# see https://tutorialedge.net/post/python/removing-html-from-string/
# trying not to use bs4 unless it's really needed
def strip_html(s):
    # separate the paragraphs first
    para_pat = re.compile('<\/?p.*?>')
    s = re.sub(para_pat, '\n', s)

    # strip the rest of the html tags
    pat = re.compile('<.*?>')
    stripped = re.sub(pat, '', s)
    return html.unescape(stripped)