# -*- coding: utf-8 -*

# input : list organized by python dictionary
# output : print (insert success or fail)

import json
import pymysql
from datetime import datetime

open_cafe_list = []

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
        with conn.cursor() as cursor :
            cursor.execute("select * from CAFES")
            cafe_list = cursor.fetchall()
        return cafe_list
    finally:
        conn.close()

# get information about date
def getDate() :
    now_day = datetime.today().weekday()
    now = datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    return now_day, now_hour, now_minute #return type is tuple 

# find out opening cafe
def findOpenCafes(cafes):
    now_day, now_hour, now_minute = getDate()
    day_to_find = now_day + 7 # the number '7' is to match with attribute 
    #loop for each cafe in cafe list
    for cafe in cafes :
        print (cafe)
        print (cafe[1],cafe[day_to_find])
        if cafe[day_to_find] == 'NULL' :
            continue
        else :
            open_hour = cafe[day_to_find][1]
            closing_hour = cafe[day_to_find][2]
            open_hour = int(cafe[day_to_find][6] + cafe[day_to_find][7])
            open_minute = int(cafe[day_to_find][8] + cafe[day_to_find][9])
            close_hour = int(cafe[day_to_find][15] + cafe[day_to_find][16])
            close_minute = int(cafe[day_to_find][17] + cafe[day_to_find][18])
            if (((open_hour == now_hour and open_minute <= now_minute) or (open_hour < now_hour)) and \
                ((close_hour == now_hour and close_minute >= now_minute) or (close_hour > now_hour))) :
                open_cafe_list.append(cafe[1])
    return open_cafe_list



if __name__ == "__main__":
    cafe_list = getTable()
    result = findOpenCafes(cafe_list)
    print (result)

