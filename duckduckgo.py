import greq_pre
import utils
import grequests

def search(term, flags=None):
    url = "http://api.duckduckgo.com/?q=" + term + "&format=json"
    r = [grequests.get(url)]
    grequests.map(r, utils.exception_handler)
    res = r[0].response.json()
    _type = res["Type"]
    result = ""

    _entity = res["Entity"]
    if _entity == "film":
        result += infobox(res, {"Starring", "Released", "Running time"})

    if _type == "A":
        result = "Type: {}\n{} \nTaken from {}".format(res["Entity"], res["AbstractText"], res["AbstractURL"])
    elif _type == "D":
        result = "View disambugation page {}\n".format(res["AbstractURL"])
        result += related(res)
    
    return "No results found." if result == "" else result

# untested
def infobox(res, wanted_keys):
    if res["Infobox"] == "":
        return "No infobox"
    info = []
    
    # feels like this can be more elegantly done, with a collect function of some sort
    fl = filter((lambda j: j["label"] in wanted_keys), res["Infobox"]["content"])
    for f in fl:
        info.append("{}: {}".format(f["label"], f["value"]))
    return "\n".join(info)

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
