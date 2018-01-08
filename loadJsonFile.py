import googlemaps
import json
import requests

API_KEY = 'AIzaSyDFtKtm0jnjckE-lB0LkO3SKlWmQIJush8';
gmaps = googlemaps.Client(key=API_KEY)

# Load file -> load 'result.json'
with open('result.json') as f:
    read_data = f.read()

# Dict type is 'list'
datainfo = json.loads(read_data)

data = dict()

# If the information is unknown, save 'unknown'
for item in datainfo:
    try: data['name'] = item['name']
    except KeyError: data['name'] = 'unknown'
    try: data['address'] = item['formatted_address']
    except KeyError: data['address'] = 'unknown'
    try: data['latitude'] = item['geometry']['location']['lat'] 
    except KeyError: data['latitude'] = 'unknown' 
    try: data['longitude'] = item['geometry']['location']['lng']
    except KeyError: data['longitude'] = 'unknown'  
    try: data['phone'] = item['formatted_phone_number'] 
    except KeyError: data['phone'] = 'unknown' 
    try: data['rating'] = item['rating'] 
    except KeyError: data['rating'] = 'unknown' 
    try: data['website'] = item['website']
    except KeyError: data['website'] = 'unknown'

    opendatalist = []
    for openitem in item['opening_hours']['periods']:
        opendata = dict()
        try: opendata['day'] = openitem['open']['day']
        except KeyError: opendata['day'] = 'unknown'
        try: opendata['start'] = openitem['open']['time']
        except KeyError: opendata['start'] = 'unknown'
        try: opendata['end'] = openitem['close']['time']
        except KeyError: opendata['end'] = 'unknown'
        opendatalist.append(opendata)
    data['openinfo'] = opendatalist

    photourl = []
    try: 
        for photoitem in item['photos']:
            photo_query = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photoreference={}&key={}'.format(photoitem["width"], photoitem["photo_reference"], API_KEY)
            photourl.append(photo_query)
    except KeyError: data['photourl'] = 'unknown'
    data['photourl'] = photourl
    
    print(json.dumps(data, indent=4))

