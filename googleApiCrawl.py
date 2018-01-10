import os
import googlemaps
import json
import requests
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(find_dotenv(), override=True)

API_KEY = os.environ.get("API_KEY")

gmaps = googlemaps.Client(key=API_KEY)

# Twin Peaks is center of SF : 37.755305, -122.466763
gmaps_result = gmaps.places_radar(location=(37.755305, -122,466763)
                                  , radius=50000
                                  , min_price=0
                                  , max_price=2
                                  #, open_now=True
                                  , type='cafe')

datalist = []

# Gmaps_result has 'results' tag
for place in gmaps_result['results'][0:1000]:
    # Find place_id
    place_id = place['place_id']

    # Then find json data from place_id
    req_query = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, API_KEY)

    # Request result recieve and change json
    req = requests.get(req_query).json()
    datalist.append(req["result"])

with open("result.json", "w") as f:
    f.write(json.dumps(datalist, indent=4))


print(len(gmaps_result['results']))
