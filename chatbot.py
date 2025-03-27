from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from pymongo import MongoClient
import os
import logging
import urllib.parse

# 初始化Flask应用（必须命名为 flask_app）
flask_app = Flask(__name__)

# 初始化Telegram Bot
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_app = ApplicationBuilder().token(telegram_token).build()

# 注册命令处理函数
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

# 添加处理程序
handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help_command),
    CommandHandler("map", map_command)
]
for handler in handlers:
    telegram_app.add_handler(handler)

# Webhook路由（必须保留）
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return 'OK'

# 初始化Webhook（仅需运行一次）
if __name__ == '__main__':
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
    )