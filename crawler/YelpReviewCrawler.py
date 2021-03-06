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

file_reader = open('../db_connection_info', 'r')
db_connection_info = file_reader.read()
file_reader.close()
sql_conn = pymysql.connect(db_connection_info)
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

fetch_query = "select id, yelpurl from CAFES"
curs.execute(fetch_query)
cafes = curs.fetchall()

insert_query = """UPDATE CAFES_REVIEWS SET reviews = %s WHERE cafe_id = %s"""

for row in cafes :
    i = 0
    review_list = list()
    while True : 
        crawling_url_from_table = row['yelpurl']
        crawling_url = crawling_url_from_table.split("?")[0]
        try :
            index = i * 20
            crawling_cursor = crawling_url + "?start=" + str(index)
            print(crawling_cursor)
            plain_text = requests.get(crawling_cursor).text
            soup = BeautifulSoup(plain_text, "lxml")
            # parsing reviews
            reviews = soup.select("p[lang|=en]")
            if len(reviews) == 0 :
                break
            for review in reviews :
                review = review.replace("<p lang=\"en\">", "")
                review_content = review.replace("</p", "")
                review_list.append(review_content)
        except Exception as ex : 
            print(ex)
            break
        i = i + 1
    
    curs.execute(insert_query, ("#tag#".join(review_list), row['id']))