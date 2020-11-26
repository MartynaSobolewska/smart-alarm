from flask import Flask, render_template, url_for, request
from datetime import datetime
import time
import sched
import pyttsx3
import data_handler

app = Flask(__name__)

def tts_request(announcement="Text to speech example announcement!"):
    engine = pyttsx3.init()
    engine.say(announcement)
    engine.runAndWait()
    return "Hello text-to-speech example"


@app.route("/index")
def form():
    alarms = data_handler.get_alarms()
    data_handler.get_user_input()
    return render_template('alarms.html', alarms=alarms)


@app.route("/")
def CA3():
    alarms = data_handler.get_alarms()
    return render_template('alarms.html', alarms=alarms)


if __name__ == '__main__':
    app.run(debug=True)
