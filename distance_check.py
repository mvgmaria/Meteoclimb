from dotenv import load_dotenv
import os
import requests
import mysql.connector
import time
import numpy as np
import plotly.express as px

load_dotenv(dotenv_path=".climbproject\.env")

api_key = os.getenv("API_KEY")
dbpssw = os.getenv("DB_KEY")

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd=dbpssw, database="meteoclimb"
)

mycursor = mydb.cursor()

ccaas = []

input_ccaa = input("Por favor, seleccione una CCAA: ")
ccaas.append(input_ccaa)
while True:
    input_si_no = input("¿Quiere elegir otra CCAA, además de la anterior? ")
    if input_si_no.lower() in ("sí", "si"):
        input_otra_ccaa = input("Por favor, seleccione otra CCAA: ")
        ccaas.append(input_otra_ccaa)
    if input_si_no.lower() == "no":
        break

while True:
    filter_input = input(
        "Do you want to input a max kilometer range ('km'), a max driving time range ('min'), or both?: \n"
    )
    if filter_input.lower() == "km":
        input_km = int(
            input(
                "Por favor, introduzca el máximo de kilometros que se quiere desplazar: "
            )
        )
        mins = False
        km = True
    elif filter_input.lower() == "min":
        input_min = int(
            input(
                "Por favor, introduzca el máximo de minutos que se quiere desplazar: "
            )
        )
        km = False
        mins = True
    else:
        input_km = int(
            input(
                "Por favor, introduzca el máximo de kilometros que se quiere desplazar: "
            )
        )
        input_min = int(
            input(
                "Por favor, introduzca el máximo de minutos que se quiere desplazar: "
            )
        )
        km = True
        mins = True
    break

if len(ccaas) == 1:
    select_statement = f"SELECT region_name, crag_name, latitude,longitude FROM meteoclimb.crag_coords WHERE region_name = '{input_ccaa}';"
else:
    count = len(ccaas)
    print(count)
    f_str = str(ccaas)[1:-1]
    print(f_str)
    ff_str = f_str.replace(",", " or region_name =", count - 1)
    print(ff_str)
    select_statement = f"SELECT region_name, crag_name, latitude,longitude FROM meteoclimb.crag_coords WHERE region_name = {ff_str};"
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


def main():
    delay = 2

    for coord in coords:
        coord_checked = dist(
            float(myloc[0]), float(myloc[1]), float(coord["lat"]), float(coord["lon"])
        )
        if int(coord_checked) > input_km:
            coords.remove(coord)
            print(f"Lineal distance out of range already, {coord['crg']} removed.")

    for coord in coords:
        print(f"Region name: {coord['reg']}")
        print(f"Crag name: {coord['crg']}")
        global parameters
        parameters = {
            "api_key": api_key,
            "start": f"{str(myloc[1])},{str(myloc[0])}",
            "end": f'{str(coord["lon"])},{str(coord["lat"])}',
        }

        distance_time_check()
        time.sleep(delay)


def distance_time_check():

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
    # print(summary)

    distance = summary["distance"] / 1000
    duration = summary["duration"] / 60

    if mins == False:
        if distance < input_km:
            print(f"This crag is in your distance range: {int(distance)} km.")

        else:
            print("The crag is out of your distance range.")

    if km == False:
        if duration < input_min:
            print(f"This crag is in your driving time range: {int(duration)} min.\n")
        else:
            print("The crag is out of your driving time range.\n")

    if km == True and mins == True:
        if distance < input_km:
            print(f"This crag is in your distance range: {int(distance)} km.")
            if duration < input_min:
                print(
                    f"The crag is also in your driving time range: {int(duration)} min.\n"
                )
            else:
                print("The crag is out of your driving time range.\n")
        else:
            print("This crag is out of your distance range.")
            if duration < input_min:
                print(
                    f"But it is within your driving time range: {int(duration)} min.\n"
                )
            else:
                print("The crag is also out of your driving time range.\n")


if __name__ == "__main__":
    main()
