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
import distance_check

# Configure application
app = Flask(__name__, template_folder="templates")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

load_dotenv(dotenv_path=".climbproject\.env")

dbpssw = os.getenv("DB_KEY")

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
    if request.method == "POST":
        if len(ccaas) == 1:
            select_statement = f"SELECT region_name, crag_name, latitude,longitude FROM meteoclimb.crag_coords WHERE region_name = '{input_ccaa}';"
        else:
            ccaas = [request.get.form("region")]
            count = len(ccaas)
            f_str = str(ccaas)[1:-1]
            ff_str = f_str.replace(",", " or region_name =", count - 1)
            select_statement = f"SELECT region_name, crag_name, latitude,longitude FROM meteoclimb.crag_coords WHERE region_name = {ff_str};"
        
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
                + np.cos(deg_to_rad(lat1)) * np.cos(deg_to_rad(lat2)) * np.sin(d_lon / 2) ** 2
            )
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
            return R * c


        delay = 2

        skipped_crags = 0

        weather_api_counter = 0
        distance_api_counter = 0
        time_range = True
        distance_range = True

        distance_check.main()


    return render_template("search.html")
