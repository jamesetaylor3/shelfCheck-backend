import pymongo
import boto3
import datetime
import credentials

BUCKET_NAME = "INVENTORY-DATA-REPOSITORY"

'''
Description:
This will run overnight and move all inventory data from the mongodb
instance to an aws s3 bucket. It will filter out and delete an inventory
reporters where attribute crawler = true

Good resources:
https://clouductivity.com/amazon-web-services/download-upload-files-amazon-s3-python/

Possible change:
Don't save the csv. Convert to binary and then pass as Body. Might save time
If the database gets huge, this wont work, will need to stagger it
'''

def getAllData():

	client = pymongo.MongoClient(credentials.atlas_mondb_endpoint)

	db = client['database0']
	inventory = db['inventory']

	cursor = inventory.find({})

	ret = {}

	for inventory in cursor:
		oid = inventory['_id']
		sid = str(oid)

		# faster removing these than if statement in next block
		del inventory['_id'], inventory['store_id']

		ret[sid] = {}

		for item in inventory:
			ret[sid][item] = []

			for report in inventory[item]:
				# if this was found by web crawler, we don't want to keep it
				if "crawler" in report:
					continue

				ret[sid][item].append({
					'quantity': str(report['quantity']),
					'timestamp': str(report['timestamp'])
				})


	return ret

def writeToCSV(data):
	filename = str(datetime.date.today()) + '.csv'

	with open(filename, 'w') as file:
		suda_buff = 'inventory_id,item_name,quantity,timestamp\n'

		for sid in data:
			for item in data[sid]:
				for report in data[sid][item]:
					suda_buff += f'{sid},{item},{report["quantity"]},{report["timestamp"]}\n'

		file.write(suda_buff)

	return filename

def uploadToS3(filename):
	content = open(filename, 'rb')
	s3 = boto3.client('s3')
	s3.put_object(
		Bucket=BUCKET_NAME,
		Key=f'{filename[0:4]}/{filename}',
		Body=content
	)

data = getAllData()

filename = writeToCSV(data)

uploadToS3(filename)