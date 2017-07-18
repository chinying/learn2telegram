import requests

def search(term, flags=None):
    url = "http://api.duckduckgo.com/?q=" + term + "&format=json"
    r = requests.get(url)
    res = r.json()
    _type = res["Type"]
    result = ""
    if _type == "A":
        result = "Type: {}\n{} \nTaken from {}".format(res["Entity"], res["AbstractText"], res["AbstractURL"])
    elif _type == "D":
        result = "View disambugation page {}\n".format(res["AbstractURL"])
        result += related(res)

    return result
            
def related(res):
    results = []
    topics = res["RelatedTopics"]
    for idx, topic in enumerate(topics, start=1):
        if "Text" in topic:
            row = "{}. {} \n{}\n".format(idx, topic["Text"], topic["FirstURL"])
            results.append(row)
    return "\n".join(results)

def ddg_in_browser(term):
    return "https://duckduckgo.com/?q=" + term
