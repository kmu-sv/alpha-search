# -*- coding: utf-8 -*-
from __future__ import print_function
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup
import argparse
import json
import pprint
import requests
import sys
import urllib
import os

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

API_KEY = os.environ.get("API_KEY")

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'cafes'
LATITUDE = 37.778281
LONGITUDE = -122.411865
RADIUS = 1000
OPEN_NOW = 'false'
SEARCH_LIMIT = 10

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def search(api_key, term, latitude, longitude):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'radius': RADIUS,
        'open_now': OPEN_NOW.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)

# Define default place : wework civic, default wifi='free', default parking='street'
def getYelpData(lat=37.778264, long=-122.411843, wifi="Free", parking="Street"):
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-la', '--longitude', dest='longitude', default=LONGITUDE,
                        type=float, help='Search longitude (default: %(default)f)')
    parser.add_argument('-lo', '--latitude', dest='latitude', default=LATITUDE,
                        type=float, help='Search latitude (default: %(default)f)')

    input_values = parser.parse_args()

    try:
        response = search(API_KEY, input_values.term, lat, long)
        businesses = response.get('businesses')
        businessList = []
        for idx in businesses:
            response = get_business(API_KEY, idx['id'])
            businessList.append(response)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

    # Merge loadJsonFile.py in this file
    datainfo = businessList

    datalist = []

    for item in datainfo:
        data = dict()
        try: data['name'] = item['name']
        except KeyError: data['name'] = ''
        try:
            address = ", ".join(item['location']['display_address'])
            data['address'] = address
        except KeyError: data['address'] = ''
        try: data['latitude'] = item['coordinates']['latitude']
        except KeyError: data['latitude'] = ''
        try: data['longitude'] = item['coordinates']['longitude']
        except KeyError: data['longitude'] = ''
        try: data['phone'] = item['display_phone']
        except KeyError: data['phone']= ''
        try: data['rating'] = item['rating']
        except KeyError: data['rating'] = ''

        opendata_list = []
        for openitem in item['hours']:
            for openitem_detail in openitem['open']:
                opendata = dict()
                try: opendata['day'] = openitem_detail['day']
                except KeyError: opendata['day'] = ''
                try: opendata['start'] = openitem_detail['start']
                except KeyError: opendata['start'] = ''
                try: opendata['end'] = openitem_detail['end']
                except KeyError: opendata['end'] = ''
                opendata_list.append(opendata)
        data['openinfo'] = opendata_list

        photourl = []
        try:
            for photoitem in item['photos']:
                photourl.append(photoitem)
        except KeyError: data['photourl'] = ''

        data['photourl'] = photourl

        # search more info with beautifulsoup and yelp_url
        url_text = requests.get(item['url']).text

        # Beautiful : Translate text to html
        soup = BeautifulSoup(url_text, "lxml")

        try:
            website = soup.select(".biz-website > a")[0].string
            data['website'] = website
        except Exception as ex:
            data['website'] = ""

        moreinfo_data = dict()

        moreinfo = soup.select(".short-def-list > dl")
        for info in moreinfo:

            attr_name, attr_content = "", ""
            for dataidx in info.children:
                if dataidx.name == "dt": #tag_name == dt
                    attr_name = dataidx.string.strip() # strip function removes in bracket.
                if dataidx.name == "dd": 
                    attr_content = dataidx.string.strip()
            moreinfo_data[attr_name] = attr_content

        data['attributes'] = moreinfo_data
        if data['attributes'].get('Wi-Fi')==wifi and data['attributes'].get('Parking') :
            datalist.append(data)
        



    return json.dumps(datalist, indent=4)


if __name__ == '__main__':
    getYelpData()
