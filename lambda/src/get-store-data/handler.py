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
import confidential
from bson.objectid import ObjectId

LAMBDA_PARAM = -1 / 10

all_items = ["Bread", "Milk", "Eggs", "Bottled Water", "Ground Beef", "Toilet Paper", "Diapers", "Masks",
             "Garbage Bags", "Disinfectant Wipes", "Hand Sanitizer", "Hand Soap", "Paper Towels", "Batteries", "Flashlights"]
all_items_dict_proj = dict(zip(all_items, [ { "$slice" : -10} ] * len(all_items)))

client = None

def lambda_handler(event, context):
    global client

    if not client:
        client = pymongo.MongoClient(confidential.MONGO)

    body = json.loads(event["body"])

    store_id = body["store_id"]
    user_lat = body["latitude"]
    user_lon = body["longitude"]

    db = client["database0"]
    stores = db["stores"]
    inventory = db["inventory"]

    store_doc = stores.find_one({ "_id" : ObjectId(store_id) })

    ret = store_doc

    ret["_id"] = str(store_doc["_id"])
    ret["inventory_id"] = str(store_doc["inventory_id"])

    ret["distance"] = prop.get_distance(user_lat, user_lon, *list(reversed(store_doc["coordinates"])))

    ret["inventory"] = db.inventory.find_one(
        { "_id" : ObjectId(store_doc["inventory_id"]) },
        { "_id" : 0, "store_id": 0, **all_items_dict_proj }
    )

    # find estimates for quantities and convert datetimes to strings
    
    # defintely should clean this up a bit
    for item in ret["inventory"]:
        ret["inventory"][item] = {
            "approximate_quantity" : prop.get_weighted_average(ret["inventory"][item]),
            "crowdsourced_data" : ret["inventory"][item]
        }
        for i in range(len(ret["inventory"][item]["crowdsourced_data"])):
            del ret["inventory"][item]["crowdsourced_data"][i]["ip_address"]
            ret["inventory"][item]["crowdsourced_data"][i]["recency"] = (datetime.datetime.now() - ret["inventory"][item]["crowdsourced_data"][i]["timestamp"]).total_seconds() / 60
            del ret["inventory"][item]["crowdsourced_data"][i]["timestamp"]
    
    ret["inv"] = []
    for item in ret["inventory"]:
        ret["inv"].append(ret["inventory"][item])
        ret["inv"][-1]["item_name"] = item
    
    ret["inventory"] = ret["inv"]
    del ret["inv"]
    
    ret["numberOfItems"] = len(ret["inventory"])
    
    return {
        "statusCode": 200,
        "body": json.dumps(ret)
    }