# API_FETCH_TO_DATABASE

## Description 

API_FETCH_TO_DB est un programme qui effectu plusieurs actions:

- Télécharge les donnés de l'API de la sncf vers des JSON

- Vérifie et créer au besoin une database en SQLITE

- Rentre les données nécessaires du JSON dans la database

## Installation 

API_FETCH_TO_DB a besoin de **python3** pour fonctionner, ainsi que de plusieurs librairies:
- La lib requests, pour pouvoir intéragir avec l'API 

- La lib json, pour pouvoir lire et écrire dans les fichiers .json

- la lib sqlite3, pour exécuter et insérer dans des database en SQLITE

## API_to_json 

Le fichier API_to_json contient 2 fonctions:

- journey_to_json 

- disruptions_to_json

### journey_to_json 

La fonction journey_to_json utilise les librairies susmentionnée: requests et json 

Grâce à requests elle va pouvoir intérroger l'API et insérer les données du fichier vehicle_journeys dans la variable data

Ensuite, grâce à la lib json la fonction va écrire et intenter au format json les données 

### disruptions_to_json

La fonction disruptions_to_json utilise les même librairies que journey_to_json et a le même fonctionnement

La seule différence est qu'elle va chercher les données disruptions et non de vehicle_journeys 

## sql_create

Le fichier sql_create ne contient qu'une seule fonction : create_sql

Cette fonction utilise la librairie sqlite3, elle permet d'éxecuter du code sqlite

Elle va donc créer une database grâce à un code sqlite généré avec l'outil **looping**, en fonction des besoins de la future

base de donnée

## main.py 

Le fichier main.py va appeler les fonctions nécessaires pour faire fonctionner la database

Il est structuré par des try ainsi que des except pour pouvoir exécuter les fonctions uniquement si les fichiers recherchés ne sont pas déjà crées


