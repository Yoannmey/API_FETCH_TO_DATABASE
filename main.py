from API_to_json import *
from sql_create import *

try: 
    with open('json/vehicules_journeys.json') as file:
       print("oui")
except FileNotFoundError: 
    api_to_json()
    print("non")


try: 
    with open('db_sncf.db') as file:
       print("oui")
except FileNotFoundError: 
    create_sql()
    print("non")

