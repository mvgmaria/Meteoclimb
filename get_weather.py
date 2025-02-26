import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint

load_dotenv(dotenv_path=".climbproject\.env")


# enables the env variables so we can retrieve them
def get_weather(lat, lon):

    date = input(
        "Introduzca qué día va a escalar: "
    )  # 21 (its implicit that this day is from the current month or the one immediately after, but beware of possible bugs in the last days of the month, check that cases"
    cnt = (
        int(date) - datetime.now().day
    )  # i would have to check the format of the datetime function
    print(cnt)

    request_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv("API_KEY_W")}'

    weather_data = requests.get(request_url).json()

    pprint(weather_data)

    # print(f'\nCurrent Weather for {weather_data["name"]}.')
    # print(f'\nThe temp is {weather_data["main"]["temp"]}.')
    # print(
    #     f'\nFeels like {weather_data["main"]["feels_like"]} and {weather_data["weather"][0]["description"]}.'
    # )


if __name__ == "__main__":
    get_weather(
        40.3202739, -3.8796409
    )  # to make tests, remember i have to manually update the arguments in this line
