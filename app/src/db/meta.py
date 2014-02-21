import webapp2
import logging
import csv

from google.appengine.ext import deferred

from db.model import *

class UpdateDB(webapp2.RequestHandler):
    def get(self):
#        deferred.defer(update)
        update()
        self.response.out.write('meta.UpdateDB')

def update():
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

    dbMeta = Meta.query().get()

    if dbMeta is None:
        dbMeta = Meta()

    dbMeta.total_pop = sum_total
    dbMeta.total_child = sum_child
    dbMeta.total_work = sum_work
    dbMeta.total_pens = sum_pens

    dbMeta.put()
