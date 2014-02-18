from flask import Flask, render_template
from dbmodel import *
from google.appengine.ext import ndb
import simplejson as json
from StringIO import StringIO

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("main.html")

@app.route('/test')
def testing():
    return getPostcodes()

@app.route('/get/postcodes')
def getPostcodes():
    output = StringIO()
    data = [x.to_dict() for x in Postcodes.get()]
    json.dump(data,output)
    

# ndb database classes
#class PostCode (ndb.Model):
#    id = int()
#    postocde = ndb.StringProperty(indexed=False)
#    x_coord = float()
#    y_coords = float()
#
#class District (ndb.Model):
#    id = int()
#    name = ndb.StringProperty(indexed = False)
#
#class Person (ndb.Model):
#    id = int()
#    district_id = int()
#    postcode_id = int()
#
#class PlaceCat(ndb.Model):
#    id = int()
#    cat_name = ndb.StringProperty(indexed = False)
#    
#class PublicPlace(ndb.Model):
#    id = int()
#    cat_id = int()
#    postcode_id = int()
>>>>>>> 73b99127d9cddf16b1bb4345611861596e1da8b2
