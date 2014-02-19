# http://www.movable-type.co.uk/scripts/latlong-gridref.html

from math import *
import logging
logging.getLogger().setLevel(logging.WARNING)

class GeoRef():
	longitude = 0.0
	latitude = 0.0

	def __init__(self, x, y):
		self.longitude = x
		self.latitude = y

	@classmethod
	def fromGridRef(self, ref):
		E = ref.x
		N = ref.y

#		logging.info("Conversion from N " + str(E) + ", E " + str(N))
		
		a = 6377563.396
		b = 6356256.910
		F0 = 0.9996012717
		lat0 = 49*pi/180
		lon0 = -2*pi/180
		N0 = -100000
		E0 = 400000
		e2 = 1 - (b*b)/(a*a)
		n = (a-b)/(a+b)
		n2 = n*n
		n3 = n*n*n

		lat = lat0
		M = 0
		while (N-N0-M >= 0.00001):
			lat = (N-N0-M)/(a*F0) + lat
			Ma = (1 + n + (5/4)*n2 + (5/4)*n3) * (lat-lat0)
			Mb = (3*n + 3*n*n + (21/8)*n3) * sin(lat-lat0) * cos(lat+lat0)
			Mc = (((15/8)*n2 + (15/8)*n3)
						* sin(2*(lat-lat0))
						* cos(2*(lat+lat0)))
			Md = (35/24)*n3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
			M = b * F0 * (Ma - Mb + Mc - Md)

		cosLat = cos(lat)
		sinLat = sin(lat)
		nu = a*F0/sqrt(1-e2*sinLat*sinLat)
		rho = a*F0*(1-e2)/pow(1-e2*sinLat*sinLat, 1.5)
		eta2 = nu/rho-1

		tanLat = tan(lat)
		tan2lat = tanLat*tanLat
		tan4lat = tan2lat*tan2lat
		tan6lat = tan4lat*tan2lat
		secLat = 1/cosLat
		nu3 = nu*nu*nu
		nu5 = nu3*nu*nu
		nu7 = nu5*nu*nu
		VII = tanLat/(2*rho*nu)
		VIII = tanLat/(24*rho*nu3)*(5+3*tan2lat+eta2-9*tan2lat*eta2)
		IX = tanLat/(720*rho*nu5)*(61+90*tan2lat+45*tan4lat)
		X = secLat/nu
		XI = secLat/(6*nu3)*(nu/rho+2*tan2lat)
		XII = secLat/(120*nu5)*(5+28*tan2lat+24*tan4lat)
		XIIA = secLat/(5040*nu7)*(61+662*tan2lat+1320*tan4lat+720*tan6lat)

		dE = (E-E0)
		dE2 = dE*dE
		dE3 = dE2*dE
		dE4 = dE2*dE2
		dE5 = dE3*dE2
		dE6 = dE4*dE2
		dE7 = dE5*dE2
		lat = lat - VII*dE2 + VIII*dE4 - IX*dE6
		lon = lon0 + X*dE - XI*dE3 + XII*dE5 - XIIA*dE7

		return self(lat*180/pi, lon*180/pi)

class GridRef():
	x = 0													# easting
	y = 0													# northing

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def distance(self, a):
		dx = a.x - self.x
		dy = a.y - self.y
		return sqrt(dx*dx+dy*dy)
