import json

with open('yelpData.json', 'r') as yelpfile:
    yelpdata = json.load(yelpfile)

with open('googleData.json', 'r') as googlefile:
    googledata = json.load(googlefile)

def checkDuplicated(yelpAddress, googleAddress):
    yelpAddress_split = []
    googleAddress_spilt = []

    yelpAddress_split = yelpAddress.split(' ')
    googleAddress_split = googleAddress.split(' ')

    yelpAddress_part = yelpAddress_split[0] + " " + yelpAddress_split[1]
    googleAddress_part = googleAddress_split[0] + " " + googleAddress_split[1]

    if(yelpAddress_part == googleAddress_part):
        return True
    else:
        return False


# main
only_google_list = []

for googleitem in googledata:
    googleAddress = googleitem['address']
    for yelpitem in yelpdata:
        yelpAddress = yelpitem['address']
        if(checkDuplicated(yelpAddress, googleAddress)):
            if not (yelpitem.get('phone')) : 
                if(googleitem.get('phone')):
                    yelpitem['phone'] = googleitem['phone']
            if not (yelpitem.get('website')): 
                if(googleitem.get('website')):
                    yelpitem['website'] = googleitem['website']
            if not (yelpitem.get('googleurl')): 
                yelpitem['googleurl'] = googleitem['googleurl']
            if not (yelpitem.get('openinfo')): 
                if(googleitem.get('openinfo')):
                   yelpitem['openinfo'] = googleitem['openinfo']
            if not (yelpitem.get('rating')): 
                if(googleitem.get('rating')):
                   yelpitem['rating'] = googleitem['rating']
            if(googleitem.get('googlereviews')):
                yelpitem['googlereviews'] = googleitem['googlereviews']
            break
    else:
        only_google_list.append(googleitem)

for onlyGoogleitem in only_google_list:
    yelpdata.append(onlyGoogleitem)

with open('mergeData.json', 'w') as mergefile:
    mergefile.write(json.dumps(yelpdata, indent=4))
