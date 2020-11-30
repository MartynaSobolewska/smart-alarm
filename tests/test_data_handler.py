"""This module tests the functions from the json_handler.py module
Be careful, it deletes the data from """
import pytest
import sys
sys.path.append(".")
from json_handler import add_data_to_json, get_list_from_json,clean_json, process_user_input


def test_add_data_to_json_1():
    """does the notification data save properly and is read properly?"""
    clean_json("notification")
    add_data_to_json("notification", {"title": "b", "content": "d"})
    assert get_list_from_json("notification") == [{"title": "b", "content": "d"}]
    clean_json("notification")

def test_add_data_to_json_2():
    """does it add a badly formatted dictionary?"""
    with pytest.raises(ValueError):
        add_data_to_json("alarm", {"caption": "a"})


def test_add_data_to_json_3():
    """does it take the wrong variable type input"""
    with pytest.raises(ValueError):
        add_data_to_json("xyz", {"title": "b", "content": "d"})


def test_add_data_to_json_4():
    """does it properly add two new dictionaries"""
    clean_json("notification")
    add_data_to_json("notification", {"title": "b", "content": "d"})
    add_data_to_json("notification", {"title": "b", "content": "d"})
    assert get_list_from_json("notification") == [{"title": "b", "content": "d"},{"title": "b", "content": "d"}]

def test_process_user_input_1():
    clean_json("alarm")
    process_user_input("2020-11-30T22:54", "xyz", "news", "")
    print(get_list_from_json("alarm"))
    assert get_list_from_json("alarm") == [{'date': '2020-11-30', 'time': '22:54:00', 'title': 'xyz', 'content': 'alarm set for 2020-11-30 at 22:54:00', 'news': True, 'weather': False}]

