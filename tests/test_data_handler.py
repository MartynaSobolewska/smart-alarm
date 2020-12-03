"""This module tests the functions from the json_handler.py module
Be aware it modifies data in json files."""
import pytest
import sys
from json_handler import add_data_to_json, get_list_from_json, \
    clean_json, save_new_notifications, delete_from_json,\
    save_list_to_json, process_user_input


def test_clean_json():
    """are the json files empty after calling the method"""
    add_data_to_json("notification", {"title": "Spotify artist pages hacked by Taylor Swift 'fan'",
                                     "content": "An apparent Taylor Swift..."})
    clean_json("notification")
    assert get_list_from_json("notification") == []


def test_add_notification_to_json():
    """does the notification data save properly and is read properly?"""
    clean_json("notification")
    add_data_to_json("notification", {"title": "Spotify artist pages hacked by Taylor Swift 'fan'",
                                      "content": "An apparent Taylor Swift..."})
    assert [{'title': "Spotify artist pages hacked by Taylor Swift 'fan'", 'content': 'An apparent Taylor Swift...'}] == get_list_from_json("notification")


def test_add_alarm_to_json():
    """does the alarm data save properly and is read properly?"""
    clean_json("alarm")
    add_data_to_json("alarm", {"date": "2020-12-04", "time": "13:18:00", "title": "xyz",
                               "content": "alarm set for 2020-12-04 at 13:18:00",
                               "news": True, "weather": False})
    assert  get_list_from_json("alarm") == [{"date": "2020-12-04", "time": "13:18:00", "title": "xyz",
                               "content": "alarm set for 2020-12-04 at 13:18:00",
                               "news": True, "weather": False}]


def test_save_new_notifications():
    """Is the amount of new notifications correct, are notifications saved in json file"""
    notifications = save_new_notifications()
    assert len(notifications) == 5
    assert notifications == get_list_from_json("notification")


def test_delete_from_json():
    """Is the data deleted properly from the alarms_data.json"""
    clean_json("alarm")
    add_data_to_json("alarm", {"date": "2020-12-04", "time": "13:18:00", "title": "xyz",
                               "content": "alarm set for 2020-12-04 at 13:18:00",
                               "news": True, "weather": False})
    add_data_to_json("alarm", {"date": "2020-12-04", "time": "13:19:00", "title": "abc",
                               "content": "alarm set for 2020-12-04 at 13:18:00",
                               "news": True, "weather": False})
    delete_from_json("alarm", {"date": "2020-12-04", "time": "13:18:00", "title": "xyz",
                               "content": "alarm set for 2020-12-04 at 13:18:00",
                               "news": True, "weather": False})
    assert get_list_from_json("alarm") == [{"date": "2020-12-04", "time": "13:19:00", "title": "abc",
                               "content": "alarm set for 2020-12-04 at 13:18:00",
                               "news": True, "weather": False}]


def test_save_list_to_json():
    """is saving lists of alarms working"""
    alarm_list = [{"date": "2020-12-04", "time": "13:18:00", "title": "xyz",
                    "content": "alarm set for 2020-12-04 at 13:18:00",
                    "news": True, "weather": False},
                  {"date": "2020-12-04", "time": "13:18:00", "title": "xyz",
                   "content": "alarm set for 2020-12-04 at 13:18:00",
                   "news": True, "weather": False},
                  {"date": "2020-12-04", "time": "13:18:00", "title": "xyz",
                   "content": "alarm set for 2020-12-04 at 13:18:00",
                   "news": True, "weather": False}]
    save_list_to_json(alarm_list, "alarm")
    assert get_list_from_json("alarm") == alarm_list


def test_process_user_input():
    """test if the input data is saved properly as an alarm"""
    clean_json("alarm")
    process_user_input("2021-01-04T13:18", "xyz", "news", "weather")
    print(get_list_from_json("alarm"))
    assert get_list_from_json("alarm") == [{'date': '2021-01-04', 'time': '13:18:00', 'title': 'xyz', 'content': 'alarm set for 2021-01-04 at 13:18:00', 'news': True, 'weather': True}]
