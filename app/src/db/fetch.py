from flask import Flask
from StringIO import StringIO
import simplejson as json
import publicPlaces

import logging

from db import model

from ..coords import *

Main = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)
def retJson(obj):
    output = StringIO()
    json.dump(obj, output)
    return output.getvalue()


@Main.route('/get/postcodes')
def get_postcodes():
    data = [x.to_dict()["postcode"] for x in model.Postcodes.get().fetch()]
    return retJson(data)

@Main.route('/get/district/of-postcodes')
def get_distOfPc():
    data = model.Postcodes.get().fetch()
    data = {x.postcode: x.district for x in data}
    return retJson(data)
        
@Main.route('/get/georef/of-postcodes')
def get_grOfPcs():
    data = model.Postcodes.get().fetch()
    def f_(x):
        r = GeoRef.fromGridRef(GridRef(x.grid_x, x.grid_y))
        return [r.latitude, r.longitude]
    data = {x.postcode: f_(x) for x in data}
    return retJson(data)

    
@Main.route('/get/publicPlaces')
def get_public_places():
    return str(publicPlaces.storePublicPlaces())
@Main.route('/get/test_data')
def test_data():
    postcode = model.Postcodes()
    postcode.id = 1
    postcode.postcode = "EH1 1LY"
    postcode.x = 59
    postcode.y = -34
    postcode.district = "Newington"
    postcode.put()
    
    pub = model.PlaceCat()
    pub.id = 1
    pub.name = "Pub"
    pub.put()
    
    school = model.PlaceCat()
    school.id = 2
    school.name = "School"
    school.put()
    
    pub_eh1 = model.PlacePostRel()
    pub_eh1.postcode_id = 1
    pub_eh1.place_cat_id = 1
    pub_eh1.val = 2
    pub_eh1.put()
    
    school_eh1 = model.PlacePostRel()
    school_eh1.postcode_id = 1
    school_eh1.place_cat_id = 2
    school_eh1.val = 3
    school_eh1.put()
    
    return "done"
    
@Main.route('/get/fullPostcodes')
def get_full_postcodes():
    return retJson(model.Postcodes.getFull())
    
@Main.route('/get/georef/of-postcode/<string:pc>')
def get_grOfPc(pc):
    data = model.Postcodes.by_postcode(pc).fetch()
    logging.info("Have %i entries" % (len(data)))
    def f_(x):
        r = GeoRef.fromGridRef(GridRef(x.grid_x, x.grid_y))
        return [r.latitude, r.longitude]
    data = [f_(x) for x in data]
    return retJson(data)

@Main.route('/get/datazone/by-postcode/<string:pc>')
def get_dzByPc(pc):
    data = [x.to_dict()["datazone"] for x in model.Postcodes.by_datazone(pc)]
    return retJson(data)
    
