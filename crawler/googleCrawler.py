import googlemaps
import json
import requests
import os
import time

from bs4 import BeautifulSoup
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(find_dotenv(), override=True)

API_KEY = os.environ.get("API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

fread = open('zipcode.txt', 'r')
while True:
    line = fread.readline()
    if not line: break
    zipcode = line[0:5]

    query_str = "San,Francisco,CA," + zipcode
    language_str = "en"
    type_str = "cafe"
    page_token = ""

    result_list = []
    for idx in range(3):
        time.sleep(8)
        req_query = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&language={}&type={}&pagetoken={}&key={}'.format(query_str.replace(',','+'), language_str, type_str, page_token, API_KEY)
        req = requests.get(req_query).json()
        if(req.get('next_page_token')):
            page_token = req['next_page_token']

        for item in req['results']:
            result_dict = dict()
            result_dict['place_id'] = item['place_id']
            result_dict['address'] = item['formatted_address']
            result_dict['latitude'] = item['geometry']['location']['lat']
            result_dict['longitude'] = item['geometry']['location']['lng']
            result_dict['name'] = item['name']

            photourl = []
            try:
                for photoitem in item['photos']:
                    time.sleep(3)
                    link = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photoreference={}&key={}'.format(photoitem['width'], photoitem['photo_reference'], API_KEY)
                    resp = requests.get(link, allow_redirects=False)
                    link_to_pic = resp.headers["Location"]
                    photourl.append(link_to_pic)
            except KeyError:
                pass
            result_dict['photourl'] = photourl
            result_list.append(result_dict)

    with open('./zipcode/'+zipcode+'.txt', 'w') as fwrite:
        fwrite.write(json.dumps(result_list, indent=4))

fread.close()












