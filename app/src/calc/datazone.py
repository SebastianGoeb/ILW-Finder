import webapp2
from model import *

class Calc(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('done')


def datazone(my_id):
    pc_here = Postcodes.query(Postcodes.datazone_id == my_id).fetch()
    
