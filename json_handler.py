"""This is a module containing functions for saving and retrieving data from json data files"""
import json
from datetime import datetime
from flask import request
from typing import List, Dict

json_files = {
    "alarm": "data/alarms_data.json",
    "notification": "data/notifications_data.json",
    "user_input": "data/user_input_data.json"
}


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
    # dictionary formatting is checked in the add_alarm function
    # it can be skipped here since this function should only be called from there
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
        if not list(data.keys()) == ['title', 'content']:
            raise ValueError("Error: the dictionary formatting is wrong.")
    elif data_type == "user_input":
        if not list(data.keys()) == ['date', 'time', 'label', 'news', 'weather']:
            raise ValueError("Error: the dictionary formatting is wrong.")
    # Make sure that the provided data type is correct, else raise an error
    elif not data_type in json_files.keys():
        raise ValueError("Error: wrong data type '{}' trying to be saved.".format(data_type))

    data_list = get_list_from_json(data_type)
    data_list.append(data)
    save_list_to_json(data_list, data_type)


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


def save_user_input(date_time, label, is_news, is_weather):
    """save the data from the form"""
    #if this is none, do not save because the rest is too
    if date_time is None:
        return
    full_date = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
    date = str(full_date.date())
    time = str(full_date.time())
    if is_news == "news":
        news = True
    else:
        news = False
    if is_weather == "weather":
        weather = True
    else:
        weather = False

    dictionary = {"date": date, "time": time, "label": label, "news": news, "weather": weather}
    add_data_to_json("user_input", dictionary)


def get_user_input():
    """get the data from the form"""
    date_time = request.args.get("alarm")
    print(date_time)
    label = request.args.get("two")
    print(label)
    is_news = request.args.get("news")
    print(is_news)
    is_weather = request.args.get("weather")
    print(is_weather)
    save_user_input(date_time, label, is_news, is_weather)