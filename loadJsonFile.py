import json
import requests

with open('result.json') as openfile:
    read_data = openfile.read()

datainfo = json.loads(read_data)

datalist = []

for item in datainfo:
    data = dict()
    try: data['name'] = item['name']
    except KeyError: data['name'] = 'unknown'
    try: 
        address = ", ".join(item['location']['display_address'])
        data['address'] = address
    except KeyError: data['address'] = 'unknown'
    try: data['latitude'] = item['coordinates']['latitude']
    except KeyError: data['latitude'] = 'unknown'
    try: data['longitude'] = item['coordinates']['longitude']
    except KeyError: data['longitude'] = 'unknown'
    try: data['phone'] = item['display_phone']
    except KeyError: data['phone']= 'unknown'
    try: data['rating'] = item['rating']
    except KeyError: data['rating'] = 'unknown'
    try: data['infourl'] = item['url']
    except KeyError: data['infourl'] = 'unknown' 

    opendata_list = []
    for openitem in item['hours']:
        for openitem_detail in openitem['open']:
            opendata = dict()
            try:
                opendata['day'] = openitem_detail['day']
                print(opendata['day'])
            except KeyError: opendata['day'] = 'unknown'
            try: opendata['start'] = openitem_detail['start']
            except KeyError: opendata['start'] = 'unknown'
            try: opendata['end'] = openitem_detail['end']
            except KeyError: opendata['end'] = 'unknown'
            opendata_list.append(opendata)
    data['openinfo'] = opendata_list

    photourl = []
    try:
        for photoitem in item['photos']:
            photourl.append(photoitem)
    except KeyError: data['photourl'] = 'unknown'

    data['photourl'] = photourl
    datalist.append(data)

print(json.dumps(datalist, indent=4))

