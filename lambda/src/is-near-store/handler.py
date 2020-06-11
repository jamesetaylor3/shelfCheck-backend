import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
import requests
import confidential
from bson.son import SON

DIST_THRESHOLD = 1000

client = None

def lambda_handler(event, context):
    global client

    if not client:
        client = pymongo.MongoClient(confidential.MONGO)

    body = json.loads(event["body"])

    user_lat = body["latitude"]
    user_lon = body["longitude"]
    
    if (user_lat == None or user_lon == None):
        return {
            "statusCode": 200,
            "body": json.dumps({ "near" : False })
        }

    db = client["database0"]
    stores = db["stores"]

    query = {"coordinates": {"$near": SON([("$geometry", SON([("type", "Point"), ("coordinates", [user_lon, user_lat])])), ("$maxDistance", DIST_THRESHOLD)])}}
    
    r = stores.find_one(query)

    if not r:
    	return {
    		"statusCode": 200,
    		"body": json.dumps({ "near" : False })
    	}

    return {
        "statusCode": 200,
        "body": json.dumps({ "near" : True })
    }
