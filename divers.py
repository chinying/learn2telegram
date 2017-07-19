import utils
import grequests

def long_url(url):
    if not url.startswith('http'):
        url = "http://" + url
    r = [grequests.get("http://x.datasig.io/short?url=" + url)]
    grequests.map(r, utils.exception_handler)
    res = r[0].response.json()["/short"]
    if "destination" in res.keys():
        return res["destination"]
    else:
        return "error"