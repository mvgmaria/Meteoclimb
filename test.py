from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".climbproject\.env")

api_key = os.getenv("API_KEY")

import requests

mostoles = (40.3231228, -3.8882308)
sharma = (40.4377515, -3.6250799)

parameters = {
    "api_key": api_key,
    "start": "{},{}".format(mostoles[1], mostoles[0]),
    "end": "{},{}".format(sharma[1], sharma[0]),
}

response = requests.get(
    "https://api.openrouteservice.org/v2/directions/driving-car", params=parameters
)

if response.status_code == 200:
    print("Request successful.")
    data = response.json()
else:
    print("Request failed.")

data = response.json()

summary = data["features"][0]["properties"]["summary"]
print(summary)

duration = summary["duration"]
print(duration / 60)

distance = summary["distance"]
print(distance / 1000)
