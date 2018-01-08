import googlemaps
import json
import requests

API_KEY = 'AIzaSyDFtKtm0jnjckE-lB0LkO3SKlWmQIJush8';
gmaps = googlemaps.Client(key=API_KEY)

# Wework civic : 37.778159, -122.411867
gmaps_result = gmaps.places_radar(location=(37.778159, -122.411867)
                                  , radius=500
                                  , min_price=0
                                  , max_price=2
                                  , open_now=True
                                  , type='cafe')

datalist = []

# Gmaps_result has 'results' tag
for place in gmaps_result['results'][0:20]:
    # Find place_id
    place_id = place['place_id']

    # Then find json data from place_id
    req_query = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, API_KEY)

    # Request result recieve and change json
    req = requests.get(req_query).json()
    datalist.append(req["result"])

with open("result.json", "w") as f:
    f.write(json.dumps(datalist, indent=4))
