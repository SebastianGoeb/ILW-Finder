#import webapp2
import logging
import csv
from math import *
from coords import *

#from google.appengine.ext import deferred

import model

import logging
def extractPublicPlaces():
    cat_list = ["school","playArea","parksAndGardens","museumsAndGalleries","SportsFacilieties"]
    schools_Coord = []
    playArea_Coord = []
    parksAndGardens_Coord = []
    museumsAndGalleries_Coord = []
    SportsFacilities_Coord = []
    postCode_Coord = []
    postCode_Dictionary = {}
    with open('data/all-schools.csv', 'r') as f_in:
            csv_in = csv.DictReader(f_in)
            for row in csv_in:
                schools_Coord.append((float(row['X_COORD']), float(row['Y_COORD'])))


    #print schools_Coord

    with open('data/Play areas.csv', 'r') as f_in:
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

    with open('data/Parks and gardens.csv', 'r') as f_in:
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

    with open('data/Museums and galleries.csv', 'r') as f_in:
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

    with open('data/Sports and recreational facilities.csv', 'r') as f_in:
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

    with open('data/Survey Data.csv', 'r') as f_in:
            csv_in = csv.DictReader(f_in)
            for row in csv_in:
                if (row['Xcord'] != 'Xcord' and row['Xcord'] != '#N/A' and row['Xcord'] != ''):
                    x = float(row['Xcord'])
                if (row['Ycord'] != 'Ycord' and row['Ycord'] != '#N/A' and row['Ycord'] != ''):
                    y = float(row['Ycord'])
                code = row['Pcode']
                postCode_Coord.append((x, y, code))	

    #print (postCode_Coord)

    def distance((x1, y1), (x2, y2)):
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)


    def weight_Calc((x, y, z), public_place):
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
        postCode_Dictionary[postCode[2]] = dic
        dic["x"] = postCode[0]
        dic["y"] = postCode[1]
    return postCode_Dictionary
    
def storePublicPlaces():
    cat_list = ["school","playArea","parksAndGardens","museumsAndGalleries","SportsFacilieties"]
    public_dict = extractPublicPlaces()
    i = 1
    # deleting all the data first
    for cat in model.PlaceCat().query().fetch():
        cat.key.delete()
    for entry in model.PlacePostRel().query().fetch():
        entry.key.delete()
    for entry in model.Postcodes().query().fetch():
        entry.key.delete()
    
    #populating the database
    for cat in cat_list:
        db_entry = model.PlaceCat()
        db_entry.id = i
        db_entry.name = cat
        db_entry.put()
        i += 1
    j = 0
    for item in public_dict.items():
        post_entry = model.Postcodes()
        post_entry.grid_x = int(item[1]["x"])
        post_entry.grid_y = int(item[1]["y"])
        post_entry.id = j
        post_entry.postcode = item[0]
        post_entry.datazone_id = 0;
        post_entry.district = "Leith lol"
        post_entry.put()
        i = 1
        for cat in cat_list:
            relation_entry = model.PlacePostRel()
            relation_entry.place_cat_id = i
            relation_entry.postcode_id = j
            relation_entry.put()
            i+=1
        j +=1
    return "done"






