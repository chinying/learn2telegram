import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
from dotenv import load_dotenv, find_dotenv
from bot import wiki, bus, divers, mercury_postlight, duckduckgo, oxford_dict
from bot import nlp

load_dotenv(find_dotenv())
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PORT = int(os.environ.get('PORT', '5000'))
APPNAME = os.environ.get("HEROKU_APP_NAME")
ENV_STATUS = os.environ.get("PROJ_ENV", "PROD")

MAX_MSG_LEN = 4096

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
	logger.warning('Update "%s" caused error "%s"' % (update, error))

def error_callback(bot, update, error):
    try:
        raise error
    except TimedOut:
        # TODO replace with retry function of some sort
        bot.send_message(chat_id=update.message.chat_id, text="Timed out")
    except TelegramError:
        # handle all other telegram related errors
        logger.warning('Update "%s" caused error "%s"' % (update, error))

def split_msg(bot, update, reply):
    try:
        bot.send_message(chat_id=update.message.chat_id, text=reply)
    except:
        msglen = len(reply)
        for i in range((22288 // 4096) + 1):
            bot.send_message(chat_id=update.message.chat_id, text=reply[MAX_MSG_LEN * i : MAX_MSG_LEN * (i + 1)])

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    text = update.message.text
    msg = nlp.extract_entity(text)
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def help_handler(bot, update):
    commands = ["/wiki <term> to search wikipedia",
                "/bus <stop number> to get bus timings",
                "/expand <url>",
                "/article <url> (full|excerpt) for summary"
               ]
    message = "\n".join(commands)
    bot.send_message(chat_id=update.message.chat_id, text=message)    

def wiki_extract_handler(bot, update, args):
    extract = wiki.fetch_extract(' '.join(args))
    split_msg(bot, update, extract)
    
def bus_id_handler(bot, update, args):
    reply = bus.fetch_buses(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def long_url_handler(bot, update, args):
    reply = divers.long_url(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def mercury_handler(bot, update, args):
    allowed_flags = ["full", "excerpt"]
    flag = "excerpt"
    if len(args) > 1:
        if (args[1] in allowed_flags):
            print("fetching with flag " + args[1])
            flag = args[1]
    reply = mercury_postlight.mercury(args[0], flag)
    split_msg(bot, update, reply)

def duck_handler(bot, update, args):
    term = " ".join(args)
    message = duckduckgo.search(term)
    bot.send_message(chat_id=update.message.chat_id, text=message)

def oxford_dict_handler(bot, update, args):
    term = " ".join(args)
    reply = oxford_dict.retrieve(term)
    bot.send_message(chat_id=update.message.chat_id, text=reply) 

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    
    # handlers, think of this as your api
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('wiki', wiki_extract_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('bus', bus_id_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('expand', long_url_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('article', mercury_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('answer', duck_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('dict', oxford_dict_handler, pass_args=True))

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_error_handler(error)

    if ENV_STATUS == "DEV":
        print("-- DEV ENV --")
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TELEGRAM_TOKEN)
        updater.bot.set_webhook("https://" + APPNAME + ".herokuapp.com/" + TELEGRAM_TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()