import json, pymysql

sql_conn = pymysql.connect(host='localhost',user='gaeul',password='alpha',db='CAFE',charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)
insert_query = """INSERT INTO CAFES_REVIEWS(cafe_id, reviews) VALUES(%s, %s)"""

def insert_yelp_reviews() :
    f = open('data', 'r')
    data = f.read()
    f.close()
    yelp_reviews_list = eval(data)
    index = 1
    for row in yelp_reviews_list :
        cafe_id = str(index)
        reviews = row[cafe_id].replace(">", "").replace("\xa0", "").replace("\\","")
        curs.execute(insert_query, (cafe_id, reviews))
        index += 1
def insert_google_reviews() :
    fetch_query = """SELECT id, googlereviews from CAFES"""
    curs.execute(fetch_query)
    google_reviews_list = curs.fetchall()
    for row in google_reviews_list :
        cafe_id = str(row['cafe_id'])
        reviews = row['reviews']
        curs.execute(insert_query, (cafe_id, reviews))  
if __name__ == "__main__" :    
    #insert_yelp_reviews()
    insert_google_reviews()
    sql_conn.commit()
    sql_conn.close()


