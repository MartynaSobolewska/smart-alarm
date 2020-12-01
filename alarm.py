from flask import Flask, render_template, url_for, request
from datetime import datetime, timedelta
import time
import sched
import pyttsx3
import json_handler
import threading

app = Flask(__name__)
s = None
time_last_refresh = datetime.now()


def schedule_all_alarms():
    """get all alarms from the alarms.json file and schedule them
    making sure none are scheduled for the past.
    Run the scheduler."""
    print("schedule all alarms")
    global s
    s = sched.scheduler(time.time, time.sleep)
    delete_alarms_in_the_past()
    alarms = json_handler.get_list_from_json("alarm")
    for a in alarms:
        delay = get_delay(a["date"], a["time"])
        s.enter(delay, 1, json_handler.trigger_alarm, argument=(a,))

    x = threading.Thread(target=run_sched)
    x.start()


def delete_alarms_in_the_past():
    alarms = json_handler.get_list_from_json("alarm")
    for alarm in alarms:
        delay = get_delay(alarm["date"], alarm["time"])
        if delay < 0:
            json_handler.delete_from_json("alarm", alarm)


def tts_request(announcement="Text to speech example announcement!"):
    engine = pyttsx3.init()
    engine.say(announcement)
    engine.runAndWait()
    return "Hello text-to-speech example"


def fill_out_the_form():
    global time_last_refresh
    delete_alarms_in_the_past()
    # refresh the notifications every hour
    if time_last_refresh + timedelta(hours=1) < datetime.now():
        print("an hour have past. Refresh notifications!")
        time_last_refresh = datetime.now()
        json_handler.save_new_notifications()
    notifications = json_handler.get_list_from_json("notification")
    alarms = json_handler.get_list_from_json("alarm")
    return render_template('alarms.html', alarms=alarms, notifications=notifications, image="pic.png")


def get_delay(date: str, time:str):
    try:
        now = datetime.now()
        future = datetime.strptime(date+time, "%Y-%m-%d%H:%M:%S")
        return (future-now).total_seconds()
    except ValueError:
        print("Wrong time input")


@app.route('/index')
def schedule_event():
    json_handler.get_user_input()
    print(request.url)
    if "alarm_item" in str(request.url) or "notif" in str(request.url):
        print("trying to delete")
        delete_title = request.url.split("?")[1]
        #find out if we delete alarm or notification
        delete_type = delete_title.split("=")[0]
        if(delete_type == "notif"):
            delete_type = "notification"
        elif(delete_type == "alarm_item"):
            delete_type = "alarm"
        else:
            print("Wrong delete type")
            return
        # get rid of non-alphanumeric chars and problematic chars
        delete_title = delete_title.replace("%3A", "")
        delete_title = delete_title.replace("%27", "")
        delete_title_only_with_alphabet = ''.join([i for i in delete_title.split("=")[1] if i.isalpha()])
        list_of_obj = json_handler.get_list_from_json(delete_type)
        for o in list_of_obj:
            o_title_only_with_alphabet = ''.join([i for i in o["title"] if i.isalpha()])
            if o_title_only_with_alphabet == delete_title_only_with_alphabet:
                print("matched: "+ str(o))
                json_handler.delete_from_json(delete_type, o)
                break
    return fill_out_the_form()


def run_sched():
    s.run()


@app.route("/")
def form():
    return fill_out_the_form()

if __name__ == '__main__':
    json_handler.save_new_notifications()
    schedule_all_alarms()
    app.run(debug=False, use_reloader=False)
