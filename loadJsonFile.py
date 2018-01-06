import json
import requests

with open('result.json') as f:
    read_data = f.read()

dict = json.loads(read_data)

for item in dict:
    try: print(item['name'])
    except KeyError: print('unknown')
    try: print(", ".join(item['location']['display_address']))
    except KeyError: print('unknown')
    try: print(item['coordinates']['latitude'])
    except KeyError: print('unknown')
    try: print(item['coordinates']['longitude'])
    except KeyError: print('unknown')
    try: print(item['display_phone'])
    except KeyError: print('unknown')
    try: print(item['rating'])
    except KeyError: print('unknown')
    try: print(item['url'])
    except KeyError: print('unknown')

    try:
        for openitem in item['hours']:
            for openitem_detail in openitem['open']:
                print(openitem_detail['day'])
                print(openitem_detail['start'])
                print(openitem_detail['end'])
    except KeyError: print('unknown')

    try:
        for photoitem in item['photos']:
            print(photoitem)
    except KeyError: print('unknown')

print('\n\n')

