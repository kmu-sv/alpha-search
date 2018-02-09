import json, pymysql

# Connect to MySQL and Generete dictionary cursor from connection
sql_conn = pymysql.connect(host='localhost',user='gaeul',password='alpha',db='CAFE',charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

def setFilteredReviews() :
    # Fetch data from DB
    fetch_query = "SELECT cafe_id, reviews from CAFES_REVIEWS"
    curs.execute(fetch_query)
    reviews_list = curs.fetchall()
    # Filter review and Update table
    insert_query = """INSERT INTO CAFES_REVIEWS_FILTERED(cafe_id, reviews_filtered, review_count) VALUES(%s, %s, %s)"""
    for row in reviews_list :
        print(row['cafe_id'])
        reviews = row['reviews']
        review_list = reviews.split("#tag#")
        filtered_list = list()
        for review in review_list :
            review_lower = review.lower()
            if "wi-fi" in review_lower \
                or "wifi" in review_lower \
                or "outlet" in review_lower :           
                filtered_list.append(str(review))
        curs.execute(insert_query, (str(row['cafe_id']), str(filtered_list), str(len(filtered_list))))
    sql_conn.commit()
    sql_conn.close()

def getFilteredReviews() :
    fetch_query = "SELECT * from CAFES_REVIEWS_FILTERED"
    curs.execute(fetch_query)
    filtered_reviews_list = curs.fetchall()
    return filtered_reviews_list

if __name__ == "__main__" :
    setFilteredReviews()