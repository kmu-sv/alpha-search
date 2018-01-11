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

from flask import Flask, request, make_response

import uuid
import redis

# Flask app should start in global layout
app = Flask(__name__)

# Generate Redis Object
redis_obj = redis.Redis(host='localhost',port=6379,db=0)

VAL_INDENT = 4 # Constant value for indent
# This route is for fulfillment webhook for an Dialogflow agent.
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get json from dialogflow. 
    req = request.get_json(silent=True, force=True)

    # TODO : remove later
    print("Request:")
    print(json.dumps(req, indent=VAL_INDENT))

    res = processWebhookRequest(req)

    # JSON Encoding
    res = json.dumps(res, indent=VAL_INDENT)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processWebhookRequest(req):
    if req.get("result").get("action") != "search.cafe":
        return {}
    query = makeQuery(req)
    if query is None:
        return {}
    # TODO : select data from DB(data shoud be converted to JSON)
    data = "<THIS SHOULD BE CONVERTED TO JSON>"
    res = makeWebhookResult(json.dumps(data))
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

def makeWebhookResult(data):
    base_url = "ec2-13-124-187-211.ap-northeast-2.compute.amazonaws.com:5000/mappedcafes/"

    # Generate token
    token_generated = uuid.uuid4()

    # insert mapping data to redis table
    redis_obj.set(token_generated, data)

    # TODO : make a url
    speech = base_url + token_generated
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
    }

# TODO : Write responding code
@app.route('/mappedcafes/<token>', method = ['POST', 'GET'])
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