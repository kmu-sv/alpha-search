## !/usr/bin/env python
"""
Author : Hwancheol Kang
Project : Alpha-search
Date : January 5, 2018
Description :
This script is for back-end service including fulfillment webhook for an Dialogflow agent 
and responding for web-client's request, Using flask and redis

"""
from __future__ import print_function
import json, os, uuid, redis, pymysql
# import custom modules
import yelpCrawler, Decorator_for_HTTP
from flask import Flask, request, make_response, render_template

# Flask app should start in global layout
app = Flask(__name__)

# Generate Redis Object
redis_obj = redis.StrictRedis(host="localhost", port=6379, db=0)

# Connect to MySQL and Generete dictionary cursor from connection
sql_conn = pymysql.connect(host='localhost', user='gaeul', password='alpha', db='CAFE', charset='utf8mb4')
curs = sql_conn.cursor(pymysql.cursors.DictCursor)

# Constant for indent
VAL_INDENT = 4

# This route is for fulfillment webhook for an Dialogflow agent.
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # Get json from dialogflow. 
    req = request.get_json(silent=True, force=True)
    res = processWebhookRequest(req)
    
    # JSON Encoding
    res = json.dumps(res, indent=VAL_INDENT)

    res_formatted = make_response(res)
    res_formatted.headers['Content-Type'] = 'application/json'

    return res_formatted

def processWebhookRequest(req):
    if req.get("result").get("action") != "search.cafe":
        return {}
    
    data = parseEntity(req) # data contains entities.
    res = makeWebhookResult(data)
    return res

def parseEntity(req) :
    atmosphere = ["UNKNOWN" for i in range(7)]
    wifi = "0"
    parking = "0"

    result = req.get("result")
    parameters = result.get("parameters")
    parameter_atmosphere = parameters.get("atmosphere")
    parameter_facility = parameters.get("facility")
    # parsing atmospheres
    if "quiet" in parameter_atmosphere :
         atmosphere[0] = "quiet"
    if "casual" in parameter_atmosphere :
         atmosphere[1] = "casual"
    if "cosy" in parameter_atmosphere :
         atmosphere[2] = "cosy"
    if "romantic" in parameter_atmosphere :
         atmosphere[3] = "romantic"
    if "classy" in parameter_atmosphere :
         atmosphere[4] = "classy"
    if "trendy" in parameter_atmosphere :
         atmosphere[5] = "trendy"
    if "hipster" in parameter_atmosphere :
         atmosphere[6] = "hipster"
    # parsing facilities
    if 'wifi' in parameter_facility :
        wifi = "1"
    if 'parking' in parameter_facility :
        parking = "1"

    data = {
        'atmosphere' : {
            'quiet' : atmosphere[0],
            'casual' : atmosphere[1],
            'cosy' : atmosphere[2],
            'romantic' : atmosphere[3],
            'classy' : atmosphere[4],
            'trendy' : atmosphere[5],
            'hipster' : atmosphere[6],
        },
        'wifi' : wifi,
        'parking' : parking,
        'location' : {
            'latitude' : '37.777905600000000',
            'longitude' : '-122.414220300000000'
        }
    }
    return data

def makeQuery(entities):
    query = "select * from CAFES where " + "wifi=" + entities['wifi'] + " and parking=" + entities['parking']
    return query

def getDatafromDB(query) :
    curs.execute(query)
    data = curs.fetchall()
    return json.dumps(data)

def makeWebhookResult(data):
    base_url = "https://alpha-search.in:5000/"
    #base_url = "https://54.241.216.252:5000/"

    # Generate token
    token_generated = str(uuid.uuid4()).replace("-", "")

    # insert mapping data to redis table
    redis_obj.set(token_generated, data)
    speech = base_url + token_generated
    
    return {
        "speech": speech,
        "displayText": speech
    }

@app.route('/mappedcafes/<token>/<latitude>/<longitude>', methods = ['POST', 'GET', 'OPTIONS'])
@Decorator_for_HTTP.crossdomain(origin='*')
def getCafes(token, latitude, longitude) :
    # TODO : remove later
    print("token : ", token)
    print("latitude : ", latitude, "longitude : ", longitude)
    # Get data mapped token from redis table 
    data = redis_obj.get(token)
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

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))