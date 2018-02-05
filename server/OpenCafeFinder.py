# -*- coding: utf-8 -*

# input : list organized by python dictionary
# output : print (insert success or fail)

import json
import pymysql
from datetime import datetime
import pytz

# connect to DB
def getConnection():
    return pymysql.connect(host='localhost',
                            user='gaeul',
                            password='alpha',
                            db='CAFE',
                            charset='utf8mb4')

# inquiry data from connected DB 
def getTable():
    conn = getConnection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor :
            cursor.execute("select * from CAFES")
            cafe_list = cursor.fetchall()
        return cafe_list
    finally:
        conn.close()

# get information about date
def getDate() :
    now_day = datetime.today().weekday()
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    #now = datetime.now()
    #now = localtz.localize(now)
    now_hour = now.hour
    now_minute = now.minute
    return now_day, now_hour, now_minute #return type is tuple 

# find out opening cafe
def findOpenCafes(cafes):
    open_cafe_list = []
    now_day, now_hour, now_minute = getDate()
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_to_find = weekdays[now_day]
    #loop for each cafe in cafe list
    for cafe in cafes :
        if cafe[day_to_find + '_open_hours'] == 'NULL' :
            continue
        else :
            open_hour = int(cafe[day_to_find+'_open_hours'][6] + cafe[day_to_find+'_open_hours'][7])
            open_minute = int(cafe[day_to_find+'_open_hours'][8] + cafe[day_to_find+'_open_hours'][9])
            close_hour = int(cafe[day_to_find+'_open_hours'][15] + cafe[day_to_find+'_open_hours'][16])
            close_minute = int(cafe[day_to_find+'_open_hours'][17] + cafe[day_to_find+'_open_hours'][18])
            if (((open_hour == now_hour and open_minute <= now_minute) or (open_hour < now_hour)) and \
                ((close_hour == now_hour and close_minute >= now_minute) or (close_hour > now_hour))) :
                open_cafe_list.append(cafe)
    return open_cafe_list

if __name__ == "__main__":
    cafe_list = getTable()
    result = findOpenCafes(cafe_list)
    print (result)

