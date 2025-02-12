import json
import sqlite3
from pprint import pprint

# def json_to_db(): 

# Ouverture du fichier json 
file_journey = open('json/vehicle_journeys.json')

journey = json.load(file_journey)

# Connexion à la base de donnée
con = sqlite3.connect("db_sncf.db")
cursor = con.cursor()
"""
count2 = -1
count = -1
data = []
keep = 1
vehicle_journeys = "vehicle_journeys"
stop = 0
id = 1

while 1:
    count += 1
    keep = 0
    for vehicle_journeys in journey[count]:
        for i in journey[count]["vehicle_journeys"]:
            if count2 < 999:
                count2 += 1
            else:
                break
            while 1:
                departure_train_station = journey[count]["vehicle_journeys"][count2]["stop_times"][0]["stop_point"]["name"]
                arrival_train_station = journey[count]["vehicle_journeys"][count2]["stop_times"][-1]["stop_point"]["name"]
                value = (id, departure_train_station, arrival_train_station)
                sql = "INSERT INTO line (id_line, departure_train_station, arrival_train_station) VALUES(?,?,?)"
                print("Reussi",count," -->", count2, departure_train_station, arrival_train_station)

                cursor.execute(sql, value)
                id += 1
                keep = 1
                stop += 1
                if stop == 1:
                    break
            stop = 0
    count2 = 0
    con.commit()
    if keep == 0:    
        break

"""
file_journey.close
cursor.close
con.close


