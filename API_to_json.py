import requests
import json

token = "token" # token de connexion à l'API

tabData_journey = [] # tab qui va contenir les données de vehicle_journeys
tabData_disruptions = [] # tab qui va contenir les données de disruptions

def journeys_to_json():
    url_journey = "https://api.sncf.com/v1/coverage/sncf/vehicle_journeys?count=1000"
    while 1:  # Boucle while pour aller de page en page
        request = requests.get(url_journey, auth = (token, ""))
        
        data = request.json()
        tabData_journey.append(data)  # ajoute la page suivant au tab de données

        stop = 0
        if "links" in data:
            for link in data["links"]: 
                if link["type"] == "next": # si le type du lien trouvé est next 
                    url_journey = link["href"] # on change le lien par le nouveau
                    stop = 1 
                    print("Ok", url_journey)
                    break 

        if stop == 0:  # gestion d'arrêt de la boucle while 
            break

    f = open("json/vehicle_journeys.json", "w") 
    json.dump(tabData_journey, f, indent = 4) 

def disruptions_to_json():
    url_disruptions = "https://api.sncf.com/v1/coverage/sncf/disruptions?count=1000" 
    while 1:  # Boucle while pour aller de page en page
        request = requests.get(url_disruptions, auth = (token, ""))
        
        data = request.json() 
        tabData_disruptions.append(data)  # ajoute la page suivant au tab de données

        stop = 0
        if "links" in data:
            for link in data["links"]: 
                if link["type"] == "next": 
                    url_disruptions = link["href"] 
                    stop = 1 
                    print("Ok", url_disruptions)
                    break

        if stop == 0:  # gestion d'arrêt de la boucle while 
            break

    f = open("json/disruptions.json", "w") 
    json.dump(tabData_disruptions, f, indent = 4) 

