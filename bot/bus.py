import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
import bot.utils as utils
import bot.greq_pre
import grequests

load_dotenv(find_dotenv())
LTA_TOKEN = os.environ.get("LTA_KEY")
BACKEND_URL = os.environ.get("BACKEND_SERVER_URL")
NEXT_BUS = "NextBus"
NEXT_BUS2 = "NextBus2"
NEXT_BUS3 = "NextBus3"

def parse_time(s):
    if len(s) == 0:
        return ""
    t = datetime.strptime(s[:-6], '%Y-%m-%dT%H:%M:%S')
    return datetime.strftime(t, '%H:%M')

def load_to_icon(s):
    if s == "LSD":
        return "🔴"
    elif s == "SDA":
        return "🔸"
    elif s == "SEA":
        return "🔵"
    else:
        return ""

def parse_request(req):
    if len(req) == 5 and req.isdigit():
        return fetch_buses(req)
    else:
        # TODO
        print("fetch results")
        return "unknown param"

def fetch_buses(stop_id):
    lta_url = "http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode=" + stop_id
    headers = {'AccountKey': LTA_TOKEN}
    backend_url = BACKEND_URL + "bus/stop/" + stop_id
    r = [grequests.get(lta_url, headers=headers), grequests.get(backend_url)]
    grequests.map(r, utils.exception_handler)
    ret = []
    response = r[0].response.json()["Services"]
    stop_name = r[1].response.json()["stops"]

    print(r[0].response.json())
    ret.append(stop_name[stop_id])

    if len(response) == 0:
        return "invalid stop id"
    else:
        for bus in response:
            formatted_string = "🚌 {}: {} {} {}  {} {} {}  {} {} {}".format(bus["ServiceNo"],
            parse_time(bus[NEXT_BUS]["EstimatedArrival"]), utils.surround_brackets(bus[NEXT_BUS]["Type"]), load_to_icon(bus[NEXT_BUS]["Load"]),
            parse_time(bus[NEXT_BUS2]["EstimatedArrival"]), utils.surround_brackets(bus[NEXT_BUS2]["Type"]), load_to_icon(bus[NEXT_BUS2]["Load"]),
            parse_time(bus[NEXT_BUS3]["EstimatedArrival"]), utils.surround_brackets(bus[NEXT_BUS3]["Type"]), load_to_icon(bus[NEXT_BUS3]["Load"]))

            ret.append(formatted_string)

    return "\n".join(ret)
