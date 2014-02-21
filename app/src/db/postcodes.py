import webapp2
import logging
import csv

from google.appengine.ext import deferred

from db.model import *

class UpdateDB(webapp2.RequestHandler):
    def get(self):
#        deferred.defer(update)
        update()
        self.response.out.write('postcodes.UpdateDB')

def update():
    logging.info("Updating Postcode data from local Council Data")
    n_pcs = 0
    invalid_postcodes = re.compile(
        r"((((South|West|East|North)\s)+Edinburgh)|(NN not supplied))",
        re.IGNORECASE)
    with open('data/natural-neighbourhoods-survey.csv', 'r') as f_in:
        csv_in = csv.DictReader(f_in)
        for row in csv_in:
            try:
                if ((int(row["Xcord"]) != 0)
                    and (int(row["Ycord"]) != 0)
                    and (len(invalid_postcodes.findall(row["Allocated  NN"]))
                         == 0)):
                    pcString = row["Pcode"].strip().upper()
                    
                    dbPostcode = Postcodes.query(
                        Postcodes.postcode == pcString).get()

                    if dbPostcode is None:
                        dbPostcode = Postcodes(
                            postcode = pcString,
                            grid_x = int(row["Xcord"]),
                            grid_y = int(row["Ycord"]),
                            districts = []
                        )
                    else:
                        continue
                    
                    district_names = row["Allocated  NN"].split('/')

                    for d in district_names:
                        dbDistrictKey = District.query(
                            District.name == d).get()
                        if dbDistrictKey is None:
                            dbDistrictKey = District(name = d).put()
                        else:
                            dbDistrictKey = dbDistrictKey.key
                        
                        dbPostcode.districts.append(dbDistrictKey)

                    dbPostcode.put()
                    n_pcs += 1
            except ValueError as e:
                logging.warning("Exception: at %i (%s)"
                                % (n_pcs, ' '.join(e.args)))
    logging.info("Successfully read %i entries" % (n_pcs))
    logging.info("Testing pulling")
                
