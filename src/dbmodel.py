from google.appengine.ext import ndb

# ndb database classes
class Postcodes (ndb.Model):
    postcode = ndb.StringProperty()
    x_coord = ndb.IntegerProperty()
    y_coord = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()

class District (ndb.Model):
    name = ndb.StringProperty(indexed = False)
    
    @classmethod
    def get(cls):
        return cls.query().fetch()

class Person (ndb.Model):
    district_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()

class PlaceCat(ndb.Model):
    cat_name = ndb.StringProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()
    
class PublicPlace(ndb.Model):
    cat_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()
