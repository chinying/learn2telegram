import os
import bot.utils as utils
import bot.greq_pre
import grequests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DARKSKY_KEY = os.environ.get("DARKSKY_KEY")

latlng = "1.3294,103.8021"
settings = "units=uk2"
last_checked = None # TODO

def fetch_weather(params=["Currently"]):
    # test to parse params
    url = "https://api.darksky.net/forecast/{}/{}?{}".format(DARKSKY_KEY, latlng, settings)
    r = [grequests.get(url)]
    grequests.map(r, utils.exception_handler)
    res = r[0].response.json()
    current_weather = res["currently"]
    return "Temp.: {}\u00B0C\nFeels like: {}\u00B0C".format(current_weather["temperature"], current_weather["apparentTemperature"])
