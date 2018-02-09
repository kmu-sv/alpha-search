import json, pymysql

# Connect to MySQL and Generete dictionary cursor from connection
file_reader = open('../db_connection_info', 'r')
db_connection_info = file_reader.read()
file_reader.close()
sql_conn = pymysql.connect(db_connection_info)
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

def setFilteredReviews() :
    # Fetch data from DB
    fetch_query = "SELECT cafe_id, reviews from CAFES_REVIEWS"
    curs.execute(fetch_query)
    reviews_list = curs.fetchall()
    # Filter review and Update table
    insert_query = """INSERT INTO CAFES_REVIEWS_FILTERED(cafe_id, reviews_filtered) VALUES(%s, %s)"""
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
                filtered_list.append(review)
        curs.execute(insert_query, (str(row['cafe_id']), str(filtered_list)))
    sql_conn.commit()
    sql_conn.close()

def getFilteredReviews() :
    fetch_query = "SELECT * from CAFES_REVIEWS_FILTERED"
    curs.execute(fetch_query)
    filtered_reviews_list = curs.fetchall()
    return filtered_reviews_list

if __name__ == "__main__" :
    setFilteredReviews()