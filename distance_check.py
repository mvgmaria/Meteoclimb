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

ccaas = []

input_ccaa = input("Por favor, seleccione una CCAA: ")
ccaas.append(input_ccaa)
while True:
    input_si_no = input("¿Quiere elegir otra CCAA, además de la anterior?")
    if input_si_no.lower() in ("sí", "si"):
        input_otra_ccaa = input("Por favor, seleccione otra CCAA: ")
        ccaas.append(input_otra_ccaa)
    if input_si_no.lower() == "no":
        break

input_km = input(
    "Por favor, introduzca el máximo de kilometros que se quiere desplazar: "
)

if len(ccaas) == 1:
    select_statement = f"SELECT region_name, crag_name, latitude,longitude FROM meteoclimb.crag_coords WHERE region_name = '{ccaas}';"
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
print(result)
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


# myloc = (myloc[0], myloc[1])
coords = crags_list


def main():
    delay = 1.5
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
    if distance < int(input_km):
        print(f"Distance in km: {int(distance)}")
        duration = summary["duration"]
        print(f"Duration in minutes: {int(duration / 60)}\n")
    else:
        print("This crag is out of the range.\n")


# if __name__ == "__main__":
#     main()
