import json
import googlemaps
import json
import requests
import os
import time

from bs4 import BeautifulSoup
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

API_KEY = os.environ.get("API_KEY")

with open('totalList.json') as f:
    read_data = f.read()

datainfo = json.loads(read_data)
dataList = []

for item in datainfo:
    data = dict()
    if(item.get('name')): data['name'] = item['name']
    if(item.get('formatted_address')): data['address'] = item['formatted_address']
    if(item['geometry']['location'].get('lat')): data['latitude'] = item['geometry']['location']['lat']
    if(item['geometry']['location'].get('lng')): data['longitude'] = item['geometry']['location']['lng']
    if(item.get('formatted_phone_number')): data['phone'] = item['formatted_phone_number']
    if(item.get('website')): data['website'] = item['website']
    if(item.get('url')): data['googleurl'] = item['url']
    if(item.get('opening_hours')):
        opendata_list = []
        for openitem in item['opening_hours']['periods']:
            opendata = dict()
            if(openitem.get('close') and openitem.get('open')):
                if(openitem['close'].get('day')>=0 and openitem['close'].get('day')<=6):
                    opendata['day'] = openitem['close']['day']
                if(openitem['open'].get('time')):
                    opendata['start'] = openitem['open']['time']
                if(openitem['close'].get('time')):
                    opendata['end'] = openitem['close']['time']
                opendata_list.append(opendata)
        data['openinfo'] = opendata_list
    if(item.get('rating')):
        data['rating'] = item['rating']
    try:
        photourlList = []
        for photoitem in item['photos'] :
            time.sleep(1)
            photo_query = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photoreference={}&key={}'.format(photoitem["width"], photoitem["photo_reference"], API_KEY)
            resp = requests.get(photo_query, allow_redirects=False)
            link_to_pic = resp.headers['Location']
            photourlList.append(link_to_pic)
        data['photourl'] = photourlList
    except KeyError as ex: 
        pass

    dataList.append(data)

with open('googleData.json', 'w') as fwrite:
    fwrite.write(json.dumps(dataList, indent=4))



