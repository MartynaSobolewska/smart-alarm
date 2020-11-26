"""This module tests the functions from the json_handler.py module
Be careful, it deletes the data from """
import pytest
import sys
sys.path.append(".")
from json_handler import add_data_to_json, get_list_from_json,clean_json


def test_add_data_to_json_1():
    """does the alarm data save properly and is read properly?"""
    clean_json("alarm")
    add_data_to_json("alarm", {"title": "b", "content": "d"})
    assert get_list_from_json("alarm") == [{"title": "b", "content": "d"}]
    clean_json("alarm")

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
    clean_json("alarm")
    add_data_to_json("alarm", {"title": "b", "content": "d"})
    add_data_to_json("alarm", {"title": "b", "content": "d"})
    assert get_list_from_json("alarm") == [{"title": "b", "content": "d"},{"title": "b", "content": "d"}]