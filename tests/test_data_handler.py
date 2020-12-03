"""This module tests the functions from the json_handler.py module
Be aware it modifies data in json files."""
import pytest
import sys
from json_handler import add_data_to_json, get_list_from_json, clean_json


def test_add_notification_to_json_1():
    """does the notification data save properly and is read properly?"""
    clean_json("notification")
    add_data_to_json("notification", {"title": "Spotify artist pages hacked by Taylor Swift 'fan'",
                                      "content": "An apparent Taylor Swift fan defaced the artist pages for Lana Del Ray and Dua Lipa, among others."})
    assert [{'title': "Spotify artist pages hacked by Taylor Swift 'fan'", 'content': 'An apparent Taylor Swift fan defaced the artist pages for Lana Del Ray and Dua Lipa, among others.'}] == get_list_from_json("notification")

test_add_notification_to_json_1()