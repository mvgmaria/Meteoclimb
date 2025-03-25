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
    return render_template("search.html")
