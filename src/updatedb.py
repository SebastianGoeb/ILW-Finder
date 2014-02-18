import webapp2
from dbmodel import *
import csv
from google.appengine.ext import ndb, webapp
from google.appengine.api import background_thread
import logging

logging.getLogger().setLevel(logging.DEBUG)

def updatedb():
	scrape_neighbourhoods()
		
def scrape_neighbourhoods():
	if Postcodes.get():
		return											# Database already populated
	i_row = 0
	logging.info("Scraping neighbourhoods...")
	with open('db-nat-neigh/Survey Data.csv', 'r') as f_in:
		f = csv.reader(f_in)
		for row in f:
			if i_row == 0:
				i_row += 1
				continue								# skip header row
			i_row += 1
				# TODO: coordinates. What is their current meaning?
			Postcodes(id = int(i_row-1),
								postcode = row[3].replace(' ', '')).put()
	logging.info("Finished scraping neighbourhoods. "
							 + str(i_row - 1)  + " entries total")

class Main(webapp.RequestHandler):
	def get(self):
		background_thread.start_new_background_thread(updatedb, [])
		self.response.out.write('Done')

app = webapp2.WSGIApplication([('/_ah/start', Main)],
															debug=True)
