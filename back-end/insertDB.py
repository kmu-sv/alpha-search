# -*- coding: utf-8 -*

# input : list organized by python dictionary
# output : print (insert success or fail)

import json
import pymysql

record_values = ['name_value', 'address_value', 'phone_number_value', 'latitude_value', 'longitude_value', \
'rating_value', 'monday_open_hours_value', 'tuesday_open_hours_value', 'wednesday_open_hours_value', \
'thursday_open_hours_value', 'friday_open_hours_value', 'saturday_open_hours_value', \
'sunday_open_hours_value', 'photourl_value', 'take_out_available_value', 'parking_available_value', 'bike_parking_available_value', \
'good_for_groups_value', 'ambience_value', 'wi_fi_available_value', 'website_value']

extracted_info = ['name', 'address', 'phone', 'latitude', 'longitude', 'rating', 'openinfo', 'photourl', 'attributes', 'website']
extracted_attributes_info = ['Take-out', 'Parking', 'Bike Parking', 'Good for Groups', 'Ambience', 'Wi-Fi']
day_info = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# connect to DB
def getConnection():
    return pymysql.connect(host='localhost',
    user='gaeul',
    password='alpha',
    db='CAFE',
    charset='utf8mb4')

# insert into connected DB 
def insertTable():
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            sql = 'INSERT INTO CAFES (name, address, phone_number, latitude, longitude, rating, monday_open_hours, tuesday_open_hours, \
            wednesday_open_hours, thursday_open_hours, friday_open_hours, saturday_open_hours, sunday_open_hours, photourl, \
            take_out_available, parking_available, bike_parking_available, good_for_groups, ambience, wi_fi_available, website) \
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (record_values[0], record_values[1], record_values[2], record_values[3], record_values[4], \
            	record_values[5], record_values[6], record_values[7], record_values[8], record_values[9], record_values[10], \
            	record_values[11], record_values[12], record_values[13], record_values[14], record_values[15], record_values[16], \
            	record_values[17], record_values[18], record_values[19], record_values[20]))
            conn.commit()
            print(cursor.lastrowid)

    finally:
        conn.close()	

# determine what record would be stored
def getRecord(cafes):
	# loop for each of the cafe
    for cafeIndex in range (0, len(cafes)):
        recordIndex = 0
        #loop for storing data for the cafe
        for infoIndex in range (len(extracted_info)):
            # if data doesn't exists, store 'NULL' 
            isExist = cafes[cafeIndex].get(extracted_info[infoIndex], 0)
            if isExist == 0 :
                if extracted_info[infoIndex] == 'openinfo' :
                    print ('this is openinfo')
                    for day in range(7):
                        record_values[recordIndex] == 'NULL'
                        recordIndex+=1
                else :
                	record_values[recordIndex] = 'NULL'
                	recordIndex+=1
            # if data exists, store the corresponded data
            else :
                print (cafeIndex,infoIndex)
                if extracted_info[infoIndex] == 'openinfo' :
                    openinfo_list = cafes[cafeIndex].get(extracted_info[infoIndex])
                    dayIndex = 0
                    day_countIndex = 0
                    testIndex = 0
                    print (openinfo_list[-1].get('day'))
                    # loop for the operating hours for each day of the week
                    for day_number in range (len(openinfo_list)):
                        #compare day_countInex and the day 
                        day = openinfo_list[day_number].get('day')
                        if day == day_countIndex :
                            record_values[recordIndex] = day_info[openinfo_list[day_number].get('day')], openinfo_list[day_number].get('start'), openinfo_list[day_number].get('end')
                            record_values[recordIndex] = str(record_values[recordIndex])
                            recordIndex+=1
                            day_countIndex+=1
                        else :
                            while day_countIndex < day :
                                record_values[recordIndex] ='NULL'
                                recordIndex+=1
                                day_countIndex+=1
                    while day_countIndex < 7 :
                        record_values[recordIndex] = 'NULL'
                        day_countIndex += 1
                        recordIndex += 1	
                elif extracted_info[infoIndex] == 'photourl' :
                    record_values[recordIndex] = cafes[cafeIndex].get(extracted_info[infoIndex])[0]
                    print('record_values[recordIndex] : ', record_values[recordIndex], 'extracted_info : ', extracted_info[infoIndex])
                    recordIndex+=1
                elif extracted_info[infoIndex] == 'attributes' :
                    attributes_info = cafes[cafeIndex].get(extracted_info[infoIndex])
                    # loop for storing data for the attribute (for lists in the dictionary)
                    for attributeIndex in range (len(extracted_attributes_info)):
                        if extracted_attributes_info[attributeIndex] in attributes_info :
                            if extracted_attributes_info[attributeIndex] == 'Ambience' :
                                record_values[recordIndex] = attributes_info.get(extracted_attributes_info[attributeIndex])
                                recordIndex+=1
                            else :
                                record_values[recordIndex] = attributes_info.get(extracted_attributes_info[attributeIndex])
                                if record_values[recordIndex] == 'Yes' or record_values[recordIndex] == 'Street' or record_values[recordIndex] == 'Free':
                                    record_values[recordIndex] = 1
                                else :
                                    record_values[recordIndex] = 0
                                print('record_values[recordIndex] : ', record_values[recordIndex], 'extracted_info : ', extracted_attributes_info[attributeIndex])
                                recordIndex+=1
                        else :
                            record_values[recordIndex] = 0
                            print('record_values[recordIndex] : ', record_values[recordIndex], 'extracted_info : ', extracted_attributes_info[attributeIndex])
                            recordIndex+=1
                else :
                    record_values[recordIndex] = cafes[cafeIndex].get(extracted_info[infoIndex])
                    print(recordIndex, ': ', record_values[recordIndex], 'extracted_info : ', extracted_info[infoIndex])
                    recordIndex+=1
                print ('cafeIndex  is :', cafeIndex, 'infoIndex is : ', infoIndex)

        print('finish')
        insertTable()

if __name__ == "__main__":
    #import json and change into python dictionary
    with open("result2.json", "r") as f:
        read_data = f.read()
    cafe_list = json.loads(read_data)
    getRecord(cafe_list)

