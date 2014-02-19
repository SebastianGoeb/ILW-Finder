import webapp2
import logging

from db import postcodes, fetch, datazone

class OkHandler(webapp2.RequestHandler):
	def get(self):
		logging.warning("OkHandler is OK")
		self.response.out.write("ok")

main = webapp2.WSGIApplication([
	('/test/ok', OkHandler),
	('/updatedb/pc', postcodes.UpdateDB),
	('/updatedb/dz', datazone.UpdateDB),
#	('/get/.*', fetch.Main)
	])

init = webapp2.WSGIApplication([
	('/_ah/start', OkHandler)
	])
