import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
import requests
import confidential

from bson.objectid import ObjectId

client = None

def lambda_handler(event, context):
    global client

    if not client:
        client = pymongo.MongoClient(confidential.MONGO)

    body = json.loads(event["body"])

    store_name = body["store_name"]
    store_address = body["store_address"]
    store_coords = body["store_coords"]

    db = client["database0"]
    stores = db["stores"]
    inventory = db["inventory"]

    store_id = ObjectId()
    inventory_id = ObjectId()

    store_doc = {
        "_id" : store_id,
        "inventory_id" : inventory_id,
        "name" : store_name,
        "address" : store_address,
        "coordinates" : store_coords
    }

    inventory_doc = {
        "_id" : inventory_id,
        "store_id" : store_id
    }
    
    stores.insert_one(store_doc)
    inventory.insert_one(inventory_doc)

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "store_id" : str(store_id),
                "inventory_id" : str(inventory_id),
                "coordinates" : store_coords
            }
        )
    }
