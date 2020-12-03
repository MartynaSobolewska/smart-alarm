"""This is a module containing functions for saving and retrieving data from json data files"""
import json
from datetime import datetime, timedelta
from flask import request, Markup
from typing import List, Dict
import APIs_fetcher
import alarm
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_list_from_json(data_type: str):
    """returns a list of dictionaries that contain
    the alarm data from alarms_data.json"""
    # if wrong data type provided, raise an error
    if not data_type in json_files.keys():
        logger.error("Error: wrong data type '{}' trying to be saved.".format(data_type))
    with open(json_files[data_type], "r") as data_file:
        try:
            data = json.load(data_file)
        # the file might be empty, then this error will occur:
        except ValueError:
            # then return an empty list
            return []
    return data


json_files = {
    "alarm": "data/alarms_data.json",
    "notification": "data/notifications_data.json",
    "config": "data/config.json",
    "covid_temp": "data/covid_temp.json",
    "news_temp": "data/news_temp.json"
}

CITY = get_list_from_json("config")["city"]


def save_new_notifications():
    """Gets a list of notifications containing: 3 latest BBC articles every 12h,
    Current weather info for city specified in config.json file
    COVID-19 cases data from yesterday.
    News articles and COVID-19 data are temporarily stored in json files
    and updated when needed."""

    logger.info("Refreshing the notifications")

    clean_json("notification")
    notifications = []

    # get pre-fetched articles from the json file
    articles = list(APIs_fetcher.news_api()["articles"])
    # sort articles from the most to least recent
    latest_articles = sorted(articles, key=lambda item: item['publishedAt'], reverse=True)[:3]
    save_list_to_json(latest_articles, "news_temp")

    for article in latest_articles:
        notification = {}
        notification["title"] = article["title"]
        notification["content"] = article["description"]
        notifications.append(notification)

    # get weather for the city specified in config.json
    weather_data = APIs_fetcher.weather_api(CITY)
    weather_title = "Current weather in {}: {}".format(CITY, weather_data['weather'][0]["main"])
    weather_content = "Temperature: {}°C, Pressure: {}hPa, Humidity: {}%".format(weather_data['main']['temp'],
                                                                                 weather_data['main']['pressure'],
                                                                                 weather_data['main']['humidity'])
    notifications.append({"title": weather_title, "content": weather_content})

    # get the data about covid from json file
    covid_data = get_list_from_json("covid_temp")
    covid_title = "COVID-19 new cases yesterday"
    # check if data from json was fetched for yesterday, if not, fetch it from API
    if len(covid_data) == 0 or \
            not covid_data["England"]["data"][0]["date"] == str(
                datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d")):
        logger.info("Covid data not from yesterday, fetching new data from API.")
        covid_data = APIs_fetcher.covid_api(CITY)
        save_list_to_json(covid_data, "covid_temp")

    # formatting notification about covid
    covid_content = "{}: {}, ".format(CITY, covid_data[CITY]["data"][0]["newCasesByPublishDate"]) + \
                    "{}: {}, ".format('England', covid_data["England"]["data"][0]["newCasesByPublishDate"]) + \
                    "{}: {}, ".format('Scotland', covid_data["Scotland"]["data"][0]["newCasesByPublishDate"]) + \
                    "{}: {}, ".format('Northern Ireland',
                                      covid_data["Northern Ireland"]["data"][0]["newCasesByPublishDate"]) + \
                    "{}: {}".format('Wales', covid_data["Wales"]["data"][0]["newCasesByPublishDate"])

    notifications.append({"title": covid_title, "content": covid_content})
    save_list_to_json(notifications, "notification")
    return notifications


def clean_json(data_type: str):
    """deletes all the data from the json corresponding to the data type.
    data_type is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored."""
    # check if correct data type
    if not data_type in json_files.keys():
        logger.error("Incorrect data type detected while tying to clear the json file.")
        return
    with open(json_files[data_type], "w") as app_data_file:
        json.dump([], app_data_file)


def delete_from_json(data_type: str, data_object: dict):
    """looks for a corresponding object in the list fetched from json and, if found,
     deletes it and saves an updated list"""
    list_of_obj = get_list_from_json(data_type)
    logger.info("Attempting to delete a {} object.".format(data_type))
    try:
        list_of_obj.remove(data_object)
        logger.info("Removing object of type {} with title {}".format(data_type, data_object["title"]))
        save_list_to_json(list_of_obj, data_type)
    except ValueError:
        logger.warning("object of type {} and title {} not found, hence unable to delete it".format(data_type, data_object["title"]))


def save_list_to_json(data: List[dict], data_type: str):
    """saves a list of dictionaries to a json file.
    data_type is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored."""
    clean_json(data_type)
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
            logger.error("The dictionary formatting found wrong while trying to add an object to {}.".format(json_files[data_type]))
            return
        if data_type == "alarm" and not ('date' in list(data.keys()) and 'time' in list(data.keys())):
            logger.error("The alarm does not contain a date.")
    elif data_type == "user_input":
        if not list(data.keys()) == ['date', 'time', 'label', 'news', 'weather']:
            logger.error("The dictionary formatting found wrong while trying to add an object to {}.".format(json_files[data_type]))
    # Make sure that the provided data type is correct, else raise an error
    elif not data_type in json_files.keys():
        logger.error("Wrong data type '{}' trying to be saved.".format(data_type))

    data_list = get_list_from_json(data_type)
    data_list.append(data)
    # if the alarm is added, make sure the list of alarms is sorted by the time they should be triggered
    if data_type == "alarm":
        sorted_data_list = sorted(data_list, key=lambda alarm: datetime.strptime(alarm["date"] + alarm["time"],
                                                                                 "%Y-%m-%d%H:%M:%S"))
    else: sorted_data_list = data_list
    save_list_to_json(sorted_data_list, data_type)


def process_user_input(date_time, label, is_news, is_weather):
    """process the data gathered from the form in a way that it can be saved to alarms.json file
    Check if the inputs are correct,
    If they are, save the alarm."""
    logger.info("Processing user input...")
    # if this is none, do not save because the rest is too
    if date_time is None:
        logger.warning("No date selected in user input.")
        alarm.tts_request("No date selected.")
        return
    # check if the selected time is in the future
    full_date = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
    if datetime.now() > full_date:
        logger.warning("Date selected by user is in the past.")
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
            logger.warning("User tried to set two alarms at the same time.")
            alarm.tts_request("Another alarm is already scheduled at that time.")
            return
    # alarm data formatting
    dictionary = {"date": date, "time": time, "title": label,
                  "content": "alarm set for {} at {}".format(date, time),
                  "news": True if is_news == "news" else False,
                  "weather": True if is_weather == "weather" else False}
    # save in json file
    add_data_to_json("alarm", dictionary)
    # alarms have to all be scheduled in a correct order so other alarms need rescheduling
    logger.info("New alarm added, need for rescheduling.")
    alarm.schedule_all_alarms()


def get_user_input():
    """get the data from the form"""
    date_time = request.args.get("alarm")
    label = request.args.get("two")
    is_news = request.args.get("news")
    is_weather = request.args.get("weather")
    if not date_time is None:
        logger.info("User input data.")
        try:
            datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
            process_user_input(date_time, label, is_news, is_weather)

        except ValueError:
            logger.warning("Wrong date input from the user!")
            return


def get_alarm_content(alarm: dict):
    """Based on what user wanted to be informed about, create a message to be read."""
    content = ""
    # get 3 most recent news articles from API (those from notifications are fetched every 12h)
    news = sorted(APIs_fetcher.news_api()["articles"], key=lambda item: item['publishedAt'], reverse=True)[:3]
    # get notifications
    notifications = get_list_from_json("notification")
    if alarm["news"]:
        for n in news:
            content += "{}: {};\n ".format(n["title"], n["description"])
    # get weather from notifications, it is always up to date
    if alarm["weather"]:
        content += "{}: {};\n ".format(notifications[-2]["title"], notifications[-2]["content"])
    content += "{}: {}".format(notifications[-1]["title"], notifications[-1]["content"])
    return content


def trigger_alarm(alarm_dict: dict):
    """At scheduled time, fetch up-to-date data to inform user and read it out loud."""
    logger.info("Alarm with title '{}' triggered".format(alarm_dict["title"]))
    # get up to date data based on user preferences
    alarm_dict["content"] = get_alarm_content(alarm_dict)
    logger.info("Alarm read: {}".format(alarm_dict["content"]))
    # read alarm title and content
    alarm.tts_request(alarm_dict["title"])
    alarm.tts_request(alarm_dict["content"])
    # delete the alarm since it was already triggered
    delete_from_json("alarm", alarm_dict)
