#import webapp2
import logging
import csv
from math import *
from coords import *

#from google.appengine.ext import deferred

#from db import model

schools_Coord = []
playArea_Coord = []
parksAndGardens_Coord = []
museumsAndGalleries_Coord = []
SportsFacilities_Coord = []
postCode_Coord = []
postCode_Dictionary = []

with open('../../../datasets/schools/All schools.csv', 'r') as f_in:
		csv_in = csv.DictReader(f_in)
		for row in csv_in:
			schools_Coord.append((float(row['X_COORD']), float(row['Y_COORD'])))


#print schools_Coord

with open('../../../datasets/Play areas.csv', 'r') as f_in:
		csv_in = csv.DictReader(f_in)
		for row in csv_in:
			x = float((row['Location map'].split(','))[0])
			y = float((row['Location map'].split(','))[1])
			g = GridRef(0, 0)
			cord = GeoRef(x, y)
			x = g.fromGeoRef(cord).x
			y = g.fromGeoRef(cord).y
			playArea_Coord.append((x, y))
			
			


#print playArea_Coord

with open('../../../datasets/Parks and gardens.csv', 'r') as f_in:
		csv_in = csv.DictReader(f_in)
		for row in csv_in:
			x = float((row['Location map'].split(','))[0])
			y = float((row['Location map'].split(','))[1])
			g = GridRef(0, 0)
			cord = GeoRef(x, y)
			x = g.fromGeoRef(cord).x
			y = g.fromGeoRef(cord).y
			parksAndGardens_Coord.append((x, y))

#print parksAndGardens_Coord

with open('../../../datasets/Museums and galleries.csv', 'r') as f_in:
		csv_in = csv.DictReader(f_in)
		for row in csv_in:
			if (row['Location'] != ''):
				x = float((row['Location'].split(','))[0])
				y = float((row['Location'].split(','))[1])
				g = GridRef(0, 0)
				cord = GeoRef(x, y)
				x = g.fromGeoRef(cord).x
				y = g.fromGeoRef(cord).y
				museumsAndGalleries_Coord.append((x, y))

#print museumsAndGalleries_Coord

with open('../../../datasets/Sports and recreational facilities.csv', 'r') as f_in:
		csv_in = csv.DictReader(f_in)
		for row in csv_in:
			if (row['Location'] != ''):
				x = float((row['Location'].split(','))[0])
				y = float((row['Location'].split(','))[1])
				g = GridRef(0, 0)
				cord = GeoRef(x, y)
				x = g.fromGeoRef(cord).x
				y = g.fromGeoRef(cord).y
				SportsFacilities_Coord.append((x, y))

#print SportsFacilities_Coord

with open('../../../natural-neighbourhoods/Survey Data.csv', 'r') as f_in:
		csv_in = csv.DictReader(f_in)
		for row in csv_in:
			if (row['Xcord'] != 'Xcord' and row['Xcord'] != '#N/A' and row['Xcord'] != ''):
				x = float(row['Xcord'])
			if (row['Ycord'] != 'Ycord' and row['Ycord'] != '#N/A' and row['Ycord'] != ''):
				y = float(row['Ycord'])
			postCode_Coord.append((x, y))	

#print (postCode_Coord)

def distance((x1, y1), (x2, y2)):
	return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def weight_Calc((x, y), public_place):
	weight = 0
	for i in public_place:
		weight += (1/(distance((x, y), i)**2))
	return weight
				
for postCode in postCode_Coord:
	dic = {}
	val = weight_Calc(postCode, schools_Coord)
	dic["school"] = val
	val = weight_Calc(postCode, playArea_Coord)
	dic["playArea"] = val
	val = weight_Calc(postCode, parksAndGardens_Coord)
	dic["parksAndGardens"] = val
	val = weight_Calc(postCode, museumsAndGalleries_Coord)
	dic["museumsAndGalleries"] = val
	val = weight_Calc(postCode, SportsFacilities_Coord)
	dic["SportsFacilities"] = val
	postCode_Dictionary.append(dic)

print postCode_Dictionary






