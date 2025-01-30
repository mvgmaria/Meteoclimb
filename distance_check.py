from dotenv import load_dotenv
import os
import requests
import mysql.connector
import time

load_dotenv(dotenv_path=".climbproject\.env")

api_key = os.getenv("API_KEY")
dbpssw = os.getenv("DB_KEY")

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd=dbpssw, database="meteoclimb"
)

mycursor = mydb.cursor()

mycursor.execute(
    "SELECT latitude,longitude FROM meteoclimb.crag_coords WHERE region_name = 'Andalucía';"
)

# this returns a list with the coordinates of the andalucía crags
result = mycursor.fetchall()


response = requests.get("https://ipinfo.io/json")
mydata = response.json()
myloc = mydata["loc"].split(",")

myloc = (myloc[0], myloc[1])
sharma = (40.4377515, -3.6250799)

parameters = {
    "api_key": api_key,
    "start": "{},{}".format(myloc[1], myloc[0]),
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
print(int(duration / 60))

distance = summary["distance"]
print(int(distance / 1000))
