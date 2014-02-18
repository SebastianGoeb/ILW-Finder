from __future__ import print_function
from flask import Flask
from dbmodel import *
from google.appengine.ext import ndb
import simplejson as json
from StringIO import StringIO

app = Flask(__name__)

@app.route('/')
def index():
	return getPostcodes()


@app.route('/get/postcodes')
def getPostcodes():
    output = StringIO()
    
    data = [x.to_dict() for x in Postcodes.get()]
    json.dump(data,output)
    return output.getvalue()
    

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
