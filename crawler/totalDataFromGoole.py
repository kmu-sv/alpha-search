from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import json
import googlemaps
import requests
import time
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

API_KEY = os.environ.get("API_KEY")
with open('placeidList.json') as data_file:
    data = json.load(data_file)

dataList = []

for item in data:
    place_id = item['place_id']
    req_query = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, API_KEY)

    time.sleep(1)
    req = requests.get(req_query).json()

    dataList.append(req['result'])

with open('totalList.json', 'w') as f:
    f.write(json.dumps(dataList, indent=4))

