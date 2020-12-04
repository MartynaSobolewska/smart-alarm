# README for smart alarm
### Purpose
Smart alarm is a project aiming to give an easy access to reliable news and data. It allows user to schedule alarms with customized contents such as information about covid-19 or weather. The alarms are read out loud when scheduled while the notifications pop out on the right side of the screen and are refreshed every hour.
### Prerequisites
Python version: 3.0 +\
Windows tts module installed for English language\
Web browser other than Firefox
### Installation
#### module dependencies
to install module dependencies type those commands in the terminal:\
pip install sched\
pip install pyttsx3\
pip install uk_covid19\
pip install requests\
pip install python-dateutil\
pip install flask\
For testing:\
pip install pytest
#### API keys
for the news to be fetched, the program must be provided with API keys. 
To get them, go to:\
https://openweathermap.org/api and subscribe to Current Weather Data API.\
https://newsapi.org/ and get API key\
Open config.json file that you will find in data folder and paste API keys in fields provided.
#### location setup
In config.json type any UK city name to set it as user's location.

### Getting started
To run the server, type "python alarm.py" in the terminal and go to http://127.0.0.1:5000/. 
After opening the main page, the notifications pop up on the right hand side of the screen.
Notifications contain newest articles from BBC news, information on the local weather and brief summary of new covid-19 cases in the UK.
Alarms will be displayed on the left side of the screen but since no alarm has been set yet, nothing is displayed.
To set an alarm, fill out the form in the middle of the screen. To choose date, click on calendar button and pick it from there.
Choose the title of your alarm and check the additional information that you want your alarm to contain.
By default, the alarm only contains newest information about covid-19 cases. Click submit.
The alarm should appear on the left side of the screen. It is now scheduled to read newest information at time and date specified.
To cancel the alarm, simply click the x button. You can also hide notifications by clicking x button.

### Testing
In order to test, type pytest in the terminal. To add more tests, create more test modules in tests file or add new functions to preexisting ones.
### Developer documentation
The project consists of three main modules: alarm.py, apis_fetcher.py and json_handler.py each serving specific set of tasks.
#### alarm.py
Main module handling scheduling and Flask loading in two threads. It also initializes the logger.
It uses apis_fetcher to fill out the html forms with relevant news and json_handler to save alarms or temp news data.

It's functions are:

def schedule_all_alarms() -> None:\
    """gets all alarms from the alarms.json file and schedules them
    making sure none are scheduled for the past.
    Runs the scheduler."""
    
    
def delete_alarms_in_the_past() -> None:\
    """Finds alarms that are set in the past and deletes them from json file"""
    
    
def tts_request(announcement="Text to speech example announcement!") -> None:\
    """Reads the message specified in parameter"""
    
    
def fill_out_the_form():\
    """fills out the form with data from json files, refreshes the notifications
    if they have not been refreshed for over an hour. Returns the filled out form"""    
    
    
def get_delay(date: str, time_str: str) -> int:\
    """Returns the difference in second between the given parameter and current time"""

def delete_an_object() -> None:\
    """Finds an object to be deleted based on the current URL
     and uses a method from a json_handler.py to delete it"""

def index():\
    """renders the html form and listens for user trying to delete an object."""

def form():
    """Renders the html form for the homepage."""

def run_sched() -> None:
    """Starts a scheduler."""

#### apis_fetcher.py
Module containing functions that return the data fetched from APIs.

It's functions are:

def weather_api(city_name):\
    """Fetches the data from the open weather API.
    It returns weather data for a given city in form of json"""
    
def news_api():
    """Fetches top BBC articles from the news API and returns it
    in a form of json file"""
    
def covid_api(city: str):
    """Fetches data from Covid-19 API
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
    is the cumulative number of cases in England until yesterday.
    """
    
####json_handler.py
Module containing functions for saving and retrieving data from json data files.

It's functions are:

def get_list_from_json(data_type: str):\
    """returns a list of dictionaries that contain
    the alarm data from alarms_data.json"""

def save_new_notifications():\
    """Gets a list of notifications containing: 3 latest BBC articles every 12h,
    Current weather info for city specified in config.json file
    COVID-19 cases data from yesterday.
    News articles and COVID-19 data are temporarily stored in json files
    and updated when needed."""

def clean_json(data_type: str):\
    """deletes all the data from the json corresponding to the data type.
    data_type is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored."""
    
def delete_from_json(data_type: str, data_object: dict):\
    """looks for a corresponding object in the list fetched from json and, if found,
     deletes it and saves an updated list"""
     
def save_list_to_json(data: List[dict], data_type: str):\
    """saves a list of dictionaries to a json file.
    data_type is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored."""
    
def add_data_to_json(data_type: str, data: Dict):\
    """gets a dictionary with the data,
    and a data_type which is a string corresponding to key of the dictionary "data_types",
    where the names of json files for each data type are stored.
    adds a new alarm to the list and saves the extended list
    to alarms_data.json file"""

def process_user_input(date_time, label, is_news, is_weather):\
    """process the data gathered from the form in a way that it can be saved to alarms.json file
    Check if the inputs are correct,
    If they are, save the alarm."""

def get_user_input():\
    """get the data from the form"""

def get_alarm_content(alar: dict):\
    """Based on what user wanted to be informed about, create a message to be read."""

def trigger_alarm(alarm_dict: dict):\
    """At scheduled time, fetch up-to-date data to inform user and read it out loud."""

### Details
Programming language: Python
Github repository: https://github.com/MartynaSobolewska/smart-alarm
Authors: Matt Collison, Martyna Sobolewska
License:: OSI approved :: MIT license
