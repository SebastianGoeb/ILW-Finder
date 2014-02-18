import webapp2
from google.appengine.ext import ndb, webapp
from dbmodel import *
from coords import *
import simplejson as json

def req_testGetAllPostcodes(args):
	

class Main(webapp.RequestHandler):
	def post(self):
		
		self.response.out.write('Done')

app = webapp2.WSGIApplication([('/request', Main)],
															debug=True)
