__author__ = 'spousty'

import psycopg2
from bottle import route, run, get, DEBUG
import os
import random
from random_words import RandomWords




@route('/')
def index():
	return "<h1> hello OpenShift Ninja without DB</h1>"

# since this is a read only talk to the replicas
@get('/db')
def dbexample():
	print(os.environ.get('POSTGRESQL_USER'))
	print("After Env")
	try:
		conn = psycopg2.connect(database=os.environ.get('PG_DATABASE'), user=os.environ.get('PG_USER'), host=os.environ.get('PG_SLAVE_RC_SERVICE_HOST'), password=os.environ.get('PG_ROOT_PASSWORD'))
	except:
		print(os.environ.get('PG_USER')	+ "  " + os.environ.get('PG_SLAVE_RC_SERVICE_HOST'))
	
	cur = conn.cursor()
	cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints limit 10""")
	
	rows = cur.fetchall()
	result_string = "<h2>Here are your results: </h2>"
	for row in rows:
		result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + "</h3>"

	return  result_string

@post('/db')
def dbpost():

	#changes these to the master
	try:
		conn = psycopg2.connect(database=os.environ.get('PG_DATABASE'), user=os.environ.get('PG_USER'), host=os.environ.get('PG_MASTER_RC_SERVICE_HOST'), password=os.environ.get('PG_ROOT_PASSWORD'))
	except:
		print(os.environ.get('PG_USER')	+ "  " + os.environ.get('PG_SLAVE_RC_SERVICE_HOST'))

	#Need to generate some data - no need for ID
	#NEED a name and a lat and long
	lat = random.uniform(-90,90)
	lon = random.uniform(-180,180)
	rw = RandomWords()
	name = rw.random_word() + " " + rw.random_word()

	#here comes the insert srid = 4326
	cur = conn.cursor()
	cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints limit 10""")

	rows = cur.fetchall()
	result_string = "<h2>Here are your results: </h2>"
	for row in rows:
		result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + "</h3>"

	return  result_string

if __name__ == '__main__':
	run(host='0.0.0.0', port=8080, debug=True)
