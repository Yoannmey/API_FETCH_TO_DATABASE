import requests
import json

token = "token" # token de connexion à l'API

tabData_journey = [] # tab qui va contenir les données de vehicle_journeys
tabData_disruptions = [] # tab qui va contenir les données de disruptions

def journeys_to_json():
    url_journey = "https://api.sncf.com/v1/coverage/sncf/vehicle_journeys?count=1000" # URL de l'API pour vehicle_journeys
    while 1:  # Boucle while pour aller de page en page
        request = requests.get(url_journey, auth = (token, "")) # requests accéde à l'URL avec le token
        
        data = request.json()  # requests rentre les données de l'URL dans la variable data
        tabData_journey.append(data)  # ajoute la page suivant au tab de données

        stop = 0
        if "links" in data:
            for link in data["links"]: 
                if link["type"] == "next": # si le type du lien trouvé est next 
                    url_journey = link["href"] # on change le lien par le nouveau
                    stop = 1 
                    print("Ok", url_journey)
                    break # on arrete la boucle apres avoir récupéré le lien

        if stop == 0:  # gestion d'arrêt de la boucle while 
            break

    f = open("json/vehicle_journeys.json", "w") # ouverture en mode écriture du fichier "vehicules_journeys.json" dans le dossier json 
    json.dump(tabData_journey, f, indent = 4) # écriture dans le .json du contenu de l'API avec une intentation pour une meilleure lecture du fichier 

def disruptions_to_json():
    url_disruptions = "https://api.sncf.com/v1/coverage/sncf/disruptions?count=1000" # URL de l'API pour disruptions
    while 1:  # Boucle while pour aller de page en page
        request = requests.get(url_disruptions, auth = (token, "")) # requests accéde à l'URL avec le token
        
        data = request.json()  # requests rentre les données de l'URL dans la variable data
        tabData_disruptions.append(data)  # ajoute la page suivant au tab de données

        stop = 0
        if "links" in data:
            for link in data["links"]: 
                if link["type"] == "next": # si le type du lien trouvé est next 
                    url_disruptions = link["href"] # on change le lien par le nouveau
                    stop = 1 
                    print("Ok", url_disruptions)
                    break # on arrete la boucle apres avoir récupéré le lien

        if stop == 0:  # gestion d'arrêt de la boucle while 
            break

    f = open("json/disruptions.json", "w") # ouverture en mode écriture du fichier "vehicules_journeys.json" dans le dossier json 
    json.dump(tabData_disruptions, f, indent = 4) # écriture dans le .json du contenu de l'API avec une intentation pour une meilleure lecture du fichier 


