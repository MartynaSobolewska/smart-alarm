from flask import Flask, render_template, url_for, request
from datetime import datetime
import time
import sched
import pyttsx3
import json_handler

app = Flask(__name__)


def schedule_already_saved():
    return


def tts_request(announcement="Text to speech example announcement!"):
    engine = pyttsx3.init()
    engine.say(announcement)
    engine.runAndWait()
    return "Hello text-to-speech example"


def fill_out_the_form():
    json_handler.save_new_notifications()
    alarms = json_handler.get_list_from_json("alarm")
    notifications = json_handler.get_list_from_json("notification")
    return render_template('alarms.html', alarms=alarms, notifications=notifications, image="pic.png")


def hhmm_to_seconds(time_str: str):
    print("hhmm to seconds")
    try:
        print("input hh: ", time_str[:2], ", input mm: ", time_str[-2:])
        hh_mm_ss_list = time_str.split(":")
        hh = int(hh_mm_ss_list[0])
        mm = int(hh_mm_ss_list[1])
        return hh * 60 * 60 + mm * 60
    except ValueError:
        print("Wrong time input")


def schedule_alarm(alarm: dict):
    print("schedule alarm")
    delay = hhmm_to_seconds(json_handler.get_list_from_json("user_input")[-1]["time"]) \
            - hhmm_to_seconds(datetime.now().strftime("%H:%M:%S"))
    print("delay: {}".format(delay))
    # s.enter(delay, 1, tts_request(alarm["title"]))



@app.route('/index')
def schedule_event():
    json_handler.get_user_input()
    print("schedule event")
    return fill_out_the_form()


@app.route("/")
def form():
    print("form (/)")
    return fill_out_the_form()

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
