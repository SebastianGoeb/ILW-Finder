import webapp2
import logging
import csv

from StringIO import StringIO

from google.appengine.api import urlfetch
from google.appengine.ext import deferred
from urllib import urlencode

from db import model

sparql_edinPostcodeDatazone = """
PREFIX label: <http://www.w3.org/2000/01/rdf-schema#label>
PREFIX geoDataZone: <http://data.opendatascotland.org/def/geography/dataZone>
PREFIX inDistrict: <http://data.ordnancesurvey.co.uk/ontology/admingeo/inDistrict>
PREFIX spatial: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
SELECT ?dzLabel ?dzGridX ?dzGridY ?pcLabel WHERE {
?pc a <http://data.ordnancesurvey.co.uk/ontology/postcode/PostcodeUnit>;
    label: ?pcLabel;
    geoDataZone: ?dz.
?dz a <http://data.opendatascotland.org/def/geography/DataZone>;
    label: ?dzLabel;
    inDistrict: <http://statistics.data.gov.uk/id/statistical-geography/S12000036>;
    spatial:easting ?dzGridX;
    spatial:northing ?dzGridY.
}
"""

class UpdateDB(webapp2.RequestHandler):
	def get(self):
		deferred.defer(update)
		self.response.out.write('finished datazone.UpdateDB')

def dzNum_fromStr(s):
	return int(s.split(' ')[-1][1:])

def pc_fromStr(s):
	return s.replace(' ', '').upper()
		
def update():
	logging.info("Updating Datazones from Open Data Scotland")
	payload = urlencode({"query":sparql_edinPostcodeDatazone})
	data = urlfetch.fetch(
		url="http://data.opendatascotland.org/sparql.csv?"+payload,
		method=urlfetch.GET).content
	logging.info("Received %i bytes" % (len(data)))
	csv_in = csv.DictReader(StringIO(data))
	n_rows = 0
	for row in csv_in:
		dzNo = dzNum_fromStr(row["dzLabel"])
		dzs = model.Datazone.by_name(dzNo).fetch()
		if len(dz) == 0:
			dzs.append(model.Datazone(name=dzNo))
		for dz in dzs:
			dz.grid_x = int(row["dzGridX"])
			dz.grid_y = int(row["dzGridY"])
			dz.put()
		
		
#		else:
#			dzId = model.Datazone.by_name(dzNo).fetch(1)[0].key.id()
		pc = model.Postcodes.by_postcode(pc_fromStr(row["pcLabel"])).fetch()
		for x in pc:
			x.datazone_id = dzNo
			x.put()
		# pcs = model.Postcodes.by_postcode(row["pcLabel"]).key.get()
		
#		pcs.datazone_id = dzId
#		pcs.put()
		n_rows += 1
	logging.info("Successfully read %i entries" % (n_rows))
