from uk_covid19 import Cov19API
import requests
import json

with open("config.json") as f:
    keys = json.load(f)

def weather_api():
    city_name = input("Enter a city name: ")
    api_key = keys['API keys']['weather']
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city_name, api_key)
    weather_data = requests.get(url).json()
    return weather_data

def news_api():
    api_key = keys['API keys']['news']
    url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={}".format(api_key)
    news_data = requests.get(url).json()
    return news_data


def covid_api():
    list_of_countries_filters = []
    countries = ["England", "Scotland", "Northern Ireland", "Wales"]

    for country in countries:
        list_of_countries_filters.append(
            [
                'areaType=region',
                'areaName={}'.format("Devon")
            ]
        )
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }

    apis = {}
    for i in range(len(list_of_countries_filters)):
        country=Cov19API(filters=list_of_countries_filters[i], structure=cases_and_deaths).get_json()
        apis[countries[i]] = country

    print(apis['England'])


covid_api()
