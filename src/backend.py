import webapp2
import logging

from db import postcodes

class OkHandler(webapp2.RequestHandler):
	def get(self):
		logging.warning("OkHandler is OK")
		self.response.out.write("ok")

main = webapp2.WSGIApplication([
	('/test/ok', OkHandler),
	('/updatedb/pc', postcodes.UpdateDB)
	])

init = webapp2.WSGIApplication([
	('/_ah/start', OkHandler)
	])
