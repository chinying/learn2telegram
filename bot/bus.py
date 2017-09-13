import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
import bot.utils as utils
import bot.greq_pre
import grequests

load_dotenv(find_dotenv())
LTA_TOKEN = os.environ.get("LTA_KEY")
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

def fetch_buses(stop_id):
    url = "http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode=" + stop_id
    headers = {'AccountKey': LTA_TOKEN}
    r = [grequests.get(url, headers=headers)]
    grequests.map(r, utils.exception_handler)
    ret = []
    response = r[0].response.json()["Services"]
    if len(response) == 0:
        return "invalid stop id"
    else:
        for bus in response:
            # TODO, parse time, add hours, strip date, add load status
            ret.append(" ".join(["🚌 " + bus["ServiceNo"] + ":", 
            parse_time(bus[NEXT_BUS]["EstimatedArrival"]) + " " + load_to_icon(bus[NEXT_BUS]["Load"]) + " ", 
            parse_time(bus[NEXT_BUS2]["EstimatedArrival"]) + " " + load_to_icon(bus[NEXT_BUS2]["Load"]) + " ", 
            parse_time(bus[NEXT_BUS3]["EstimatedArrival"]) + " " + load_to_icon(bus[NEXT_BUS3]["Load"])]))
    
    return "\n".join(ret)
