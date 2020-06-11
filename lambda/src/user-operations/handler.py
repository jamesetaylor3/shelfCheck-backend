import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
import requests
import datetime

client = None

def add_email(collection, contents):
	email = contents['email']
	
	r = collection.count_documents(
		{ 'email' : email }
	)
	
	if r != 0:
		return {
			'statusCode': 200,
			'body': json.dumps({ 'status': 'That email already exists in our database!'})
		}

	collection.insert_one(
		{ 'email' : email }
	)

	return {
		'statusCode': 200,
		'body': json.dumps({ 'status': "worked" })
	}

def edit_email(collection, contents):
	old_email = contents['old_email']
	new_email = contents['new_email']

	r = collection.update_one(
		{ 'email' : old_email },
		{ '$set' : { 'email' : new_email } }
	)

	status = 'worked' if r.matched_count == 1 else 'no record found'

	return {
		'statusCode': 200,
		'body': json.dumps({ 'status': status })
	}

def remove_email(collection, contents):
	email = contents['email']

	r = collection.delete_one({ 'email' : email })

	status = 'worked' if r.deleted_count == 1 else 'no record found'

	return {
		'statusCode': 200,
		'body': json.dumps({ 'status': status })
	}

def record_submission(collection, contents):
	email = contents['email']

	date = str(datetime.date.today())

	r = collection.find_one(
		{ 'email' : email },
		{ date : 1 }
	)
	
	if date not in r:
		r[date] = 0

	r[date] += 1

	r = collection.update_one(
		{ 'email' : email },
		{ '$set' : { date : r[date] } }
	)

	status = 'worked' if r.matched_count == 1 else 'no record found'

	return {
		'statusCode': 200,
		'body': json.dumps({ 'status' : status })
	}

RUN = {
	'add': add_email, 
	'edit': edit_email,
	'remove': remove_email,
	'record': record_submission
}

def lambda_handler(event, context):
	global client

	if not client:
		client = pymongo.MongoClient(atlas_mondb_endpoint)

	db = client['database0']
	collection = db['users']

	body = json.loads(event['body'])

	action = body['action']
	contents = body['contents']

	return RUN[action](collection, contents)
