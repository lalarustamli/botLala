from flask import request
from app import app
from app import chatbot
import subprocess
import os

@app.route("/")
def hello_world():
    return 'Hello, World!'


@app.route("/github_hook", methods=['POST'])
def deploy():
    try:
        output = subprocess.check_output("sudo chmod +x deploy.sh && sudo ./deploy.sh", shell=True,
                                         cwd="/var/www/chatbot")
    except Exception as e:
        return str(e)
    return output


@app.route("/webhook", methods=['GET', 'POST'])
def listen():
    if request.method == "GET":
        print('GET : '+ str(request.json))
        return chatbot.verify_webhook(request)

    if request.method == "POST":
        print('POST : '+ str(request.json))
        # print("REQUEST: "+ str(request.json['entry'][0]))
        if 'messaging' in request.json['entry'][0]:
            events = request.json['entry'][0]['messaging']
            for event in events:
                if chatbot.is_user_message(event):
                    chatbot.respond(event)
                elif chatbot.is_user_postback(event):
                    if str(event['postback']['payload']) == 'live_message':
                        r_id=str(event['sender']['id'])
                        # print(r_id)
                        chatbot.live_message(r_id)
                    chatbot.postback_response(event)

        return "user message"
