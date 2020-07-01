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
	curr_longitude = body['curr_longitude']
	curr_latitude = body['curr_latitude']
	home_longitude = body['home_longitude']
	home_latitude = body['home_latitude']

	headers = {'x-api-key': confidential.AWS}
	body = {
		'longitude': curr_longitude,
		'latitude': curr_latitude,
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

	coords['CURR'] = {
		'index': len(coords),
		'coordinates': [curr_longitude, curr_latitude]
	}

	coords['HOME'] = {
		'index': len(coords),
		'coordinates': [home_longitude, home_latitude]
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

	ret['found_items'] = set()

	for stop in best_trip.path:
		ret['stores'].append(lambda_resp[id_to_index[stop]])
		for each in lambda_resp[id_to_index[stop]]['approximate_quantities']:
			ret['found_items'].add(each['item_name'])

	ret['not_found_items'] = list(set(user_list).difference(ret['found_items']))

	ret['found_items'] = list(ret['found_items'])

	ret['found_proportion'] = len(ret['found_items']) / len(user_list)

	return {
		'statusCode': 200,
		'body': json.dumps(ret)
	}