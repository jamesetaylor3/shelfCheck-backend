import json
import time
import requests
import confidential

ENDPOINT = 'https://api.shelfcheck.io/v1/'

FUNCTIONS = ['get-store-data', 'get-closest-stores-multiple-items', 'get-closest-stores',
			 'check-region-availability', 'get-closest-stores-single-item']

def sendRequest(fn):
	requests.post(
		url = ENDPOINT + fn,
		headers = { 'x-api-key' : confidential.shelfcheck_key },
		json = confidential.body
	)

if __name__ == '__main__':
	while True:
		for fn in FUNCTIONS:
			sendRequest(fn)
		time.sleep(45)