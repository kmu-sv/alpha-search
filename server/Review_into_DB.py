import json, pymysql

sql_conn = pymysql.connect(host='localhost',user='gaeul',password='alpha',db='CAFE',charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)
insert_query = """INSERT INTO CAFES_REVIEWS(cafe_id, reviews) VALUES(%s, %s)"""
index = 1

def insert_yelp_reviews() :
    global index
    f = open('data', 'r')
    data = f.read()
    f.close()
    yelp_reviews_list = eval(data)
    for row in yelp_reviews_list :
        print(index)
        cafe_id = str(index)
        reviews = row[cafe_id].replace(">", "").replace("\xa0", "").replace("\\","")
        curs.execute(insert_query, (cafe_id, reviews))
        index += 1
def insert_google_reviews() :
    global index
    fetch_query = """SELECT id, googlereviews from CAFES"""
    curs.execute(fetch_query)
    google_reviews_list = curs.fetchall()
    for row in google_reviews_list :
        if row['id'] <= 850 :
            continue 
        cafe_id = str(row['id'])
        reviews = row['googlereviews']
        curs.execute(insert_query, (cafe_id, str(reviews)))

if __name__ == "__main__" :    
    insert_yelp_reviews()
    insert_google_reviews()
    sql_conn.commit()
    sql_conn.close()


