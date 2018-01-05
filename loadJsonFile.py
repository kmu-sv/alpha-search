import googlemaps
import json
import requests

API_KEY = 'AIzaSyDFtKtm0jnjckE-lB0LkO3SKlWmQIJush8';
gmaps = googlemaps.Client(key=API_KEY)

# Load file -> load 'result.json'
with open('result.json') as f:
    read_data = f.read()

# Dict type is 'list'
dict = json.loads(read_data)

# If the information is unknown, save 'unknown'
for item in dict:
    try: print(item['name'])
    except KeyError: print('unknown') 
    try: print(item['formatted_address'])
    except KeyError: print('unknown') 
    try: print(item['geometry']['location']['lat'])
    except KeyError: print('unknown') 
    try: print(item['geometry']['location']['lng'])
    except KeyError: print('unknown') 
    try: print(item['formatted_phone_number'])
    except KeyError: print('unknown') 
    try: print(item['opening_hours']['periods'])
    except KeyError: print('unknown') 
    try: print(item['rating'])
    except KeyError: print('unknown') 
    try: print(item['website'])
    except KeyError: print('unknown') 

	# request photo_url 
    try: 
        for photoitem in item['photos']:
	    photo_query = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photoreference={}&key={}'.format(photoitem["width"], photoitem["photo_reference"], API_KEY)
	    print(photo_query)
    except KeyError: print('unknown')

    print('\n\n')

