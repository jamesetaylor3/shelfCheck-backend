import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
import requests
import math
import datetime
import prop
from bson.son import SON

MAX_NUM_STORES_RET = 5
QTY_THRESHOLD = 5
DIST_THRESHOLD = 16000000

client = None

def lambda_handler(event, context):
    global client

    if not client:
        client = pymongo.MongoClient(atlas_mondb_endpoint)
    

    user_lat = user_lon = item_name = None
    
    body = json.loads(event["body"])
        
    user_lat = body["latitude"]
    user_lon = body["longitude"]
    item_name = body["item_name"]

    db = client["database0"]
    stores = db["stores"]
    inventory = db["inventory"]
        
    query = {"coordinates": {"$near": SON([("$geometry", SON([("type", "Point"), ("coordinates", [user_lon, user_lat])])), ("$maxDistance", DIST_THRESHOLD)])}}
    
    
    cursor = stores.find(query).limit(10)

    valid_stores = list()
    
    for store in cursor:
        dist = prop.get_distance(user_lat, user_lon, store["coordinates"][1], store["coordinates"][0])

        recent_inventory = inventory.find_one(
            { "_id" : store["inventory_id"] },
            { "_id" : 0, item_name : { "$slice" : -10 } }
        )
        
        print(recent_inventory)

        if len(recent_inventory) == 0:
            continue
        
        if item_name not in recent_inventory:
            continue
        
        qty = prop.get_weighted_average(recent_inventory[item_name])

        if qty > QTY_THRESHOLD:
            store["_id"] = str(store["_id"])
            store["inventory_id"] = str(store["inventory_id"])
            store["approximate_quantity"] = qty
            store["distance"] = dist
            store["recency"] = (datetime.datetime.now() - recent_inventory[item_name][-1]["timestamp"]).total_seconds() / 60
            valid_stores.append(store)

        if len(valid_stores) == MAX_NUM_STORES_RET:
            break
    
    if len(valid_stores) == 0:
        return {
            "statusCode": 200,
            "body": json.dumps("none")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(valid_stores)
    }
