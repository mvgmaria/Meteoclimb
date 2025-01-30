# entorno de test para no sobrecargar las requests de ORS y IPinfo
from dotenv import load_dotenv
import os
import requests
import mysql.connector
import time

load_dotenv(dotenv_path=".climbproject\.env")

dbpssw = os.getenv("DB_KEY")

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd=dbpssw, database="meteoclimb"
)

mycursor = mydb.cursor()

mycursor.execute(
    "SELECT latitude,longitude FROM meteoclimb.crag_coords WHERE region_name = 'Andalucía';"
)

result = mycursor.fetchall()

print(result)
print(type(result))
