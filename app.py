from dotenv import load_dotenv
import os
import requests
import mysql.connector
import time
from datetime import datetime
import numpy as np
from get_weather import get_weather
from flask_mysqldb import MySQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from pprint import pprint


# Configure application
app = Flask(__name__, template_folder="templates")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# update the .demo_env with your own api_keys (they are all free for Open Route Service and Open Weather)
# actualiza el archivo .demo_env con tus propias api_keys (son gratis para Open Route Service y Open Weather)
load_dotenv(dotenv_path=".climbproject\\.demo_env")

api_key = os.getenv("API_KEY")
dbpssw = os.getenv("DB_KEY")


# make sure you have created the database and table with the query from test_crags.sql
# asegúrate de que has creado la base de datos y la tabla correspondiente con el query de test_crags.sql

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = dbpssw
app.config["MYSQL_DB"] = "flask"

db = MySQL(app)

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd=dbpssw, database="meteoclimb"
)

mycursor = mydb.cursor()


# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response


@app.route("/", methods=["GET", "POST"])
def indx():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def index():

    ccaas = []

    if request.method == "POST":
        ccaas = request.form.get("region")
        if "," not in ccaas:
            ccaas = ccaas.strip()
            select_statement = f"SELECT region_name, crag_name, latitude,longitude FROM meteoclimb.test_crags WHERE region_name = '{ccaas}' LIMIT 3;"
        else:
            new_ccaas = ccaas.replace(", ", ",")
            new_ccaas = ccaas.replace(",", "' OR region_name = '")
            new_ccaas = f"'{new_ccaas}'"
            select_statement = f"SELECT region_name, crag_name, latitude,longitude FROM meteoclimb.test_crags WHERE region_name = {new_ccaas} LIMIT 3;"
            print(select_statement)

        mycursor.execute(select_statement)

        # this returns a list with the coordinates of the selected crag/s
        result = mycursor.fetchall()
        # print(result)
        counter = 0
        crags_list = []
        crags_dict = {"reg": [], "crg": [], "lat": [], "lon": []}
        for row in result:
            crags_dict["reg"] = result[counter][0]
            crags_dict["crg"] = result[counter][1]
            crags_dict["lat"] = result[counter][2]
            crags_dict["lon"] = result[counter][3]
            counter += 1
            crags_list.append(crags_dict)
            crags_dict = {"reg": [], "crg": [], "lat": [], "lon": []}

        # print(crags_list)

        response = requests.get("https://ipinfo.io/json")
        mydata = response.json()
        myloc = mydata["loc"].split(",")

        coords = crags_list

        km = False
        mins = False

        if request.form.get("distance") != "":
            km = True

            # earth radius in km
            R = 6371

            def deg_to_rad(degrees):
                return degrees * (np.pi / 180)

            # function to calculate distance (1 or 2 could correspond to either of the locations)
            def dist(lat1, lon1, lat2, lon2):

                # d stands for 'difference' in lat and in lon
                d_lat = deg_to_rad(lat2 - lat1)
                d_lon = deg_to_rad(lon2 - lon1)
                a = (
                    np.sin(d_lat / 2) ** 2
                    + np.cos(deg_to_rad(lat1))
                    * np.cos(deg_to_rad(lat2))
                    * np.sin(d_lon / 2) ** 2
                )
                c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
                return R * c

        if request.form.get("time") != "":
            mins = True

        date = request.form.get("date")

        delay = 2

        time_range = True
        distance_range = True

        def main():
            global crags
            crags = []
            if km == True:

                coords_reduced = coords[:]
                for coord_ in coords:
                    coord_checked = dist(
                        float(myloc[0]),
                        float(myloc[1]),
                        float(coord_["lat"]),
                        float(coord_["lon"]),
                    )
                    if int(coord_checked) > int(request.form.get("distance")):
                        coords_reduced.remove(coord_)
                        # print(f"Lineal distance out of range already, {coord_['crg']} removed.")

                global coord
                if len(coords_reduced) > 0:

                    for coord in coords_reduced:
                        print("coord searching")
                        print(f"Region name: {coord['reg']}")
                        print(f"Crag name: {coord['crg']}\n")
                        # global parameters
                        parameters = {
                            "api_key": api_key,
                            "start": f"{str(myloc[1])},{str(myloc[0])}",
                            "end": f'{str(coord["lon"])[:-6]},{str(coord["lat"])[:-6]}',
                        }

                        distance_time_check(parameters)
                        time.sleep(delay)
                        global distance_range

                        if mins == False and distance_range == True:
                            get_weather(str(coord["lat"]), str(coord["lon"]), date)
                            print("Appending")
                            crags.append(
                                {
                                    "region": coord["reg"],
                                    "crag_name": coord["crg"],
                                    "distance": round(distance),
                                    "time": round(duration),
                                    "weather": wdata,
                                }
                            )
                        elif mins == True and (
                            distance_range == True or time_range == True
                        ):
                            get_weather(str(coord["lat"]), str(coord["lon"]), date)
                            print("Appending")
                            crags.append(
                                {
                                    "region": coord["reg"],
                                    "crag_name": coord["crg"],
                                    "distance": round(distance),
                                    "time": round(duration),
                                    "weather": wdata,
                                }
                            )
            elif km == False:
                for coord in coords:
                    print(f"Region name: {coord['reg']}")
                    print(f"Crag name: {coord['crg']}\n")

                    # global parameters
                    parameters = {
                        "api_key": api_key,
                        "start": f"{str(myloc[1])},{str(myloc[0])}",
                        "end": f'{str(coord["lon"])[:-6]},{str(coord["lat"])[:-6]}',
                    }

                    distance_time_check(parameters)
                    time.sleep(delay)

                    if mins == True and time_range == True:
                        get_weather(str(coord["lat"]), str(coord["lon"]), date)
                        print("Appending")
                        crags.append(
                            {
                                "region": coord["reg"],
                                "crag_name": coord["crg"],
                                "distance": round(distance),
                                "time": round(duration),
                                "weather": wdata,
                            }
                        )
                    else:
                        get_weather(str(coord["lat"]), str(coord["lon"]), date)
                        print("Appending")
                        crags.append(
                            {
                                "region": coord["reg"],
                                "crag_name": coord["crg"],
                                "distance": round(distance),
                                "time": round(duration),
                                "weather": wdata,
                            }
                        )

            print(f"dictionary: {crags}")
            # print(f"Skipped crags (out of lineal range): {skipped_crags}")

        def distance_time_check(parameters):

            response = requests.get(
                "https://api.openrouteservice.org/v2/directions/driving-car",
                params=parameters,
            )

            if response.status_code == 200:
                print("Request successful.\n")

            else:
                shift = 0.01
                while True:
                    print("Request failed. Retrying...\n")
                    newlon = float(str(coord["lon"])[:-6]) + shift
                    newlat = float(str(coord["lat"])[:-6]) + shift
                    parameters = {
                        "api_key": api_key,
                        "start": f"{str(myloc[1])},{str(myloc[0])}",
                        "end": f"{str(newlon)},{str(newlat)}",
                    }

                    response = requests.get(
                        "https://api.openrouteservice.org/v2/directions/driving-car",
                        params=parameters,
                    )
                    # print(response.status_code)
                    if response.status_code == 404:
                        shift += 0.03  # can be adapted if the search is bigger
                        time.sleep(delay)
                    else:
                        break

            data = response.json()

            summary = data["features"][0]["properties"]["summary"]
            # print(summary)

            global distance
            global duration

            distance = summary["distance"] / 1000
            duration = summary["duration"] / 60

            global distance_range
            global time_range
            distance_range = False
            time_range = False

            if mins == False and km == True:
                if distance < int(request.form.get("distance")):
                    distance_range = True
                    print(f"This crag is in your distance range: {int(distance)} km.")
                else:

                    distance_range = False
                    print("The crag is out of your distance range.")

            elif km == False and mins == True:
                if duration < int(request.form.get("time")):
                    time_range = True
                    print(
                        f"This crag is in your driving time range: {int(duration)} min.\n"
                    )
                else:
                    time_range = False
                    print("The crag is out of your driving time range.\n")

            elif km == True and mins == True:
                if distance < int(request.form.get("distance")):
                    distance_range = True
                    print(f"This crag is in your distance range: {int(distance)} km.")
                    if duration < int(request.form.get("time")):
                        time_range = True
                        print(
                            f"The crag is also in your driving time range: {int(duration)} min.\n"
                        )
                    else:
                        time_range = False
                        print("The crag is out of your driving time range.\n")
                else:
                    print("This crag is out of your distance range.")
                    if duration < int(request.form.get("time")):
                        time_range = True
                        print(
                            f"But it is within your driving time range: {int(duration)} min.\n"
                        )
                    else:
                        time_range = False
                        print("The crag is also out of your driving time range.\n")
            elif mins == False and km == False:
                distance_range = True
                time_range = True

        def get_weather(lat, lon, date):
            global wdata
            timestamps_cons = 8

            timestamp_times = [3, 6, 9, 12, 15, 18, 21, 24]
            for hour in timestamp_times:
                if datetime.now().hour < hour:
                    next_timestamp = timestamp_times.index(hour)
                    break

            if next_timestamp < 7:
                timestamps_needed = timestamps_cons * int(date) + (
                    timestamps_cons - (next_timestamp + 1)
                )

            else:
                timestamps_needed = timestamps_cons * date

            if timestamps_needed < 40:
                request_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv("API_KEY_W")}&units=metric&cnt={timestamps_needed}'
            else:
                request_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv("API_KEY_W")}&units=metric&cnt=40'
            # with the parameter cnt im limiting the timestamps (every three hours)

            wdata = []

            weather_data = requests.get(request_url).json()
            for i in range(5, 0, -1):
                wd = f'Para la fecha y hora {weather_data["list"][timestamps_needed-i]["dt_txt"]}, la sensación térmica es de {weather_data["list"][timestamps_needed-i]["main"]["feels_like"]} y la probabilidad de precipitación es de {weather_data["list"][timestamps_needed-i]["pop"]}%.'
                wdata.append(wd)
            print(wdata)

            # here, the 0 gets the first element of the list, so the first timestamp

            print("\n")

        main()

        return render_template("crags.html", crags=crags)

    return render_template("search.html")
