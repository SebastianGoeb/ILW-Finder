from flask import Flask, render_template
from db import model
from google.appengine.ext import ndb
import simplejson as json
from StringIO import StringIO
import sys
import os.path
import logging

from coords import *

logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.debug = True

# def retJson(obj):
#     output = StringIO()
#     json.dump(obj, output)
#     return output.getvalue()

@app.route('/')
def index():
    #postcode = model.Postcodes.get().fetch()[0]
    #r = GeoRef.fromGridRef(GridRef(postcode.grid_x, postcode.grid_y))
    return render_template("main.html",
                           ref2 = GridRef.fromGeoRef(GeoRef(55.96216931484757, -3.198603458349107)),
                           lat = 55.95, lon = -3.2,
                           postcode = "EH1 1LY")

@app.route('/gamma')
def index_gamma():
    return render_template("head2.html",
                           ref2 = GridRef.fromGeoRef(GeoRef(55.96216931484757, -3.198603458349107)),
                           lat = 55.95, lon = -3.2,
                           postcode = "EH1 1LY")
    
# @app.route('/updatedb/dz/<indicator>')
# def route_updatedb_dz():
#     return

# @app.route('/updatedb/pc')
# def route_updatedb_pc():
#     update_pc(reinit=True)

# @app.route('/backend/updatedb')
# def updatedb():
#     taskqueue.add(name='updatedb')

# @app.route('/test')
# def testing():
#     return getPostcodes()

# @app.route('/get/postcodes')
# def getPostcodes():
#     output = StringIO()
#     data = [x.to_dict() for x in Postcodes.get().fetch()]
#     return retJson(data)

# @app.route('/get/districts')
# def getDistricts():
#     output = StringIO()
#     data = [x.to_dict() for x in District.get().fetch()]
#     return retJson(data)

# @app.route('/get/persons')
# def getPersons():
#     output = StringIO()
#     return ""
