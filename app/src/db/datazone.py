import webapp2
import logging
from pprint import pprint
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
SELECT ?dzLabel ?dzGridX ?dzGridY ?dz WHERE {
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

sparql_edinDzPcs = """
PREFIX geoDataZone: <http://data.opendatascotland.org/def/geography/dataZone>
PREFIX label: <http://www.w3.org/2000/01/rdf-schema#label>
PREFIX pc: <http://data.ordnancesurvey.co.uk/ontology/postcode/PostcodeUnit>
SELECT ?pcLabel
WHERE {
 ?pc a pc:;
     label: ?pcLabel;
     geoDataZone: <%s>.
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

def dz_parseCode(s):
    return int(s.split(' ')[-1][1:])

def pc_fromStr(s):
    return s.replace(' ', '').upper()

def reformat_postcode(s):
    return s[:-3]  + ' ' + s[-3:]

def update():
    logging.info("Updating Datazones from Open Data Scotland")
    f_in = StringIO(ods_query(sparql_edinDatazone))
    csv_in = csv.DictReader(f_in)
    n_zones = 0
    n_codes = 0
    for row in csv_in:
        dz_code = dz_parseCode(row['dzLabel'])
        dz_db = model.Datazone.by_code(dz_code).fetch()

        if len(dz_db) > 0:
            continue
        
        dz_postcodes_in = StringIO(ods_query(sparql_edinDzPcs % (row['dz'])))
        dz_postcodes_csv = csv.DictReader(dz_postcodes_in)
        for pc_row in dz_postcodes_csv:
            pc_norm = pc_fromStr(pc_row['pcLabel'])
            pc_match = model.Postcodes.query(
                model.Postcodes.postcode == pc_norm).fetch()
            for m in pc_match:
                m.datazone_id = dz_code
                n_codes += 1
                m.put()
        dz_postcodes_in.close()
        dz_lst = []
        if len(dz_db) == 0:
            # no such datazone in db
            dz_lst.append(model.Datazone(code=dz_code))
        for dz in dz_lst:
            dz.grid_x = int(row['dzGridX'])
            dz.grid_y = int(row['dzGridY'])
            dz.put()
            n_zones += 1
    f_in.close()
    logging.info("Added %i datazones to DB" % (n_zones))
    logging.info("Updated %i postcode entries" %(n_codes))
    datazones = model.Datazone.query().fetch()
    postcodes = model.Postcodes.query(model.Postcodes.datazone_id == 0).fetch()
    n_codes = 0
    for p in postcodes:
        gr = GridRef(p.grid_x, p.grid_y)
        best_id = 0
        best_rng = 0
        for d in datazones:
            rng = gr.distance(GridRef(d.grid_x, d.grid_y))
            if best_id == 0 or rng < best_rng:
                best_id = d.code
                best_rng = rng
        p.datazone_id = best_id
        n_codes += 1
        p.put()
    logging.info("Inferred %i datazones for postcodes" % (n_codes))
