from flask import Flask, render_template
from dbmodel import *
from google.appengine.ext import ndb
import simplejson as json
from StringIO import StringIO

from coords import *

app = Flask(__name__)

def retJson(obj):
    output = StringIO()
    json.dump(obj, output)
    return output.getvalue()

@app.route('/')
def index():
	postcode = Postcodes.get().fetch()[0]
	r = GeoRef.fromGridRef(GridRef(postcode.x_coord, postcode.y_coord))
	return render_template("main.html",
												 lat = r.latitude, lon = r.longitude,
												 postcode = postcode.postcode)

@app.route('/test')
def testing():
    return getPostcodes()

@app.route('/get/postcodes')
def getPostcodes():
    output = StringIO()
    data = [x.to_dict() for x in Postcodes.get().fetch()]
    return retJson(data)

@app.route('/get/districts')
def getDistricts():
    output = StringIO()
    data = [x.to_dict() for x in District.get().fetch()]
    return retJson(data)
    
@app.route('/get/persons')
def getPersons():
    output = StringIO()
    return ""
