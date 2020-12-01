"""Module containing methods to fetch data from APIs"""

from uk_covid19 import Cov19API
import requests
import json
from datetime import datetime, timedelta

#load keys needed to access APIs
with open("data/config.json") as f:
    config = json.load(f)

def weather_api(city_name):
    """function fetching data from the open weather API.
    It returns weather data for a given city in form of json"""
    api_key = config['API keys']['weather']
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(city_name, api_key)
    weather_data = requests.get(url).json()
    return weather_data

def news_api():
    api_key = config['API keys']['news']
    url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={}".format(api_key)
    news_data = requests.get(url).json()
    return news_data


def covid_api(city: str):
    """A function fetching data from Covid-19 API
    It returns a dictionary with countries in GB as keys
    and data about covid as values.
    Data contains such information:
    "date","areaName","areaCode","newCasesByPublishDate",
    "cumCasesByPublishDate","newDeathsByDeathDate",
    "cumDeathsByDeathDate","cumDeathsByDeathDate"
    to access this information:
    api["country"]["data"][days since data gained]["information you want to access"]
    where 0 stands for the most recent data in days since data gained.
    example:
    england_covid = APIs_fetcher.covid_api()["England"]['data'][0]['cumCasesByPublishDate']
    is the cumulative number of cases in England until yesterday

    """
    # create a filter for each counry in the UK
    list_of_countries_filters = []
    countries = ["England", "Scotland", "Northern Ireland", "Wales"]

    for country in countries:
        list_of_countries_filters.append(
            [
                'areaType=nation',
                'areaName={}'.format(country),
                'date={}'.format(datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d"))
            ]
        )
    # create a filter for the city from config.json file
    city_filter = [
        'areaName={}'.format(city),
        'date={}'.format(datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d"))
    ]
    cases_and_deaths = {
        "date": "date",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }

    apis = {}
    for i in range(len(list_of_countries_filters)):
        country=Cov19API(filters=list_of_countries_filters[i], structure=cases_and_deaths).get_json()
        apis[countries[i]] = country

    apis[city] = Cov19API(filters=city_filter, structure=cases_and_deaths).get_json()

    return apis