import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
import requests
import math
import prop
from queue import PriorityQueue
from bson.son import SON

NUM_STORES_RET = 12
DIST_THRESHOLD = 16000000

client = None

def lambda_handler(event, context):
	global client

	if not client:
		client = pymongo.MongoClient(atlas_mondb_endpoint)

	body = json.loads(event["body"])

	user_lat = body["latitude"]
	user_lon = body["longitude"]

	db = client["database0"]
	stores = db["stores"]

	query = {"coordinates": {"$near": SON([("$geometry", SON([("type", "Point"), ("coordinates", [user_lon, user_lat])])), ("$maxDistance", DIST_THRESHOLD)])}}
	
	cursor = stores.find(query).limit(NUM_STORES_RET)

	ret = []

	for store in cursor:
		dist = prop.get_distance(user_lat, user_lon, store["coordinates"][1], store["coordinates"][0])

		store["distance"] = dist
		store["_id"] = str(store["_id"])
		store["inventory_id"] = str(store["inventory_id"])

		ret.append(store)


	return {
		"statusCode": 200,
		"body": json.dumps(ret)
	}