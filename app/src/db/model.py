from google.appengine.ext import ndb

# ndb database classes
class Postcodes (ndb.Model):
	postcode = ndb.StringProperty()
	grid_x = ndb.IntegerProperty()
	grid_y = ndb.IntegerProperty()
	datazone_id = ndb.IntegerProperty()
    
	@classmethod
	def get(cls):
		return cls.query()

	@classmethod
	def by_id(cls, id):
		# return cls.Key(Postcodes, id).get()
		return cls.query(cls.id == id)

	@classmethod
	def by_datazone(cls, dz):
		return cls.query(cls.datazone == dz.id)

	@classmethod
	def by_postcode(cls, pc):
		return cls.query(cls.postcode == pc)

class Datazone (ndb.Model):
	name = ndb.IntegerProperty()
	grid_x = ndb.IntegerProperty()
	grid_y = ndb.IntegerProperty()

	@classmethod
	def get(cls):
		return cls.query()

	@classmethod
	def by_name(cls, name):
		return cls.query(cls.name == name)
			

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
