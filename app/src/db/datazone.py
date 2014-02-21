import webapp2
import logging
from pprint import pprint
import csv

import json

from cStringIO import StringIO

from google.appengine.api import urlfetch
from google.appengine.ext import deferred
from urllib import urlencode

from db.model import *
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
#        deferred.defer(update_dz)
#        deferred.defer(update_pop)
#        update_dz()
        update_empty_pc()
        update_pop()
        self.response.out.write('finished datazone.UpdateDB')

def dz_parseCode(s):
    return int(s.split(' ')[-1][1:])

def dz_parseCsvCode(s):
    return int(s[1:])

def pc_fromStr(s):
    return s.strip().upper()

def reformat_postcode(s):
    return s[:-3]  + ' ' + s[-3:]

def update_dz():
    logging.info("Updating Datazones from Open Data Scotland")
    f_in = StringIO(ods_query(sparql_edinDatazone))
    csv_in = csv.DictReader(f_in)
    n_zones = 0
    n_codes = 0

    dbPostcodes_in = None
    with open('data/ods-datazone-postcodes.json', 'r') as f:
        dbPostcodes_in = json.loads(f.read())

    odsPostcodes = {}

    for x in dbPostcodes_in['results']['bindings']:
        pcNorm = pc_fromStr(x['pcLabel']['value'])
        dzNorm = dz_parseCode(x['dzLabel']['value'])
        if dzNorm in odsPostcodes:
            odsPostcodes[dzNorm].append(pcNorm)
        else:
            odsPostcodes[dzNorm] = [pcNorm]
    
    for row in csv_in:
        dzCode = dz_parseCode(row['dzLabel'])
        dbDatazone = Datazone.get_by_id(dzCode)

        if dbDatazone is None:
            dbDatazone = Datazone(
                id = dzCode,
                grid_x = int(row['dzGridX']),
                grid_y = int(row['dzGridY'])
            )
            dbDatazone = dbDatazone.put()
        else:
            continue

        n_zones += 1

        if dzCode in odsPostcodes:
            for odsPostcode in odsPostcodes[dzCode]:
                dbPostcode = Postcodes.query(
                    Postcodes.postcode == odsPostcode).get()
                if dbPostcode is not None:
                    dbPostcode.datazone = dbDatazone
                    dbPostcode.put()
                    n_codes += 1
    f_in.close()
    logging.info("Added %i datazones to DB" % (n_zones))
    logging.info("Updated %i postcode entries" %(n_codes))

def update_empty_pc():
    logging.info("Updating Postcodes with no Datazone")
    datazones = Datazone.query().fetch()
    postcodes = Postcodes.query(Postcodes.datazone == None).fetch()
    n_codes = 0
    for p in postcodes:
        gr = GridRef(p.grid_x, p.grid_y)
        best_id = None
        best_rng = None
        for d in datazones:
            rng = gr.distance(GridRef(d.grid_x, d.grid_y))
            if (best_id is None) or (rng < best_rng):
                best_id = d
                best_rng = rng
        p.datazone = best_id.key
        n_codes += 1
        p.put()
    logging.info("Inferred %i datazones for postcodes" % (n_codes))

def update_pop():
    logging.info("Updating population data")
    n_pop = 0
    with open('data/datazone-population.csv', 'r') as f_in:
        csv_in = csv.DictReader(f_in)
        for row in csv_in:
            zone = Datazone.query(
                Datazone.id == dz_parseCsvCode(row['GeographyCode'])
            ).fetch()
            for z in zone:
                z.pop_total = int(row['GR-denominatorindP'])
                z.pop_child = int(z.pop_total * float(row['GR-Percchild'])/100)
                z.pop_pens = int(z.pop_total * float(row['GR-Percpens'])/100)
                z.pop_work = int(z.pop_total * float(row['GR-Percwork'])/100)
                n_pop += 1
                z.put()
    logging.info("Done. Altered %i entries."%(n_pop))
    datazones = Datazone.query().fetch()
    for dz in datazones:
        postcodes = Postcodes.query(
            Postcodes.datazone == dz.key).fetch()
        dz.num_postcodes = len(postcodes)
        dz.put()
    logging.info("Updated postcode counts")
