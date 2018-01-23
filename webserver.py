## !/usr/bin/env python
"""
Author : Hwancheol Kang
Project : Alpha-search
Date : January 5, 2018
Description :
This script is for responding for web-client's request, Using flask and redis.
"""
from __future__ import print_function
import json, os, uuid, redis, pymysql
from flask import Flask, request, make_response, render_template
# import custom modules
import Decorator_for_HTTP

# Flask app should start in global layout
app = Flask(__name__)

# Generate Redis Object
redis_obj = redis.StrictRedis(host="localhost", port=6379, db=0)

# Connect to MySQL and Generete dictionary cursor from connection
sql_conn = pymysql.connect(host='localhost', user='gaeul', password='alpha', db='CAFE', charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

def makeQuery(entities):
    query = "select * from CAFES where " + "wifi=" + entities['wifi'] + " and parking=" + entities['parking']
    return query

def getDatafromDB(query) :
    curs.execute(query)
    data = curs.fetchall()
    return json.dumps(data)

@app.route('/mappedcafes/<token>/<latitude>/<longitude>', methods = ['POST', 'GET', 'OPTIONS'])
@Decorator_for_HTTP.crossdomain(origin='*')
def getCafes(token, latitude, longitude) :
    # TODO : remove later
    print("token : ", token)
    print("latitude : ", latitude, "longitude : ", longitude)
    # Get data mapped token from redis table 
    data = json.load(redis_obj.get(token))
    # TODO : remove later
    print(data)
    query = makeQuery(data)
    # TODO : remove later
    print(query)
    result = getDatafromDB(query)
    # TODO : filter data based on location
    response = app.response_class(
        response=result,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/<token>', methods = ['POST', 'GET', 'OPTIONS'])
@Decorator_for_HTTP.crossdomain(origin='*')
def index(token) :
    print(token)
    return render_template("index.html", token=token)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting Web Server on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))