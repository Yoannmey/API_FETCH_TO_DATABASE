from API_to_json import *
from sql_create import *
from json_to_db import *

try: # Vérification de l'existance du fichier json, importation depuis l'API si il n'existe pas 
    with open('json/vehicle_journeys.json') as file:
       print("vehcile_journeys.json a été trouvé")
except FileNotFoundError: 
    journeys_to_json()
    print("Importation de vehicle_journeys.json en cours")

try: # Vérification de l'existance du fichier json, importation depuis l'API si il n'existe pas 
    with open('json/disruptions.json') as file:
       print("disruptions.json a été trouvé")
except FileNotFoundError: 
    disruptions_to_json()
    print("Importation de disruptions.json en cours")

try: # Vérification de l'existance de la base de donnée, exécution du script sql, et du script d'insert si elle n'existe pas
    with open('db_sncf.db') as file:
       print("La database a été trouvée")
except FileNotFoundError: 
    print("Création de la database, et insertion des données...")
    create_sql()
    json_to_db_first()
    print("Terminé")
    

