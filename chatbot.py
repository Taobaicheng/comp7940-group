from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext)
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import configparser
import logging
#import redis
import urllib.parse
import os
import asyncio
from flask import Flask, request


flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

#async def start(update: Update, context):
    #await update.message.reply_text("✅ Bot is running on Render!")

#async def echo(update: Update, context):
    #await update.message.reply_text(update.message.text)

#async def main():
    #await flask_app.bot.set_webhook(f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook")
    #flask_app.run(host='0.0.0.0', port=os.environ.get('PORT', 10000))

#telegram_app.add_handler(CommandHandler("start", start))
#telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return 'OK'


from ChatGPT_HKBU import HKBU_ChatGPT

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


#global redis1
def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    #global redis1
    #redis1 = redis.Redis(host=(config['REDIS']['HOST']),
                #password=(config['REDIS']['PASSWORD']),
                #port=(config['REDIS']['REDISPORT']),
                #decode_responses=(config['REDIS']['DECODE_RESPONSE']),
                #username=(config['REDIS']['USER_NAME']))
    mongo_client = MongoClient(config['MONGODB']['CONNECTION_STRING'])
    db = mongo_client[config['MONGODB']['DATABASE_NAME']]
    collection = db[config['MONGODB']['COLLECTION_NAME']]
    
# You can set this logging module, so you will know when
# and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# register a dispatcher to handle message: here we register an echo dispatcher
    #echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)
# dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
# on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("map", map_command))
# To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        redis1.incr(msg)

        update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def map_command(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text('Usage: /map <location>')
        return
    
    try:
        location = " ".join(context.args)
        encoded_location = urllib.parse.quote(location)
        map_url = f"https://www.google.com/maps?q={encoded_location}"
        update.message.reply_text(f"📍 这里是为您找到的 {location} 的位置：\n{map_url}")
    except Exception as e:
        logging.error(f"处理 /map 命令时出错: {str(e)}")
        update.message.reply_text("⚠️ 获取位置信息时出现错误，请稍后再试。")

if __name__ == '__main__':
    telegram_app.run_webhook(
        listen='0.0.0.0',
        port=10000,
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
    )


