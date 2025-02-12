from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".climbproject\.env")


print(response.status_code)
nearest_point = data["features"][0]["geometry"]["coordinates"]

parameters = {
    "api_key": api_key,
    "start": f"{str(myloc[1])},{str(myloc[0])}",
    "end": f"{str(nearest_point[0])},{str(nearest_point[1])}",
}

response = requests.get(
    "https://api.openrouteservice.org/v2/nearest/driving-car",
    params=parameters_,
)

print(response.status_code)

data = response.json()

summary = data["features"][0]["properties"]["summary"]
