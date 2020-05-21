import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
import requests
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

    body = json.loads(event["body"])

    user_lat = body["latitude"]
    user_lon = body["longitude"]
    items = body["items"]

    items_dict_proj = dict(zip(items, [ { "$slice" : -10} ] * len(items)))

    db = client["database0"]
    stores = db["stores"]
    inventory = db["inventory"]

    query = {"coordinates": {"$near": SON([("$geometry", SON([("type", "Point"), ("coordinates", [user_lon, user_lat])])), ("$maxDistance", DIST_THRESHOLD)])}}

    cursor = stores.find(query).limit(10)

    valid_stores = list()

    for store in cursor:
        dist = prop.get_distance(user_lat, user_lon, store["coordinates"][1], store["coordinates"][0])

        # maybe do a baseline check to narrow to stock that has been updated today. do it later but see if can do it here
        recent_inventory = inventory.find_one(
            { "_id" : store["inventory_id"] },
            { "_id" : 0, "store_id" : 0, **items_dict_proj }
        )

        if len(recent_inventory) == 0:
            continue

        store["distance"] = dist

        store["approximate_quantities"] = []

        for item_name in recent_inventory:
            if item_name not in items:
                continue

            qty = prop.get_weighted_average(recent_inventory[item_name])

            if qty > QTY_THRESHOLD:
                store["approximate_quantities"].append({
                    "item_name": item_name,
                    "quantity": qty,
                    "recency": (datetime.datetime.now() - recent_inventory[item_name][-1]["timestamp"]).total_seconds() / 60
                })

        if len(store["approximate_quantities"]) == 0:
            continue

        store["stock_proportion"] = len(store["approximate_quantities"]) / len(items)

        store["_id"] = str(store["_id"])
        store["inventory_id"] = str(store["inventory_id"])

        valid_stores.append(store)
    
    valid_stores = sorted(valid_stores, key=lambda k: 1 - k['stock_proportion'])
    
    
    return {
        "statusCode": 200,
        "body": json.dumps(valid_stores)
    }