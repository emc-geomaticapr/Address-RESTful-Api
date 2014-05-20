import psycopg2
import geojson

from geojson import Point, Feature, FeatureCollection
from flask_cors import cross_origin
from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask, jsonify, abort, request, make_response, url_for, Response

def get_address():
	conn = psycopg2.connect("dbname=baygis user=efra password=Tiempo4891 host=107.170.109.146")

	def query_db(query):
		cur = conn.cursor()
		cur.execute(query)
		colnames = [desc[0] for desc in cur.description]
		result = cur.fetchall()
		cur.close()
		return result, colnames

	def proccess_feature(row, colnames):
		my_point = Point((row[2],row[1]))
		feature = Feature(geometry=my_point, properties={
			colnames[0]: row[0],
			colnames[1]: row[1],
			colnames[2]: row[2],
			colnames[3]: row[3],
			colnames[4]: row[4]
		})
		return feature

	rows, colnames = query_db("select invid, lat, lon, munid, gcode from basemap.address;")
	features = []

	for row in rows:
		feature = proccess_feature(row, colnames)
		features.append(feature)

	feature_collection = FeatureCollection(features)
	mygeojson = geojson.dumps(feature_collection, sort_keys=True)
	conn.close()

	return Response(mygeojson, mimetype='application/json')

def get_address_by_id(invid):
	conn = psycopg2.connect("dbname=baygis user=efra password=Tiempo4891 host=107.170.109.146")

	def query_db(query):
		cur = conn.cursor()
		cur.execute(query)
		colnames = [desc[0] for desc in cur.description]
		result = cur.fetchall()
		cur.close()
		return result, colnames

	def proccess_feature(row, colnames):
		my_point = Point((row[2],row[1]))
		feature = Feature(geometry=my_point, properties={
			colnames[0]: row[0],
			colnames[1]: row[1],
			colnames[2]: row[2],
			colnames[3]: row[3],
			colnames[4]: row[4]
		})
		return feature

	rows, colnames = query_db("select invid, lat, lon, munid, gcode from basemap.address where invid = '{0}';".format(invid))
	features = []

	for row in rows:
		feature = proccess_feature(row, colnames)
		features.append(feature)

	feature_collection = FeatureCollection(features)
	mygeojson = geojson.dumps(feature_collection, sort_keys=True)
	conn.close()

	return Response(mygeojson, mimetype='application/json')

app = Flask(__name__)

@app.route('/geomaticapr/api/v1.0/address', methods = ['GET'])
#@auth.login_required
@cross_origin()
def address():
    return get_address()

@app.route('/geomaticapr/api/v1.0/address/<invid>', methods = ['GET'])
#@auth.login_required
@cross_origin()
def get_one_address(invid):    
	return get_address_by_id(invid)

if __name__ == '__main__':
    app.run(debug = True)



