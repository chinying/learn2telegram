import requests

def long_url(url):
    r = requests.get("http://x.datasig.io/short?url=" + url)
    res = r.json()["/short"]
    if "destination" in res.keys():
        return res["destination"]
    else:
        return "error"