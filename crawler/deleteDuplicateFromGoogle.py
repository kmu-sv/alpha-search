import json

fread = open('zipcode.txt', 'r')
temp_cafe_list = []
total_cafe_list = []

while True:
    line = fread.readline()
    zipcode = line.strip()
    if zipcode=="": break
    if not line: break

    with open('./zipcode/'+zipcode+'.json') as data_file:
        data = json.load(data_file)

    for item in data:
        temp_cafe_list.append(item)

result = []
checkPlaceId = []

for item in temp_cafe_list:
    if item['place_id'] not in checkPlaceId:
        checkPlaceId.append(item['place_id'])
        result.append(item)

with open('placeidList.json', 'w') as fwrite:
    fwrite.write(json.dumps(result, indent=4))



