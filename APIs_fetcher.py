"""Module containing methods to fetch data from APIs"""

from uk_covid19 import Cov19API
import requests
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#load keys needed to access APIs
with open("data/config.json") as f:
    config = json.load(f)

def weather_api(city_name):
    """function fetching data from the open weather API.
    It returns weather data for a given city in form of json formatted as on the example:
        {
          'coord': {
            'lon': -3.53,
            'lat': 50.72
          },
          'weather': [
            {
              'id': 803,
              'main': 'Clouds',
              'description': 'broken clouds',
              'icon': '04d'
            }
          ],
          'base': 'stations',
          'main': {
            'temp': 9.65,
            'feels_like': 8.39,
            'temp_min': 8.89,
            'temp_max': 10,
            'pressure': 1018,
            'humidity': 87
          },
          'visibility': 10000,
          'wind': {
            'speed': 1,
            'deg': 0
          },
          'clouds': {
            'all': 75
          },
          'dt': 1606913835,
          'sys': {
            'type': 1,
            'id': 1472,
            'country': 'GB',
            'sunrise': 1606895757,
            'sunset': 1606925507
          },
          'timezone': 0,
          'id': 2649808,
          'name': 'Exeter',
          'cod': 200
        }
    """
    api_key = config['API keys']['weather']
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(city_name, api_key)
    weather_data = requests.get(url).json()
    return weather_data

def news_api():
    """Fetches top BBC articles from the news API and returns it in a form of json file formatted as the example:
    {
      'status': 'ok',
      'totalResults': 10,
      'articles': [
        {
          'source': {
            'id': 'bbc-news',
            'name': 'BBC News'
          },
          'author': 'BBC News',
          'title': "Spotify artist pages hacked by Taylor Swift 'fan'",
          'description': 'An apparent Taylor Swift fan defaced the artist pages for Lana Del Ray and Dua Lipa, among others.',
          'url': 'http://www.bbc.co.uk/news/technology-55158317',
          'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_news/12F62/production/_115766677_dualipa_hacked.jpg',
          'publishedAt': '2020-12-02T12:52:20.5708095Z',
          'content': "Some of the world's most popular singers have had their Spotify pages hacked and defaced by an apparent Taylor Swift fan.\r\nOn Wednesday, artists including Lana Del Rey and Dua Lipa had their biograph… [+1578 chars]"
        },
        {
          'source': {
            'id': 'bbc-news',
            'name': 'BBC News'
          },
          'author': 'BBC News',
          'title': "Ethiopia and UN 'reach Tigray aid deal'",
          'description': 'Food and medicines are said to be running out for millions of people in the conflict-torn region.',
          'url': 'http://www.bbc.co.uk/news/world-africa-55158182',
          'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_news/13F5C/production/_115765718_mediaitem115765717.jpg',
          'publishedAt': '2020-12-02T11:22:22.8376767Z',
          'content': "image captionMany refugees have crossed over into Sudan to escape the conflict\r\nThe United Nations and Ethiopia have reached a deal to allow aid into the country's conflict-torn northern Tigray regio… [+802 chars]"
    }, ...}
    """
    api_key = config['API keys']['news']
    url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={}".format(api_key)
    news_data = requests.get(url).json()
    if news_data["status"] != "ok":
        logger.error("Unwanted response '{}' from news API.".format(news_data["status"]))
    else:
        logger.info("Successful connection with news API.")
    return news_data


def covid_api(city: str):
    """A function fetching data from Covid-19 API
    It returns a dictionary with countries in GB and City specified in config.json file
    as keys and data about covid as values.
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
        try:
            country=Cov19API(filters=list_of_countries_filters[i], structure=cases_and_deaths).get_json()
        except:
            logger.error("Encountered problem while trying to retrieve data from covid api.")
        apis[countries[i]] = country
    try:
        apis[city] = Cov19API(filters=city_filter, structure=cases_and_deaths).get_json()
    except:
        logger.error("Encountered problem while trying to retrieve data from covid api.")

    return apis