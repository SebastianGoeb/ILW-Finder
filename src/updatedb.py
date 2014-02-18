import webapp2
from dbmodel import *
import csv
from google.appengine.ext import ndb, webapp
from google.appengine.api import background_thread, urlfetch
from google.appengine.api.backends import *
import logging
from urllib import urlencode
import json

from flask import Flask

app = Flask(__name__)

logging.getLogger().setLevel(logging.DEBUG)

# sparql_edinPostcodeDatazone = """
# PREFIX label: <http://www.w3.org/2000/01/rdf-schema#label>
# PREFIX geoDataZone: <http://data.opendatascotland.org/def/geography/dataZone>
# PREFIX inDistrict: <http://data.ordnancesurvey.co.uk/ontology/admingeo/inDistrict>
# SELECT ?dzLabel ?pcLabel WHERE {
# ?pc a <http://data.ordnancesurvey.co.uk/ontology/postcode/PostcodeUnit>;
#     label: ?pcLabel;
#     geoDataZone: ?dz.
# ?dz a <http://data.opendatascotland.org/def/geography/DataZone>;
#     label: ?dzLabel;
#     inDistrict: <http://statistics.data.gov.uk/id/statistical-geography/S12000036>;
# }
# """

# def ods_getDatazones():
# 	logging.info("Fetching postcodes from Open Data Scotland")
# 	payload = urlencode({"query":sparql_edinPostcodeDatazone})
# 	data = urlfetch.fetch(url="http://data.opendatascotland.org/sparql.csv?"+payload,
# 												method=urlfetch.GET).content
# 	logging.info("Received "+str(len(data))+" bytes")


# 	data = json.loads(data)
# 	out = {}
# 	for entry in data.get("results").get("bindings"):
# 		out[entry.get("pcLabel").get("value").replace(' ', '')] = ' '.split(entry.get("dzLabel").get("value"))[2]
		
# 		out.append([' '.split(entry.get("dzLabel").get("value"))[2],
# 								])
# 	return out

def update_pc(reinit=True):
	logging.info("Updating PostCode data from local Council Data")
	n_pcs = 0
	with csv.DictReader(open('db-nat-neigh/Survey Data.csv', 'r')) as f:
		for row in f:
			try:
				Postcodes(postcode = row["Pcode"].replace(' ', '').upper(),
									x_coord = int(row["Xcord"]),
									y_coord = int(row["Ycord"]),
									datazone = 0).put()
				n_pcs += 1
			except Exception as e:
				logging.error("Exception: at "+str(i_row)+" ("+' '.join(e.args)+")")
	logging.info("Successfully read " + n_pcs  + " entries")

# class Main(webapp.RequestHandler):
# 	def get(self):
# 		logging.info(str(get_backend()) + " starting up")
# 		background_thread.start_new_background_thread(updatedb, [])
# 		self.response.out.write(''), 200

# app = webapp2.WSGIApplication([('/_ah/start', Main)],
# 															debug=True)
