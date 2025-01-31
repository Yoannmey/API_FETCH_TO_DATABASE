import requests
import json

url = "https://api.sncf.com/v1/coverage/sncf/vehicle_journeys?count=1000" # URL de l'API

token = "token" # token de connexion à l'API

tabData = [] # tab qui va contenir toute les données

def api_to_json():
    while 1:  # Boucle while pour aller de page en page
        request = requests.get(url, auth = (token, "")) # requests accéde à l'URL avec le token
        
        data = request.json()  # requests rentre les données de l'URL dans la variable data
        tabData.append(data)  # ajoute la page suivant au tab de données

        stop = 0
        if "links" in data:
            for link in data["links"]: 
                if link["type"] == "next": # si le type du lien trouvé est next 
                    url = link["href"] # on change le lien par le nouveau
                    stop = 1 
                    print("Ok", url)
                    break # on arrete la boucle apres avoir récupéré le lien

        if stop == 0:  # gestion d'arrêt de la boucle while 
            break

    f = open("json/vehicules_journeys.json", "w") # ouverture en mode écriture du fichier "vehicules_journeys.json" dans le dossier json 
    json.dump(tabData, f, indent = 4) # écriture dans le .json du contenu de l'API avec une intentation pour une meilleure lecture du fichier 



