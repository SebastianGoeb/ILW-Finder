import webapp2
import logging
import csv

from db import model

class UpdateDB(webapp2.RequestHandler):
	def get(self):
		self.update()
		self.response.out.write('finished postcodes.UpdateDB')

	def update(self):
		logging.info("Updating PostCode data from local Council Data")
		n_pcs = 0
		with csv.DictReader(open('db-nat-neigh/Survey Data.csv', 'r')) as f:
			for row in f:
				try:
					model.Postcodes(postcode = row["Pcode"].replace(' ', '').upper(),
													x_coord = int(row["Xcord"]),
													y_coord = int(row["Ycord"]),
													datazone = 0).put()
					n_pcs += 1
				except Exception as e:
					logging.error("Exception: at "+str(i_row)+" ("+' '.join(e.args)+")")
		logging.info("Successfully read " + n_pcs  + " entries")
