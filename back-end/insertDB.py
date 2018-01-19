# -*- coding: utf-8 -*

# input : list organized by python dictionary
# output : print (insert success or fail)

import test_list
import pymysql

attributes = ['name', 'address', 'phone_number', 'latitude', 'longitude', 'rating', 'monday_open_hours', 'tuesday_open_hours', 'wednesday_open_hours', 'thursday_open_hours', 'friday_open_hours', 'saturday_open_hours', 'sunday_open_hours', 'photourl', 'take_out_available', 'parking_available', 'bike_parking_available', 'good_for_groups', 'ambience', 'wi_fi_available']

record_values = ['name_value', 'address_value', 'phone_number_value', 'latitude_value', 'longitude_value', 'rating_value', 'monday_open_hours_value', 'tuesday_open_hours_value', 'wednesday_open_hours_value', 'thursday_open_hours_value', 'friday_open_hours_value', 'saturday_open_hours_value',
'sunday_open_hours_value', 'photourl_value', 'take_out_available_value', 'parking_available_value', 'bike_parking_available_value', 'good_for_groups_value', 'ambience_value', 'wi_fi_available_value']

extracted_info = ['name', 'address', 'phone', 'latitude', 'longitude', 'rating', 'openinfo', 'photourl', 'attributes']
extracted_attributes_info = ['Take-out', 'Parking', 'Bike Parking', 'Good for Groups', 'Ambience', 'Wi-Fi']


#connect to DB
def getConnection():
    return pymysql.connect(host='localhost',
    user='gaeul',
    password='alpha',
    db='CAFE',
    charset='utf8mb4')

def insertTable():
	conn = getConnection()
	try:
		with conn.cursor() as cursor:

			sql = 'INSERT INTO CAFES (name, address, phone_number, latitude, longitude, rating, monday_open_hours, tuesday_open_hours, wednesday_open_hours, thursday_open_hours, friday_open_hours, saturday_open_hours, sunday_open_hours, photourl, take_out_available, parking_available, bike_parking_available, good_for_groups, ambience, wi_fi_available) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

			cursor.execute(sql, (record_values[0], record_values[1], record_values[2], record_values[3], record_values[4], record_values[5], record_values[6], record_values[7], record_values[8], record_values[9], record_values[10], record_values[11], record_values[12], record_values[13], record_values[14], record_values[15], record_values[16], record_values[17], record_values[18], record_values[19]))
		conn.commit()
		print(cursor.lastrowid)

	finally:
		conn.close()	

def getRecord(cafes):
	for i in range (0, len(cafes)):
		k = 0
		for j in range (len(extracted_info)):
			print (i,j)
			if extracted_info[j] == 'openinfo' :
				for m in range(7):
					openinfo_list = cafes[i].get(extracted_info[j])
					record_values[k] = 'not yet'

					"""
					len_of_openinfo = len(openinfo_list)
					index_of_openinfo = 0
					index_of_7 = 0

					# 여기서부터 고치기 m이 문제인듯함 / 고치고 python insertDB.py 돌리고 , DB확인해서 0 1 2 3 5 잘 돌아가는지 확인해보
					while (index_of_7 != 7):
						if openinfo_list[len_of_openinfo-1].get('day') < index_of_7:
							record_values[k] = 'none'
							index_of_7+=1
						elif openinfo_list[index_of_openinfo].get('day') == index_of_7:
							record_values[k] = str(openinfo_list[m].get('day'))+":"+str(openinfo_list[m].get('start'))+"-"+str(openinfo_list[m].get('end'))
							index_of_openinfo+=1
							index_of_7+=1
						elif openinfo_list[index_of_openinfo].get('day') != index_of_7:
							record_values[k] = "none"
							index_of_7+=1
					print "record_values[k] : ", record_values[k], "extracted_info : ", extracted_info[j]
					"""
					k+=1
					
			elif extracted_info[j] == 'photourl' :
				record_values[k] = cafes[i].get(extracted_info[j])[0]
				print('record_values[k] : ', record_values[k], 'extracted_info : ', extracted_info[j])
				k+=1
			elif extracted_info[j] == 'attributes' :
				attributes_info = cafes[i].get(extracted_info[j])
				for n in range (len(extracted_attributes_info)):
					if extracted_attributes_info[n] in attributes_info :
						record_values[k] = attributes_info.get(extracted_attributes_info[n])
						if record_values[k] == "'Yes'" or record_values[k] == 'Street' :
							record_values[k] = 1
						else :
							record_values[k] = 0
						print('record_values[k] : ', record_values[k], 'extracted_info : ', extracted_attributes_info[n])
						k+=1
					else :
						record_values[k] = 0
						print('record_values[k] : ', record_values[k], 'extracted_info : ', extracted_attributes_info[n])
						k+=1
			else :
				record_values[k] = cafes[i].get(extracted_info[j])
				print('record_values[k] : ', record_values[k], 'extracted_info : ', extracted_info[j])
				k+=1
			print ('i  is :', i, 'j is : ', j)

		print('finish')
		insertTable()




if __name__ == "__main__":
	cafe_list = test_list.getResult()
	getRecord(cafe_list)

