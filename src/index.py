from flask import Flask
from google.appengine.ext import ndb

app = Flask(__name__)

@app.route('/')
def index():
	return 'Index cia Flask'


# ndb database classes
class PostCode (ndb.Model):
    id = int()
    postocde = ndb.StringProperty(indexed=False)
    x_coord = float()
    y_coords = float()

class District (ndb.Model):
    id = int()
    name = ndb.StringProperty(indexed = False)

class Person (ndb.Model):
    id = int()
    district_id = int()
    postcode_id = int()

class PlaceCat(ndb.Model):
    id = int()
    cat_name = ndb.StringProperty(indexed = False)
    
class PublicPlace(ndb.Model):
    id = int()
    cat_id = int()
    postcode_id = int()