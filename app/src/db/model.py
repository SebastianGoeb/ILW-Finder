from google.appengine.ext import ndb

# ndb database classes

# let's not consider this as a postcode, but rather a person/entity
class Postcodes (ndb.Model):
    postcode = ndb.StringProperty()
    grid_x = ndb.IntegerProperty()
    grid_y = ndb.IntegerProperty()
    datazone_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query()

    @classmethod
    def by_datazone(cls, dz):
        return cls.query(cls.datazone == dz.id)

    @classmethod
    def by_postcode(cls, pc):
        return cls.query(cls.postcode == pc)
        
    def format_postcode(postcode):
        ret = {}
        ret["postcode"] = postcode.postcode
        #ret["district_name"] = postcode.district
        ret["grid_x"] = postcode.grid_x
        ret["grid_y"] = postcode.grid_y
        place_posts = PlacePostRel.query(postcode.id == PlaceZoneRel.postcode_id).fetch()
        ret["vals"] =[]
        for place_post in place_posts:
            entry = {}
            entry["place_name"] = PlaceCat.getName(place_post.place_cat_id)
            entry["val"] = place_post.val
            ret["vals"].append(entry)
        return ret
        
    # returns a postcode list by a zone_id that they belong to
    @classmethod
    def get_by_zone_id(cls, zone_id):
        postcodes = cls.query(zone_id == cls.datazone_id).fetch()
        ret = []
        for postcode in postcodes:
            ret.append(format)
        return ret
    @classmethod
    def getFull(cls):
        results = []
        for postcode in cls.query().fetch():
            f_post = format_postcode(postcode)
            results.append(f_post)
        return results

class Datazone (ndb.Model):
    id = ndb.IntegerProperty(indexed = True)
    code = ndb.IntegerProperty()
    grid_x = ndb.IntegerProperty()
    grid_y = ndb.IntegerProperty()

    pop_total = ndb.IntegerProperty()
    pop_child = ndb.IntegerProperty()
    pop_pens = ndb.IntegerProperty()
    pop_work = ndb.IntegerProperty()

    @classmethod
    def get(cls):
        return cls.query()

    @classmethod
    def by_code(cls, name):
        return cls.query(cls.code == name)
        
    @classmethod
    def getDatazones(cls):
        ret = []
        for dataZone in cls.query().fetch():
            results = {}
            postcodes = Postcodes.get_by_zone_id(dataZone.id)
            results["postcodes"] = postcodes;
            results["name"] = name;
            results["grid_x"] = grid_x;
            results["grid_y"] = grid_y;
            ret.append(results)
        return ret
            
'''class District (ndb.Model):
    name = ndb.StringProperty()
    x_coord = ndb.IntegerProperty()
    y_coord = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query()
    def by_id(cls, id):
        return cls.key(District, id).get()'''

'''class Person (ndb.Model):
    district_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query()'''

class PlaceCat(ndb.Model):
    id = ndb.IntegerProperty(indexed = True)
    name = ndb.StringProperty()
    
    @classmethod
    def get(cls):
        return cls.query()
        
    @classmethod
    def getName(cls, id):
        return cls.query(cls.id == id).fetch(1)[0].name

'''class PublicPlace(ndb.Model):
    cat_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query()'''

class PlacePostRel(ndb.Model):
    place_cat_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    val = ndb.FloatProperty()
    
    @classmethod
    def get(cls):
        return cls.query()
