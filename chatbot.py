from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import os
import logging
import urllib.parse
import asyncio

flask_app = Flask(__name__)
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_app = ApplicationBuilder().token(telegram_token).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running on Render!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("可用命令：\n/add <关键词> - 计数\n/map <位置> - 获取地图链接")

async def map_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("用法：/map <位置>")
        return
    location = " ".join(context.args)
    encoded = urllib.parse.quote(location)
    await update.message.reply_text(f"📍 位置：\nhttps://www.google.com/maps?q={encoded}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("map", map_command))

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return 'OK'

async def set_webhook(app):
    if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
        webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
        await app.bot.set_webhook(webhook_url)

if __name__ == '__main__':
    asyncio.run(set_webhook(telegram_app))