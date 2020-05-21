from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from threading import RLock
import concurrent.futures
import itertools
import logging
import time
import db
import config

start = time.time()

MAX_THREADS = 16
LOADING_FROM_SEARCH_WAIT = 5

stock_value = { "likely in stock" : 25, "limited stock" : 15, "out of stock" : 0 }

lock = RLock()

options = Options()
options.add_argument("--headless")

gather = {}

def thread(params):
	global gather

	zip_code, item = params

	# not sure why this was here
	# gather = {}

	# Firefox
	# driver = webdriver.Firefox(options=options)

	# Google Chrome
	driver = webdriver.Chrome(options=options)

	driver.get("https://www.instok.org/search")

	try:
		driver.find_element_by_class_name("actions").click()
	except:
		print("no disclaimer blocking page")

	print(f"completing search of {item} in {zip_code}")
	driver.find_element_by_class_name("main-search").send_keys(item)
	driver.find_element_by_class_name("zip-input").send_keys(zip_code)
	driver.find_element_by_class_name("main-next-button").click()

	time.sleep(LOADING_FROM_SEARCH_WAIT)

	inventory_elements = driver.find_elements_by_class_name("divider")

	for element in inventory_elements:

		item_block = element.text.split("\n")

		if item_block == ['']:
			continue

		if not item.lower() in item_block[1].lower():
			# we can have keywords here or abstractions for other keywords later
			if not (item == "Toilet Paper" and "bath tissue" in item_block[1].lower()):
				continue


		if not ("likely in stock" in item_block[2].lower() or "limited stock" in item_block[2].lower() or "out of stock" in item_block[2].lower()):
			continue

		stock = address = None

		try:
			stock, address = item_block[2].split(" at ")
		except:
			print("had an error with spltting item block 2")
			continue

		stock = stock.lower()

		# going to need all abbreviations for road, drive, street, etc
		# going to need a way to find the state of the place. might need to use map api. this will work for now tho as we are only serving nc.
		address = address.lower() \
						 .replace(" e ", " east ") \
						 .replace(" w ", " west ") \
						 .replace(" n ", " north ") \
						 .replace(" s ", " south ") \
						 .replace(" nw ", " north west ") \
						 .replace(" ne ", " north east ") \
						 .replace(" se ", " south east ") \
						 .replace(" sw ", " south west ") \
						 .replace(" rd, ", " road, ") \
						 .replace(" rd ", " road, ") \
						 .replace(" dr, ", " drive, ") \
						 .replace(" dr ", " drive, ") \
						 .replace(" st, ", " street, ") \
						 .replace(" st ", " street, ") \
						 .title() \
						 + ", NC"
		
		with lock:
			if address not in gather:
				gather[address] = {}

			gather[address][item] = stock_value[stock]


	driver.close()

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
	executor.map(thread, itertools.product(config.zip_codes, config.items))

db.upload_scaped_data(gather)

stop = time.time()

print("took %.2f seconds" % float(stop - start))