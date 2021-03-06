import os
import re
import html
import bot.utils as utils
import bot.greq_pre
import grequests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
MERCURY_KEY = os.environ.get("MERCURY_KEY")
SMMRY_KEY = os.environ.get("SMMRY_KEY")

def mercury(url, flag="excerpt"):
    if flag == "summary":
        return summary(url)
    _url = "https://mercury.postlight.com/parser?url=" + url
    headers = {'x-api-key': MERCURY_KEY}
    r = [grequests.get(_url, headers=headers)]
    grequests.map(r, utils.exception_handler)
    res = r[0].response.json()
    if flag == "excerpt":
        return res["excerpt"]
    else: # return full content
        return strip_html(res["content"])

def summary(url):
    _url = "http://api.smmry.com?SM_API_KEY=" + SMMRY_KEY + "&SM_URL=" + url
    r = [grequests.get(_url)]
    grequests.map(r, utils.exception_handler)
    res = r[0].response.json()
    return res["sm_api_content"]

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
