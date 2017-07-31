import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
import utils
import greq_pre
import grequests

load_dotenv(find_dotenv())
LTA_TOKEN = os.environ.get("LTA_KEY")

def parse_time(s):
    if len(s) == 0:
        return ""
    t = datetime.strptime(s[:-6], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=8)
    return datetime.strftime(t, '%H:%M')

def load_to_icon(s):
    if s == "Limited Standing":
        return "🔴"
    elif s == "Standing Available":
        return "🔸"
    elif s == "Seats Available":
        return "🔵"
    else:
        return ""

def fetch_buses(stop_id):
    url = "http://datamall2.mytransport.sg/ltaodataservice/BusArrival?BusStopID=" + stop_id
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
            parse_time(bus["NextBus"]["EstimatedArrival"]) + " " + load_to_icon(bus["NextBus"]["Load"]), 
            parse_time(bus["SubsequentBus"]["EstimatedArrival"]) + " " + load_to_icon(bus["SubsequentBus"]["Load"]), 
            parse_time(bus["SubsequentBus3"]["EstimatedArrival"]) + " " + load_to_icon(bus["SubsequentBus3"]["Load"]) ]))
    
    return "\n".join(ret)