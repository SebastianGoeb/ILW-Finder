import webapp2
import logging
import csv

from google.appengine.ext import deferred

from db.model import *

class UpdateDB(webapp2.RequestHandler):
    def get(self):
#        deferred.defer(update)
        update()
        self.response.out.write('meta.UpdateDB')

def update():
    
