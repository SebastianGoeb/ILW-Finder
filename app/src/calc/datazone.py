import webapp2
from model import *

class Calc(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('done')


def datazone(my_code):
    dbMyDatazone = Datazone.get_by_id(my_code)

    if dbMyDatazone is None:
        return


    dbMyPostcodes = Postcodes.query(
        Postcodes.datazone == dbMyDatazone.key).fetch()

    if dbMyPostcodes is None:
        return

    myDistricts = {}

    for pc in dbMyPostcodes:
        for district in pc.districts:
            if district not in myDistricts:
                myDistricts[district] = []
            myDistricts[district].append(pc)

    

    
    
    
