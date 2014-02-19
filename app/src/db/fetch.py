from flask import Flask
from StringIO import StringIO

from db import model

Main = Flask(__name__)

def retJson(obj):
    output = StringIO()
    json.dump(obj, output)
    return output.getvalue()


@Main.route('/get/postcodes')
def get_postcodes():
	data = [x.to_dict()["postcode"] for x in model.Postcodes.get().fetch()]
	return retJson(data)
