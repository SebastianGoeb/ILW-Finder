import webapp2
import logging
import csv

from google.appengine.api import background_thread

from db import model

class UpdateDB(webapp2.RequestHandler):
	def get(self):
		background_thread.start_new_background_thread(self.update, [])
		self.response.out.write('finished postcodes.UpdateDB')

	def update(self):
		logging.info("Updating PostCode data from local Council Data")
		n_pcs = 0
		with open('db-nat-neigh/Survey Data.csv', 'r') as f_in:
			csv_in = csv.DictReader(f_in)
			for row in csv_in:
				try:
					model.Postcodes(postcode = row["Pcode"].replace(' ', '').upper(),
													grid_x = int(row["Xcord"]),
													grid_y = int(row["Ycord"]),
													datazone = 0).put()
					n_pcs += 1
				except Exception as e:
					logging.warning("Exception: at %i (%s)"
													% (n_pcs, ' '.join(e.args)))
		logging.info("Successfully read %i entries" % (n_pcs))
