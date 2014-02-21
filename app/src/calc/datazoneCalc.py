import webapp2
import logging
from db.model import *
import colorsys
from math import *

class Calc(webapp2.RequestHandler):
    def get(self):
        update_district_weights()
        update_dz_hues()
        self.response.out.write('done')

def update_district_weights():
    datazones = Datazone.get().fetch()
    sum_total = 0
    sum_child = 0
    sum_work  = 0
    sum_pens  = 0
    for dz in datazones:
        if dz.pop_total is not None:
            sum_total += dz.pop_total
            sum_child += dz.pop_child
            sum_work += dz.pop_work
            sum_pens += dz.pop_pens

    logging.info("Our population is %i" % (sum_total))

    dbDistricts = District.query().fetch()

    dCount = len(dbDistricts)
    colK = 1/float(dCount)
    colK_cur = colK

    for d in dbDistricts:
        d_pop_total = 0
        
        dbPostcodes = Postcodes.query(
            Postcodes.districts == d.key).fetch()
        for pc in dbPostcodes:
            pcDatazone = pc.datazone.get()
            if pc.population is not None:
                d_pop_total += pc.population
        d.pop_total = int(d_pop_total)
        d.pop_weight = float(d_pop_total) / float(sum_total)
        d.colour_hue = colK_cur
        colK_cur += colK
        d.put()

    logging.info("Done updating district weights")

def update_dz_hues():
    dbDatazones = Datazone.get().fetch()

    for dz in dbDatazones:
        myDistricts = {}
        myDistrictPop = 0
        
        hue_x = 0
        hue_y = 0
        
        dbPostcodes = Postcodes.query(
            Postcodes.datazone == dz.key).fetch()
        for pc in dbPostcodes:
            pcPop = 0
            if pc.population is not None:
                pcPop = pc.population / len(pc.districts)
            for district in pc.districts:
                did = district.id()
                district = district.get()
                myDistrictPop += pcPop
                if did not in myDistricts:
                    myDistricts[did] = {
                        'postcodes':[pc],
                        'pop':pcPop,
                        'hue':district.colour_hue
                    }
                    hue_x += cos(district.colour_hue * 2 * pi)
                    hue_y += sin(district.colour_hue * 2 * pi)
                else:
                    myDistricts[did]['postcodes'].append(pc)
                    myDistricts[did]['pop'] += pcPop

        dz.colour_hue = atan2(hue_y, hue_x)

        for d in myDistricts:
            if myDistricts[d]['pop'] > 0:
                w = myDistricts[d]['pop'] / myDistrictPop
                h = myDistricts[d]['hue']

                hue_x += w * (h * 2 * pi)
                hue_y += w * (h * 2 * pi)
        
                hue_delta_avg = atan2(hue_y, hue_x)
                dz.colour_hue += hue_delta_avg

        dz.colour_hue %= 2*pi
        if dz.colour_hue < 0:
            dz.colour_hue = 2*pi + dz.colour_hue

        dz.colour_hue /= 2*pi
        
        dz.put()
    logging.info("All colour hues specified.")
        

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

    

    
    
    
