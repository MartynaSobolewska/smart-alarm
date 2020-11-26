"""This is a module containing functions for saving and retrieving data from json data files"""
import json
from flask import Flask, render_template, url_for, request
from typing import List, Dict

def save_alarms(alarms: List):
    """saves a list of dictionaries (data about alarms)
    to alarms_data.json file"""
    # dictionary formatting is checked in the add_alarm function
    # if the list is empty, just do not save.
    if not alarms:
        return
    with open("alarms_data.json", "w") as app_data_file:
        json.dump(alarms, app_data_file)


def add_alarm(alarm: Dict):
    """gets a list of dictionaries with the alarms data,
    adds a new alarm to the list and saves the extended list
    to alarms_data.json file"""
    # Make sure that the dictionary contains the needed keys.
    if not list(alarm.keys()) == ['title', 'content']:
        raise ValueError("Error: the dictionary formatting is wrong.")
    alarms = get_alarms()
    alarms.append(alarm)
    save_alarms(alarms)


def get_alarms():
    """returns a list of dictionaries that contain
    the alarm data from alarms_data.json"""
    with open("alarms_data.json", "r") as data_file:
        try:
            alarms = json.load(data_file)
        # the file might be empty, then this error will occur:
        except ValueError:
            # then return an empty list
            return []
    return alarms



def save_user_input(date_time, label, is_news, is_weather):
    """save the data from the form"""



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
    return
