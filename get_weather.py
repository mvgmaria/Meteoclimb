import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint

load_dotenv(dotenv_path=".climbproject\.env")


# enables the env variables so we can retrieve them
def get_weather(lat, lon, date):

    timestamps_cons = 8

    timestamp_times = [3, 6, 9, 12, 15, 18, 21, 24]
    for hour in timestamp_times:
        if datetime.now().hour < hour:
            next_timestamp = timestamp_times.index(hour)
            break

    if next_timestamp < 7:
        timestamps_needed = timestamps_cons * date + (
            timestamps_cons - (next_timestamp + 1)
        )

    else:
        timestamps_needed = timestamps_cons * date

    if timestamps_needed < 40:
        request_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv("API_KEY_W")}&units=metric&cnt={timestamps_needed}'
    else:
        request_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv("API_KEY_W")}&units=metric&cnt=40'
    # with the parameter cnt im limiting the timestamps (every three hours)

    weather_data = requests.get(request_url).json()

    # pprint(weather_data)

    for i in range(5, 0, -1):
        wdata = f'\nPara la fecha y hora {weather_data["list"][timestamps_needed-i]["dt_txt"]}, la sensación térmica es de {weather_data["list"][timestamps_needed-i]["main"]["feels_like"]} y la probabilidad de precipitación es de {weather_data["list"][timestamps_needed-i]["pop"]}%.'
        print(wdata)

    # here, the 0 gets the first element of the list, so the first timestamp

    print("\n")


if __name__ == "__main__":
    get_weather(
        40.3202739, -3.8796409, 1
    )  # to make tests, remember i have to manually update the arguments in this line
