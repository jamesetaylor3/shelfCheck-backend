import pymongo
import datetime

atlas_mondb_endpoint = "mongodb+srv://ec2user:PJHP6MtgxsezJTIG@cluster0-1zkxg.mongodb.net/test?retryWrites=true&w=majority"

def upload_scaped_data(gather):
	print("uploading data")

	client = pymongo.MongoClient(atlas_mondb_endpoint)

	db = client["database0"]
	stores = db["stores"]
	inventory = db["inventory"]

	timestamp = datetime.datetime.utcnow()

	for address in gather:
		store = stores.find_one({ "address" : address })

		if not store:
			continue

		inventory_id = store["inventory_id"]

		for item in gather[address]:

			qty = gather[address][item]

			record = {
				"crawler": True,
				"in_stock": qty != 0,
				"quantity": qty if qty != 0 else None,
				"timestamp": timestamp
			}

			inventory.update_one(
				{ "_id" : inventory_id },
				{ "$push" : { item : record} }
			)

	print("closing database")
	client.close()
