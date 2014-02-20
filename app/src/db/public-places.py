import webapp2
import logging
from pprint import pprint
import csv
import re

from cStringIO import StringIO

from google.appengine.api import urlfetch
from google.appengine.ext import deferred
from urllib import urlencode

from db import model
from coords import *

logging.getLogger().setLevel(logging.DEBUG)

class UpdateDB(webapp2.RequestHandler):
    def get(self):
        deferred.defer(update_pubs)
        self.response.out.write('finished public-places.UpdateDB')
    

def update_pubs():
    pub_reg = re.compile(r".*public\s+house.*")
    with open('data/businesses.csv', 'r') as f_in:
        csv_in = csv.reader(f_in)
        for row in csv_in:
            
