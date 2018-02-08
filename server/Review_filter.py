import json, pymysql

# Connect to MySQL and Generete dictionary cursor from connection
sql_conn = pymysql.connect(host='localhost', user='gaeul', password='alpha', db='CAFE', charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

setFilteredReviews() :
    # Fetch data from DB
    fetch_query = "SELECT cafe_id, reviews from CAFES_REVIEWS"
    curs.execute(fetch_query)
    reviews_list = curs.fetchall()
    # Filter review and Update table
    insert_query = """UPDATE CAFES_REVIEWS_FILTERED SET reviews_filtered = %s WHERE cafe_id = %s"""
    for row in reviews_list :
        reviews = row['reviews']
        review_list = reviews.split("#tag#")
        filtered_list = list()
        for review in review_list :
            review_lower = map(lambda name: name.lower(), review) 
            if "wi-fi" in review_lower \
                or "wifi" in review_lower \
                or "outlet" in review_lower :           
                filtered_list.append(review)
        curs.execute(insert_query, (str(filtered_list), str(row['cafe_id'])))
getFilteredReviews() :
    fetch_query = "SELECT * from CAFES_REVIEWS_FILTERED"
    curs.execute(fetch_query)
    filtered_reviews_list = curs.fetchall()
    return filtered_reviews_list