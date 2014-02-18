from flask import Flask, render_template
from dbmodel import *
from google.appengine.ext import ndb
import simplejson as json
from StringIO import StringIO

from coords import *

app = Flask(__name__)

@app.route('/')
def index():
	postcode = Postcodes.get()[0]
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
    data = [x.to_dict() for x in Postcodes.get()]
    json.dump(data,output)
