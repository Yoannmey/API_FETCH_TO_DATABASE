import json
import sqlite3

def json_to_db_first(): 

    
    file_journey = open("json/vehicle_journeys.json")
    journey = json.load(file_journey)

    file_disruption = open("json/disruptions.json")
    disrupt = json.load(file_disruption)

    con = sqlite3.connect("db_sncf_v5.db")
    cursor = con.cursor()

    id = 1
    for element in journey: # Recherche du dictionnaire journeys dans le fichier vehicle_journeys et remplissage de la db
        for trip in element.get("vehicle_journeys", []):
            stop_times = trip.get("stop_times", [])
            trip_info = trip.get("trip", [])
            calendar = trip.get("calendars", [])
            disruption = trip.get("disruptions", [])

            departure_train_station = stop_times[0]["stop_point"]["name"]
            arrival_train_station = stop_times[-1]["stop_point"]["name"]

            cursor.execute(''' 
                SELECT 1 FROM line
                WHERE departure_train_station = ? AND arrival_train_station = ?
                ''', (departure_train_station, arrival_train_station)) # Verification pour eviter les doublons 
                
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

            departure_time = stop_times[0]["departure_time"]
            arrival_time = stop_times[-1]["arrival_time"]
            train_number = trip_info["name"]

            if len(calendar) > 0:
                date = calendar[0]["active_periods"][0]["begin"]
            else:
                date = "NULL"
                
            if len(disruption) > 0:
                id_disruption = disruption[0]["id"]
            else:
                id_disruption = "NULL"
            
            cursor.execute('''
                SELECT 1 FROM train
                WHERE base_departure_time = ? AND base_arrival_time = ? AND train_number = ? AND departure_date = ? AND id_disruption = ? AND id_line = ?
                ''', (departure_time, arrival_time, train_number, date, id_disruption, id )) # Verification pour eviter les doublons 
                
            if not cursor.fetchone():

                fill_train(cursor, departure_time, arrival_time, train_number, date, id_disruption, id)

        for retard in element.get("disruptions",[]):  # Recherche du dictionnaire disruptions dans le fichier vehicle_journeys et remplissage de la db
            message = retard.get("messages", [])
            impacted = retard.get("impacted_objects", [])
            severity = retard.get("severity", [])

            id_disruption = retard["id"]

            cursor.execute('''
                SELECT 1 FROM disruption
                WHERE id_disruption = ?
                ''', (id_disruption,))

            if not cursor.fetchone():
    
                name_disruption = severity["name"]
                if len(message) > 0:  # Vérification que la liste n'est pas vide pour éviter une erreur
                    message_disruption = message[0]["text"]
                else:
                    message_disruption = "NULL"

                if "impacted_stops" in impacted[0]: # Vérification que l'objet exitse pour éviter une erreur
                    if "stop_time_effect" in impacted[0]["impacted_stops"][0]:
                        status = impacted[0]["impacted_stops"][0]["stop_time_effect"]
                    else:
                        status = "NULL"

                    if "amended_departure_time" in impacted[0]["impacted_stops"][0]:
                        departure_time_disruption = impacted[0]["impacted_stops"][0]["amended_departure_time"]
                    else:
                        departure_time_disruption = "NULL"

                    if "amended_arrival_time" in impacted[0]["impacted_stops"][-1]:
                                                                                                        arrival_time_disruption = impacted[0]["impacted_stops"][-1]["amended_arrival_time"]
                    else:
                        arrival_time_disruption = "NULL"

                else:
                    status = "NULL"
                    departure_time_disruption = "NULL"
                    arrival_time_disruption = "NULL"

                fill_disruption(cursor, id_disruption, name_disruption, message_disruption, status, departure_time_disruption, arrival_time_disruption)

    for element in disrupt: # Recherche de nouveaux id_disruption dans le fichier disruptions.json 
        for disruption in element.get("disruptions", []):

            cursor.execute('''
                SELECT 1 FROM disruption
                WHERE id_disruption = ?
                ''', (id_disruption,))

            if not cursor.fetchone():

                id_disruption = disruption["id"]
                name_disruption = disruption["severity"]["name"]
                status = disruption["status"]
                message_disruption = "NULL"
                departure_time_disruption = "NULL"
                arrival_time_disruption = "NULL"

                fill_disruption(cursor, id_disruption, name_disruption, message_disruption, status, departure_time_disruption, arrival_time_disruption)
    
    con.commit()

    file_journey.close()
    cursor.close()
    con.close()

def fill_line(cursor, id, departure_train_station, arrival_train_station): # Insert dans la table line

    value = (id, departure_train_station, arrival_train_station)
    sql = "INSERT INTO line (id_line, departure_train_station, arrival_train_station) VALUES(?,?,?)"
    cursor.execute(sql, value)
    print("Insert in table line ---> id:",id," departure: ",departure_train_station," arrival: ", arrival_train_station)

def fill_station(cursor, station_name, lon, lat, id, position): # Insert dans la table station

    value = (station_name, lon, lat, id, position)
    sql = "INSERT INTO station (name_station, longitude, latitude, id_line, position) VALUES(?,?,?,?,?)"
    cursor.execute(sql, value)
    print("Insert in table station ---> id: AUTOINCREMENT name_station: ", station_name,"AND longitude, latitude, position")

def fill_train(cursor, departure_time, arrival_time, train_number, date, id_disruption, id): # Insert dans la table train

    value = (departure_time, arrival_time, train_number, date, id_disruption, id)
    sql = "INSERT INTO train (base_departure_time, base_arrival_time, train_number, departure_date, id_disruption, id_line) VALUES(?,?,?,?,?,?)"
    cursor.execute(sql, value)
    print("Insert in table train ---> id: AUTOINCREMENT, base_departure_time, base_arrival_time, train_number, departure_date, id_disruption, id_line")

def fill_disruption(cursor, id_disruption, name_disruption, message_disruption, status, departure_time_disruption, arrival_time_disruption): # Insert dans la tzble disruption

    value = (id_disruption, name_disruption, status, message_disruption, departure_time_disruption, arrival_time_disruption)
    sql = "INSERT INTO disruption (id_disruption, name, status, message, amended_departure_time, amended_arrival_time) VALUES(?,?,?,?,?,?)"
    cursor.execute(sql, value)
    print("Insert in table disruption ---> id:", id_disruption, " name_disruption, status, message_disruption, departure_time_disruption, arrival_time_disruption")

