import os
import greq_pre
import grequests
from dotenv import load_dotenv, find_dotenv
from utils import exception_handler

load_dotenv(find_dotenv())
OXFORD_APP_ID = os.environ.get("OXFORD_APP_ID") 
OXFORD_APP_KEY = os.environ.get("OXFORD_APP_KEY")

def parse_results(data):
    lexicalEntries = map(lambda x: x['entries'], data["results"][0]['lexicalEntries'])
    response = []
    cumulative_cnt = 1

    for entry in lexicalEntries:
        for idx, senses in enumerate(entry[0]['senses'], start=cumulative_cnt):
            domains = "[{}] ".format(", ".join(senses['domains'])) if 'domains' in senses else ""
            registers = "[{}] ".format(", ".join(senses['registers'])) if 'registers' in senses else ""
            # print(senses['definitions'], domain, registers)
            response.append("{}. {}{}{}".format(idx, registers, domains, senses['definitions'][0]))
            if 'subsenses' in senses:
                for subidx, subsense in enumerate(senses['subsenses'], start=1):
                    domains = "[{}] ".format(", ".join(subsense['domains'])) if 'domains' in senses else ""
                    response.append('{}.{}. {}{}'.format(idx, subidx, domains, subsense['definitions'][0]))
            cumulative_cnt=idx+1

    return "\n".join(response)

def retrieve(term):
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + term.lower()
    headers = {"Accept": "application/json",
               "app_id": OXFORD_APP_ID,
               "app_key": OXFORD_APP_KEY
               }
    r = [grequests.get(url, headers=headers)]
    grequests.map(r, exception_handler)
    
    # TODO move this error checking into utils or something
    if r[0].response.status_code == 404:
        return "Not found"
    if r[0].response.status_code == 500:
        return "Server pooped itself"

    res = r[0].response.json()
    return parse_results(res)
