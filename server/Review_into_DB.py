import json, pymysql

<<<<<<< HEAD
sql_conn = pymysql.connect(host='localhost',user='gaeul',password='alpha',db='CAFE',charset='utf8mb4')
=======
file_reader = open('../db_connection_info', 'r')
db_connection_info = file_reader.read()
file_reader.close()
sql_conn = pymysql.connect(db_connection_info)
>>>>>>> c019b43fbe9470b707c545c0ff6fdf3db2608419
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

insert_query = """INSERT INTO CAFES_REVIEWS(cafe_id, reviews) VALUES(%s, %s)"""
f = open('data', 'r')
data = f.read()
f.close()
reviews_list = eval(data)

index = 1
for row in reviews_list :
    cafe_id = str(index)
    reviews = row[cafe_id].replace(">", "").replace("\xa0", "")
    curs.execute(insert_query, (cafe_id, reviews))
    index += 1
sql_conn.commit()
sql_conn.close()

