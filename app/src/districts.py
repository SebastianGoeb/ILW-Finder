import sys
import webapp2
from model import *
import csv
from google.appengine.ext import ndb, webapp
from google.appengine.api import background_thread
import logging
from math import *

# command arguments
#parser = argparse.ArgumentParser(description='csv to postgres',\
 #fromfile_prefix_chars="@" )
#parser.add_argument('file', help='csv file to import', action='store')
#args = parser.parse_args()
#csv_file = args.file

logging.getLogger().setLevel(logging.DEBUG)

# open csv file
def updateDistricts():
	data = []
	neighBours = {}
	postcodes = {}

	with open('db-nat-neigh/Survey Data.csv', 'rb') as csvfile:
	     	
	    # get number of columns
#	    for line in csvfile.readlines():
#	        array = line.split(',')
#	        first_item = array[0]

#	    num_columns = len(array)
#	    csvfile.seek(0)

		reader = csv.reader(csvfile, delimiter=',')
		neighbourhood_col = 2
		postcode_col = 3
		x_coord_col = 4
		y_coord_col = 5

		for row in reader:
			postcode = row[postcode_col].upper().strip()# all upper case and whitespace trimmed
#			NNs = row[neighbourhood_col].split('/')
#			for nn in NNs:
#				if nn in neighBours:
#					neighBours[nn].update([(row[x_coord_col], row[y_coord_col])])
#				else:
#					neighBours[nn] = set([(row[x_coord_col], row[y_coord_col])])
			i = 0;
			if postcode in postcodes:
				postcodes[postcode] = Postcodes()
				i++
			else if isdigit(row[x_coord_col]) and isdigit(row[y_coord_col]):
				postcodes[postcode].x = int(row[x_coord_col])
				postcodes[postcode].y = int(row[y_coord_col])
		for postcode in postcodes:
			postcode.put()

class Main(webapp.RequestHandler):
	def get(self):
		background_thread.start_new_background_thread(updateDistricts, [])
		self.response.out.write('Updated Districts')

app = webapp2.WSGIApplication([('/_ah/start', Main)])





























