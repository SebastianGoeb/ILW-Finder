import webapp2
import logging
import csv

from cStringIO import StringIO

from google.appengine.api import urlfetch
from google.appengine.ext import deferred
from urllib import urlencode

from db import model
from coords import *

logging.getLogger().setLevel(logging.DEBUG)

sparql_edinDatazone = """
PREFIX label: <http://www.w3.org/2000/01/rdf-schema#label>
PREFIX geoDataZone: <http://data.opendatascotland.org/def/geography/dataZone>
PREFIX inDistrict: <http://data.ordnancesurvey.co.uk/ontology/admingeo/inDistrict>
PREFIX spatial: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
SELECT ?dzLabel ?dzGridX ?dzGridY WHERE {
?dz a <http://data.opendatascotland.org/def/geography/DataZone>;
    label: ?dzLabel;
    inDistrict: <http://statistics.data.gov.uk/id/statistical-geography/S12000036>;
    spatial:easting ?dzGridX;
    spatial:northing ?dzGridY.
}
"""

sparql_edinDzOfPc = """
PREFIX label: <http://www.w3.org/2000/01/rdf-schema#label>
PREFIX geoDataZone: <http://data.opendatascotland.org/def/geography/dataZone>
PREFIX inDistrict: <http://data.ordnancesurvey.co.uk/ontology/admingeo/inDistrict>
PREFIX spatial: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
SELECT ?dzLabel WHERE {
?pc a <http://data.ordnancesurvey.co.uk/ontology/postcode/PostcodeUnit>;
    label: "%s";
    geoDataZone: ?dz.
?dz a <http://data.opendatascotland.org/def/geography/DataZone>;
    label: ?dzLabel.
}
"""

def ods_query(fmt):
	payload = urlencode({"query":fmt})
	return urlfetch.fetch(
		url="http://data.opendatascotland.org/sparql.csv?"+payload,
		method=urlfetch.GET).content

class UpdateDB(webapp2.RequestHandler):
	def get(self):
		deferred.defer(update)
		self.response.out.write('finished datazone.UpdateDB')

def dzNum_fromStr(s):
	return int(s.split(' ')[-1][1:])

def pc_fromStr(s):
	return s.replace(' ', '').upper()

def reformat_postcode(s):
	return s[:-3]  + ' ' + s[-3:]
		
def update():
	logging.info("Updating Datazones from Open Data Scotland")
	data = ods_query(sparql_edinDatazone)
	f_in = StringIO(data)
	csv_in = csv.DictReader(f_in)
	for row in csv_in:
		dzNo = dzNum_fromStr(row["dzLabel"])
		if len(model.Datazone.by_name(dzNo).fetch()) == 0:
			model.Datazone(grid_x = int(row["dzGridX"]),
										 grid_y = int(row["dzGridY"]),
										 name = dzNo).put()
	f_in.close()
	postcodes = model.Postcodes.query().fetch()
	datazones = model.Datazone.query().fetch()
	for p in postcodes:
		with StringIO(ods_query(sparql_edinDzOfPc
														% (reformat_postcode(p.postcode)))) as f:
			data = csv.DictReader(f)
			if len(data) > 0: 				# have matching datazone?
				p.datazone_id = dzNum_fromStr(data[0]['dzLabel'])
				p.put()
			else:											# infer datazone from distance
				gr = GridRef(x.grid_x, x.grid_y)
				best_id = 0
				best_rng = 0
				for y in datazones:
					rng = gr.distance(GridRef(y.grid_x, y.grid_y))
					if best_id == 0 or rng < best_rng:
						logging.info("%s Best was: %i %f now: %i %f" % (p.postcode, best_id, best_rng, y[0], rng))
						best_id = y.name
						best_rng = rng
				p.datazone_id = best_id
				p.put()

	
