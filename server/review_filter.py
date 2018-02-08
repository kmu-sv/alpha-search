import json, pymysql

# Connect to MySQL and Generete dictionary cursor from connection
sql_conn = pymysql.connect(host='localhost', user='gaeul', password='alpha', db='CAFE', charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)
# Fetch data from DB
query = "SELECT cafe_id, reviews from CAFES_REVIEWS"
curs.execute(query)
reviews_list = curs.fetchall()
dict_list = list()

for row in reviews_list :
    reviews = row['reviews']
    review_list = reviews.split("#tag#")
    filtered_list = list()
    for review in review_list :
        filtered_list.append(review)
    dict_list.append(row['cafe_id'] : str(filtered_list))
return json.dumps(dict_list)    