import shopper
import requests
import json
import time
import confidential
from collections import OrderedDict

LAMBDA = 'https://api.shelfcheck.io/v1/get-closest-stores-multiple-items'

def generate_mapbox_endpoint(coords):
	coords_str = ''
	for _, each in coords.items():
		coords_str += str(each['coordinates'][0]) + ',' + str(each['coordinates'][1]) + ';'

	coords_str = coords_str[:-1]

	return f'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/{coords_str}.json?access_token={confidential.MAPBOX}'

def lambda_handler(event, context):

	body = json.loads(event['body'])

	user_list = body['items']
	longitude = body['longitude']
	latitude = body['latitude']

	headers = {'x-api-key': confidential.AWS}
	body = {
		'longitude': longitude,
		'latitude': latitude,
		'items': user_list
	}

	r = requests.post(LAMBDA, headers=headers, json=body)

	lambda_resp = json.loads(r.text)

	stores = []

	id_to_index = {}

	# might need to find cleaner way of doing this
	coords = OrderedDict()

	for i, each in enumerate(lambda_resp):
		items = [item['item_name'] for item in each['approximate_quantities']]

		store = shopper.Store(each['_id'], items)

		stores.append(store)

		id_to_index[each['_id']] = i

		coords[each['_id']] = {
			'index': i,
			'coordinates': each['coordinates']
		}

	coords['HOME'] = {
		'index': len(coords),
		'coordinates': [longitude, latitude]
	}

	itenerary_candidates = shopper.get_itenerary_candidates(user_list, stores)

	mb_endpoint = generate_mapbox_endpoint(coords)

	# should find a way to reduce the number of stores that are needed to be searched for
	mb_matrix = json.loads(requests.get(mb_endpoint).content)['durations']

	matrix = {}

	for id1, val1 in coords.items():
		matrix[id1] = {}
		for id2, val2 in coords.items():
			matrix[id1][id2] = mb_matrix[val1['index']][val2['index']]

	best_trip = shopper.solve_trip(itenerary_candidates, matrix)

	ret = {}

	ret['stores'] = []
	ret['stop_times'] = best_trip.stop_times
	ret['total_time'] = best_trip.total_time

	for stop in best_trip.path:
		ret['stores'].append(lambda_resp[id_to_index[stop]])

	return {
		'statusCode': 200,
		'body': json.dumps(ret)
	}