from flask import Flask
from StringIO import StringIO
import simplejson as json

import logging

from db import model

from coords import *

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

@Main.route('/get/georef/of-postcode/<string:pc>')
def get_idOfPc(pc):
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
	
