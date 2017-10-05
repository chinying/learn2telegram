import os
import datetime
import bot.utils as utils
import bot.greq_pre
import grequests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DARKSKY_KEY = os.environ.get("DARKSKY_KEY")

latlng = "1.3294,103.8021" # TODO: fetch location from telegram, or maybe store as user settings in db
settings = "units=uk2"
last_checked = datetime.datetime.now()
cached_val = None

def fetch_weather(params=["Currently"], flush=False):
    global cached_val, last_checked
    # test to parse params
    now = datetime.datetime.now()
    ret = cached_val
    if (cached_val == None or (now - last_checked) > datetime.timedelta(minutes=30)) or flush is True:
        url = "https://api.darksky.net/forecast/{}/{}?{}".format(DARKSKY_KEY, latlng, settings)
        r = [grequests.get(url)]
        grequests.map(r, utils.exception_handler)
        res = r[0].response.json()
        ret = res["currently"]
        cached_val = ret
    else:
        # TODO clear
        print("using cached value")
    return "{}\nTemp.: {}\u00B0C\nFeels like: {}\u00B0C".format(ret["summary"], 
        ret["temperature"], ret["apparentTemperature"])
