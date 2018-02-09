import json, pymysql

file_reader = open('../db_connection_info', 'r')
db_connection_info = file_reader.read()
file_reader.close()
sql_conn = pymysql.connect(db_connection_info)
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

insert_query = """INSERT INTO CAFES_REVIEWS(cafe_id, reviews) VALUES(%s, %s)"""
f = open('data', 'r')
data = f.read()
f.close()
reviews_list = eval(data)

index = 1
for row in reviews_list :
    cafe_id = str(index)
    reviews = row[cafe_id]
    curs.execute(insert_query, (cafe_id, reviews))
    index += 1
sql_conn.commit()
sql_conn.close()

