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
    return output.value()
