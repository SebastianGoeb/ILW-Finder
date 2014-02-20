import webapp2
import logging
import csv

from google.appengine.ext import deferred

from db import model

class UpdateDB(webapp2.RequestHandler):
    def get(self):
        deferred.defer(update)
        self.response.out.write('postcodes.UpdateDB')

def update():
    logging.info("Updating Postcode data from local Council Data")
    n_pcs = 0
    with open('data/natural-neighbourhoods-survey.csv', 'r') as f_in:
        csv_in = csv.DictReader(f_in)
        for row in csv_in:
            try:
                if (int(row["Xcord"]) != 0
                    and int(row["Ycord"]) != 0
                    and row["Allocated  NN"] != "NN not supplied"):
                    names = '/'.split(row["Allocated  NN"])
                    model.Postcodes(
                        # TODO: represent multiple names as list?
                        postcode = row["Pcode"].strip().upper(),
                        grid_x = int(row["Xcord"]),
                        grid_y = int(row["Ycord"]),
                        datazone_id = 0,
                        district = row["Allocated  NN"]).put()
                    n_pcs += 1
            except Exception as e:
                logging.warning("Exception: at %i (%s)"
                                                % (n_pcs, ' '.join(e.args)))
    logging.info("Successfully read %i entries" % (n_pcs))
