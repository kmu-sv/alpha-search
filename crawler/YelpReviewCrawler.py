## !/usr/bin/env python
from bs4 import BeautifulSoup
import requests, json, pymysql

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

sql_conn = pymysql.connect(host='localhost', user='gaeul', password='alpha', db='CAFE', charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

query = "select * from CAFES"
curs.execute(query)
data = curs.fetchall()
for row in data :
    i = 0
    while True : 
        crawling_url = row['yelpurl'] 
        soup = BeautifulSoup(crawling_url, "lxml")
        try :
            index = i * 20
            plain_text = requests.get(crawling_url + "?start=" + str(index)).text
            soup = BeautifulSoup(plain_text, "lxml")
            # parsing reviews
            reviews = soup.select('p[lang|=en]')
            for review in reviews :
                # TODO : Remove later
                print(review)
                print('=============================================================================================')
        except Exception as ex : 
            print(ex)
            break
    i = i + 1
    # TODO : Insert review to DB