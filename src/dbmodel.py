from google.appengine.ext import ndb

# ndb database classes
class Postcodes (ndb.Model):
    postcode = ndb.StringProperty()
    x_coord = ndb.FloatProperty()
    y_coord = ndb.FloatProperty()
    
    @classmethod
    def get(cls):
        return cls.query()
    def by_id(cls, id):
        return cls.Key(Postcodes, id).get()

class District (ndb.Model):
    name = ndb.StringProperty()
    x_coord = ndb.IntegerProperty()
    y_coord = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query()
    def by_id(cls, id):
        return cls.key(District, id).get()

class Person (ndb.Model):
    district_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query()

class PlaceCat(ndb.Model):
    cat_name = ndb.StringProperty()
    
    @classmethod
    def get(cls):
        return cls.query()
    
class PublicPlace(ndb.Model):
    cat_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query()
