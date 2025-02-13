import json
import sqlite3
from pprint import pprint

def json_to_db(): 

    # Ouverture du fichier json 
    file_journey = open('json/vehicle_journeys_sample.json')

    journey = json.load(file_journey)

    # Connexion à la base de donnée
    con = sqlite3.connect("db_sncf.db")
    cursor = con.cursor()

    id = 1
    for element in journey:
        for trip in element.get("vehicle_journeys", []):
            stop_times = trip.get("stop_times", [])

            departure_train_station = stop_times[0]["stop_point"]["name"]
            arrival_train_station = stop_times[-1]["stop_point"]["name"]

            cursor.execute('''
                SELECT 1 FROM line
                WHERE departure_train_station = ? AND arrival_train_station = ?
                ''', (departure_train_station, arrival_train_station))
                
            if not cursor.fetchone():

                fill_line(cursor, id, departure_train_station, arrival_train_station)
                id += 1
                pos = 0

                for stop_time in stop_times:
                    stop_point = stop_time["stop_point"]
                    station_name = stop_point["name"]
                    lon = stop_point["coord"]["lon"]
                    lat = stop_point["coord"]["lat"]
                    position = pos
                    fill_station(cursor, station_name, lon, lat, id, position)
                    pos += 1

    con.commit()     

    file_journey.close()
    cursor.close()
    con.close() 

def fill_line(cursor, id, departure_train_station, arrival_train_station):
    value = (id, departure_train_station, arrival_train_station)
    sql = "INSERT INTO line (id_line, departure_train_station, arrival_train_station) VALUES(?,?,?)"
    cursor.execute(sql, value)
    print("Insert in table line ---> id:",id," departure: ",departure_train_station," arrival: ", arrival_train_station)

def fill_station(cursor, station_name, lon, lat, id, position):

        value = (station_name, lon, lat, id, position)
        sql = "INSERT INTO station (name_station, longitude, latitude, id_line, position) VALUES(?,?,?,?,?)"
        cursor.execute(sql, value)
        print("Insert in table station ---> id: AUTOINCREMENT name_station: ", station_name,"AND longitude, latitude, position")

json_to_db()
