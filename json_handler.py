"""This is a module containing functions for saving and retrieving data from json data files"""
import json
from datetime import datetime
from flask import request
from typing import List, Dict
import APIs_fetcher
import alarm

CITY = 'Exeter'

json_files = {
    "alarm": "data/alarms_data.json",
    "notification": "data/notifications_data.json",
    "user_input": "data/user_input_data.json"
}


def save_new_notifications():
    """Saves 4 latest BBC news, """
    clean_json("notification")
    notifications = []
    articles = list(APIs_fetcher.news_api()["articles"])
    # get four latest articles from bbc
    latest_articles = sorted(articles, key=lambda item: item['publishedAt'], reverse=True)[:4]
    for article in latest_articles:
        notification = {}
        notification["title"] = article["title"]
        notification["content"] = article["description"]
        notifications.append(notification)
    weather_data = APIs_fetcher.weather_api(CITY)
    weather_title = "Today's weather in {}: {}".format(CITY, weather_data['weather'][0]["main"])
    weather_content = "Temperature: {}°C, Pressure: {}hPa, Humidity: {}%".format(weather_data['main']['temp'], weather_data['main']['pressure'], weather_data['main']['humidity'])
    notifications.append({"title": weather_title, "content": weather_content})
    save_list_to_json(notifications, "notification")
    return notifications



def clean_json(data_type: str):
    """deletes all the data from the json corresponding to the data type.
    data_type is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored."""
    # check if correct data type
    if not data_type in json_files.keys():
        raise ValueError("Incorrect data type detected while tying to clear the json file.")
    with open(json_files[data_type], "w") as app_data_file:
        json.dump([], app_data_file)


def save_list_to_json(data: List[dict], data_type: str):
    """saves a list of dictionaries to a json file.
    data_type is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored."""
    # if the list is empty, just do not save.
    if not data:
        return
    with open(json_files[data_type], "w") as app_data_file:
        json.dump(data, app_data_file)


def add_data_to_json(data_type: str, data: Dict):
    """gets a dictionary with the data,
    and a data_type which is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored.
    adds a new alarm to the list and saves the extended list
    to alarms_data.json file"""

    # Make sure that the dictionary contains the needed keys.
    if data_type == "alarm" or data_type == "notification":
        if not ('title' in list(data.keys()) and 'content' in list(data.keys())):
            raise ValueError("Error: the dictionary formatting is wrong.")
        if data_type == "alarm" and not ('date' in list(data.keys()) and 'time' in list(data.keys())):
            raise ValueError("Error: the alarm does not contain a date.")
    elif data_type == "user_input":
        if not list(data.keys()) == ['date', 'time', 'label', 'news', 'weather']:
            raise ValueError("Error: the dictionary formatting is wrong.")
    # Make sure that the provided data type is correct, else raise an error
    elif not data_type in json_files.keys():
        raise ValueError("Error: wrong data type '{}' trying to be saved.".format(data_type))



    data_list = get_list_from_json(data_type)
    data_list.append(data)
    # if the alarm is added, make sure the list of alarms is sorted by the time they should be triggered
    if data_type == "alarm":
        sorted_data_list = sorted(data_list, key=lambda alarm: datetime.strptime(alarm["date"]+alarm["time"], "%Y-%m-%d%H:%M:%S"))
    save_list_to_json(sorted_data_list, data_type)


def get_list_from_json(data_type: str):
    """returns a list of dictionaries that contain
    the alarm data from alarms_data.json"""
    # if wrong data type provided, raise an error
    if not data_type in json_files.keys():
        raise ValueError("Error: wrong data type '{}' trying to be saved.".format(data_type))
    with open(json_files[data_type], "r") as data_file:
        try:
            data = json.load(data_file)
        # the file might be empty, then this error will occur:
        except ValueError:
            # then return an empty list
            return []
    return data


def process_user_input(date_time, label, is_news, is_weather):
    """process the data gathered from the form in a way that it can be saved to alarms.json file
    Check if the inputs are correct,
    If they are, save the alarm."""
    print("process user input")
    # if this is none, do not save because the rest is too
    if date_time is None:
        alarm.tts_request("No date selected.")
        return
    # check if the selected time is in the future
    full_date = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
    if datetime.now() > full_date:
        alarm.tts_request("Date selected is in the past.")
        return

    date = str(full_date.date())
    time = str(full_date.time())

    alarms = get_list_from_json("alarm")
    # check if there is any other alarm set at that date
    datetimes = []
    if alarms:
        for a in alarms:
            previously_saved_date_time = ""
            previously_saved_date_time += a["date"]
            previously_saved_date_time += a["time"]
            datetimes.append(previously_saved_date_time)
        new_date_time = date + time
        # if there is another alarm at that time, notify the user
        if new_date_time in datetimes:
            alarm.tts_request("Another alarm is already scheduled at that time.")
            return

    dictionary = {"date": date, "time": time, "title": label,
                  "content": "alarm set for {} at {}".format(date, time),
                  "news": True if is_news == "news" else False,
                  "weather": True if is_weather == "weather" else False}
    # save in json file
    add_data_to_json("alarm", dictionary)
    # add event to the scheduler
    # alarm.schedule_alarm(dictionary)


def get_user_input():
    """get the data from the form"""
    date_time = request.args.get("alarm")
    label = request.args.get("two")
    is_news = request.args.get("news")
    is_weather = request.args.get("weather")
    if not date_time is None:
        print("get user input")
        try:
            print("Date selected: " + date_time)
            datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
            process_user_input(date_time, label, is_news, is_weather)

        except ValueError:
            print("Wrong date input!")
            return