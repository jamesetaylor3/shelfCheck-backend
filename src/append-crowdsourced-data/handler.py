import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
import datetime
import requests

from bson.objectid import ObjectId

client = None

def lambda_handler(event, context):
    global client
    
    if not client:
        client = pymongo.MongoClient(atlas_mondb_endpoint)
        
    body = json.loads(event["body"])
    
    ip_address = event["requestContext"]["identity"]["sourceIp"]
    inventory_id = ObjectId(body["inventory_id"])
    item_name = body["item_name"]
    in_stock = body["in_stock"]
    quantity = body["quantity"]
    timestamp = datetime.datetime.utcnow()
    
    if in_stock and quantity == None:
        return {
            "statusCode": 400,
            "body": "Quantity must be set if item is in stock"
        }
    
    if not in_stock and quantity != None:
        return {
            "statusCode": 400,
            "body": "Item must be in stock if quantity is set"
        }
    
    db = client["database0"]
    inventory = db["inventory"]
    
    record = {
        "ip_address" : ip_address,
        "in_stock" : in_stock,
        "quantity" : quantity,
        "timestamp" : timestamp
    }
        
    r = inventory.update_one(
        { "_id" : inventory_id },
        { "$push" : { item_name : record } }
    )
        
    if r.matched_count == 0:
        return {
            "statusCode": 400,
            "body": json.dumps("Not a valid inventory id")
        }
    
    
    return {
        'statusCode': 200,
        'body': json.dumps("success")
    }
