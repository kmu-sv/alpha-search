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
import json
import os
import uuid, redis, yelpCrawler, Decorator_for_HTTP
from flask import Flask, request, make_response

# Flask app should start in global layout
app = Flask(__name__)

# Generate Redis Object
redis_obj = redis.StrictRedis(host="localhost", port=6379, db=0)

# Constant for indent
VAL_INDENT = 4
# This route is for fulfillment webhook for an Dialogflow agent.
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # Get json from dialogflow. 
    req = request.get_json(silent=True, force=True)
    res = processWebhookRequest(req)
    speech = "time out test"
    res = {
        "speech": speech,
        "displayText": speech
    }
    # JSON Encoding
    res = json.dumps(res, indent=VAL_INDENT)
    # TODO : Remove later
    print("Response : ")
    print(res)
    
    res_formatted = make_response(res)
    res_formatted.headers['Content-Type'] = 'application/json'

    return res_formatted

def processWebhookRequest(req):
    if req.get("result").get("action") != "search.cafe":
        return {}
    """
    query = makeQuery(req)
    if query is None:
        return {}
    # TODO : select data from DB(data shoud be converted to JSON)
    data = "<THIS SHOULD BE CONVERTED TO JSON>"
    """
    
    # TODO : Remove this line later 
    data = callCrawler(req) # This is just test for service without demo.
    res = makeWebhookResult(data)
    return res

def makeQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    parameter_atmosphere = parameters.get("atmosphere")
    parameter_facility = parameters.get("mapsort")
    parameter_open = parameters.get("open")

    # TODO : define a query using parameters. 
    query = ""
    return query

# This is just test for service without demo.
def callCrawler(req) :
    atmosphere = ["UNKNOWN" for i in range(5)]
    wifi = "UNKNOWN"
    parking = "UNKNOWN"
    open = "UNKNOWN"

    result = req.get("result")
    parameters = result.get("parameters")
    parameter_atmosphere = parameters.get("atmosphere")
    parameter_facility = parameters.get("mapsort")
    parameter_open = parameters.get("open")
    
    if parameter_atmosphere.get("quiet") != None :
        atmosphere[0] = "quiet"
    if parameter_atmosphere.get("casual") != None :
        atmosphere[1] = "casual"
    if parameter_atmosphere.get("cosy") != None :
        atmosphere[2] = "cosy"
    if parameter_atmosphere.get("hip") != None :
        atmosphere[3] = "hip"
    if parameter_atmosphere.get("romantic") != None :
        atmosphere[4] = "romantic"
    if parameter_facility.get("wifi") != None :
        wifi = "YES"
    if parameter_facility.get("parking") != None :
        parking = "YES"
    if parameter_open != None :
        open = "YES"

    data = yelpCrawler.getYelpData(40.703491, -73.913351, wifi, parking)
    return data

def makeWebhookResult(data):
    base_url = "alpha-search.in/"

    # Generate token
    token_generated = str(uuid.uuid4()).replace("-", "")

    # insert mapping data to redis table
    redis_obj.set(token_generated, data)
    
    # TODO : make a url for webclient
    speech = base_url + token_generated
    
    return {
        "speech": speech,
        "displayText": speech
    }

@app.route('/mappedcafes/<token>', methods = ['POST', 'GET'])
def getCafes(token) :
    # Get data mapped token from redis table 
    data = redis_obj.get(token)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')