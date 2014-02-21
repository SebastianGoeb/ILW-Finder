import webapp2
import logging
from db.model import *

class Calc(webapp2.RequestHandler):
    def get(self):
        update_district_weights()
        self.response.out.write('done')

def update_district_weights():
    datazones = Datazone.get().fetch()
    sum_total = 0
    sum_child = 0
    sum_work  = 0
    sum_pens  = 0
    for dz in datazones:
        sum_total += dz.pop_total
        sum_child += dz.pop_child
        sum_work += dz.pop_work
        sum_pens += dz.pop_pens

    logging.info("Our population is %i" % (sum_total))

    dbDistricts = District.query().fetch()

    for d in dbDistricts:
        d_pop_total = 0
        
        dbPostcodes = Postcodes.query(
            Postcodes.districts == d.key).fetch()
        for pc in dbPostcodes:
            pcDatazone = pc.datazone.get()
            dzPopPerPC = (pcDatazone.pop_total
                          / pcDatazone.num_postcodes)
            d_pop_total += dzPopPerPC
        d.pop_total = d_pop_total
        d.pop_weight = float(d_pop_total) / float(sum_total)
        d.put()

    logging.info("Done updating district weights")

def datazone(my_code):
    datazones = model.Datazone.get().fetch()
    sum_total = 0
    sum_child = 0
    sum_work  = 0
    sum_pens  = 0
    for dz in datazones:
        sum_total += dz.pop_total
        sum_child += dz.pop_child
        sum_work += dz.pop_work
        sum_pens += dz.pop_pens
    
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

    

    
    
    
