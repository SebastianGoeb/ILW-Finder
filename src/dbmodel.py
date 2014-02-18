from google.appengine.ext import ndb

# ndb database classes
class Postcodes (ndb.Model):
    id = ndb.IntegerProperty()
    postcode = ndb.StringProperty()
    x_coord = ndb.FloatProperty()
    y_coord = ndb.FloatProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()
    @classmethod
    def get_id(cls, id):
        return cls.query().fetch(1)

class District (ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty(indexed = False)
    
    @classmethod
    def get(cls):
        return cls.query().fetch()
    @classmethod
    def get_id(cls, id):
        return cls.query().fetch(1)

class Person (ndb.Model):
    id = ndb.IntegerProperty()
    district_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()
    @classmethod
    def get_id(cls, id):
        return cls.query().fetch(1)

class PlaceCat(ndb.Model):
    id = ndb.IntegerProperty()
    cat_name = ndb.StringProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()
    @classmethod
    def get_id(cls, id):
        return cls.query().fetch(1)
    
class PublicPlace(ndb.Model):
    id = ndb.IntegerProperty()
    cat_id = ndb.IntegerProperty()
    postcode_id = ndb.IntegerProperty()
    
    @classmethod
    def get(cls):
        return cls.query().fetch()
    @classmethod
    def get_id(cls, id):
        return cls.query().fetch(1)
