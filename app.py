import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
from dotenv import load_dotenv, find_dotenv
import wiki, bus, misc

load_dotenv(find_dotenv())
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PORT = int(os.environ.get('PORT', '5000'))
APPNAME = os.environ.get("HEROKU_APP_NAME")
ENV_STATUS = os.environ.get("PROJ_ENV", "PROD")

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

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Type /help for more info")

def wiki_extract_handler(bot, update, args):
    extract = wiki.fetch_extract(' '.join(args))
    bot.send_message(chat_id=update.message.chat_id, text=extract)

def bus_id_handler(bot, update, args):
    reply = bus.fetch_buses(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def long_url_handler(bot, update, args):
    reply = misc.long_url(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    
    # handlers, think of this as your api
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('wiki', wiki_extract_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('bus', bus_id_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('expand', long_url_handler, pass_args=True))

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_error_handler(error)

    if ENV_STATUS == "DEV":
        print("-- DEV ENV--")
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TELEGRAM_TOKEN)
        updater.bot.set_webhook("https://" + APPNAME + ".herokuapp.com/" + TELEGRAM_TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()