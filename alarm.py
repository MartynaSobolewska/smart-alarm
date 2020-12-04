"""A module handling scheduling and Flask loading in two threads"""
from datetime import datetime, timedelta
import time
import sched
import threading
import logging
import pyttsx3
from flask import Flask, render_template, request
import json_handler

app = Flask(__name__)
# scheduler is used as a global variable to enable access in multiple functions
SCHED = None
# always restart after closing and opening the app
TIME_LAST_REFRESH = datetime.now()
logger = logging.getLogger(__name__)
logging.basicConfig(filename='sys.log',
                    format='%(levelname)s %(name)s, %(asctime)s: %(message)s')


def schedule_all_alarms() -> None:
    """gets all alarms from the alarms.json file and schedules them
    making sure none are scheduled for the past.
    Runs the scheduler."""
    logger.info("Rescheduling alarms.")

    global SCHED
    # restart the scheduler
    SCHED = sched.scheduler(time.time, time.sleep)
    delete_alarms_in_the_past()
    alarms = json_handler.get_list_from_json("alarm")
    for alar in alarms:
        delay = get_delay(alar["date"], alar["time"])
        SCHED.enter(delay, 1, json_handler.trigger_alarm, argument=(alar,))

    thread = threading.Thread(target=run_sched)
    thread.start()


def delete_alarms_in_the_past() -> None:
    """Finds alarms that are set in the past and deletes them from json file"""
    alarms = json_handler.get_list_from_json("alarm")
    for alarm in alarms:
        delay = get_delay(alarm["date"], alarm["time"])
        if delay < 0:
            json_handler.delete_from_json("alarm", alarm)


def tts_request(announcement="Text to speech example announcement!") -> None:
    """Reads the message specified in parameter"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[2].id)
    engine.say(announcement)
    engine.runAndWait()


def fill_out_the_form():
    """fills out the form with data from json files, refreshes the notifications
    if they have not been refreshed for over an hour. Returns the filled out form"""
    global TIME_LAST_REFRESH
    delete_alarms_in_the_past()
    # refresh the notifications every hour
    if TIME_LAST_REFRESH + timedelta(hours=1) < datetime.now():
        logger.info("Refreshing the news since the hour has passed.")
        TIME_LAST_REFRESH = datetime.now()
        json_handler.save_new_notifications()
    # fetch the data from json files
    notifications = json_handler.get_list_from_json("notification")
    alarms = json_handler.get_list_from_json("alarm")
    return render_template('alarms.html', alarms=alarms,
                           notifications=notifications, image="pic.png")


def get_delay(date: str, time_str: str) -> int:
    """Returns the difference in second between the given parameter and current time"""
    try:
        now = datetime.now()
        future = datetime.strptime(date+time_str, "%Y-%m-%d%H:%M:%S")
        return (future-now).total_seconds()
    except ValueError:
        logger.error("Wrong date formatting trying to be converted in get_delay function.")

def delete_an_object() -> None:
    """Finds an object to be deleted based on the current URL
     and uses a method from a json_handler.py to delete it"""
    logger.info("User pressed x button to delete an alarm/notification.")
    delete_title = request.url.split("?")[1]
    # find out if we delete alarm or notification
    delete_type = delete_title.split("=")[0]
    if delete_type == "notif":
        delete_type = "notification"
    elif delete_type == "alarm_item":
        delete_type = "alarm"
    else:
        logger.warning("Unable to recognize what type of data user wants to delete.")
        # go to main page
        form()
    # get rid of non-alphanumeric chars and problematic chars
    delete_title = delete_title.replace("%3A", "")
    delete_title = delete_title.replace("%27", "")
    delete_title_modified = ''.join([i for i in delete_title.split("=")[1] if i.isalpha()])
    list_of_obj = json_handler.get_list_from_json(delete_type)
    for obj in list_of_obj:
        obj_title_modified = ''.join([i for i in obj["title"] if i.isalpha()])
        if obj_title_modified == delete_title_modified:
            logger.info("Successfully found an object to delete.")
            json_handler.delete_from_json(delete_type, obj)
            break

@app.route('/index')
def index():
    """renders the html form and listens for user trying to delete an object."""
    json_handler.get_user_input()
    # deleting alarm/notification
    if "alarm_item" in str(request.url) or "notif" in str(request.url):
        delete_an_object()
    return fill_out_the_form()


def run_sched() -> None:
    """Starts a scheduler."""
    SCHED.run()


@app.route("/")
def form():
    """Renders the html form for the homepage."""
    return fill_out_the_form()


if __name__ == '__main__':
    logger.info("Start app: refresh notifications and reschedule alarms.")
    json_handler.save_new_notifications()
    schedule_all_alarms()
    app.run(debug=False, use_reloader=False)
