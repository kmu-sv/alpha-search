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
    wifi = "UNKNOWN"
    parking = "UNKNOWN"

    result = req.get("result")
    parameters = result.get("parameters")
    parameter_atmosphere = parameters.get("atmosphere")
    parameter_facility = parameters.get("facility")
    # if parameter_atmosphere.get("quiet") != None :
    #     atmosphere[0] = "quiet"
    # if parameter_atmosphere.get("casual") != None :
    #     atmosphere[1] = "casual"
    # if parameter_atmosphere.get("cosy") != None :
    #     atmosphere[2] = "cosy"
    # if parameter_atmosphere.get("romantic") != None :
    #     atmosphere[3] = "romantic"
    # if parameter_atmosphere.get("classy") != None :
    #     atmosphere[4] = "classy"
    # if parameter_atmosphere.get("trendy") != None :
    #     atmosphere[5] = "trendy"
    # if parameter_atmosphere.get("hipster") != None :
    #     atmosphere[6] = "hipster"
    
    if 'wifi' in parameter_facility :
        wifi = "YES"
    if 'parking' in parameter_facility :
        parking = "YES"

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

def makeQuery(entities_):
    entities_s = entities_.decode("utf-8")
    entities = json.loads(entities_s)
    query = "select * from CAFES where "
    for entity in entities :
        # TODO : remove later
        if(entity == 'atmosphere') :
            continue
        if(entity == 'location') :
            query = query + "and latitude=" 
            query = query + entities['location']['latitude'] + "and longitude" 
            query = query + entities['location']['longitude']
            continue
        print (entity)
        query = query + "and " + entity 
        query = query + "=" + str(entities[entity])
    return query

def getDatafromDB(query) :
    curs.execute(query)
    data = curs.fetchall()
    return json.dumps(data)

def makeWebhookResult(data):
    base_url = "alpha-search.in:5000/"
    #base_url = "54.241.216.252:5000/"

    # Generate token
    token_generated = str(uuid.uuid4()).replace("-", "")

    # insert mapping data to redis table
    redis_obj.set(token_generated, data)
    # 
    # TODO : make a url for webclient
    speech = base_url + "?token=" + token_generated
    
    return {
        "speech": speech,
        "displayText": speech
    }

@app.route('/mappedcafes/<token>', methods = ['POST', 'GET', 'OPTIONS'])
@Decorator_for_HTTP.crossdomain(origin='*')
def getCafes(token) :
    # Get data mapped token from redis table 
    data = redis_obj.get(token)
    query = makeQuery(data)
    print(query)
    result = getDatafromDB(query)
    response = app.response_class(
        response=result,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/')
def index() :
    return render_template("index.html")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')