from flask import Flask, render_template, url_for, request
from datetime import datetime
import time
import sched
import pyttsx3
import json_handler

app = Flask(__name__)

def tts_request(announcement="Text to speech example announcement!"):
    engine = pyttsx3.init()
    engine.say(announcement)
    engine.runAndWait()
    return "Hello text-to-speech example"


@app.route("/index")
def form():
    alarms = json_handler.get_list_from_json("alarm")
    json_handler.get_user_input()
    notifications = json_handler.get_list_from_json("notification")
    json_handler.get_user_input()
    print(json_handler.get_list_from_json("user_input"))
    return render_template('alarms.html', alarms=alarms, notifications=notifications)


@app.route("/")
def CA3():
    tts_request("")
    alarms = json_handler.get_list_from_json("alarm")
    notifications = json_handler.get_list_from_json("notification")
    json_handler.get_user_input()
    print(json_handler.get_list_from_json("user_input"))
    return render_template('alarms.html', alarms=alarms, notifiations=notifications)


if __name__ == '__main__':
    app.run(debug=True)
