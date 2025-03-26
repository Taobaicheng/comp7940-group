from flask import Flask
from serverless_wsgi import handle_request  


chatbot = Flask(__name__)

@chatbot.route("/")
def home():
    return "Hello from Netlify Function!"

def handler(event, context):
    return handle_request(chatbot, event, context)