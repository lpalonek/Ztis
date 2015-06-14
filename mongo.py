import pymongo
import unicodecsv
from bson.code import Code


class Mongo:
	def __init__(self, database, collectionName):
		self.client = pymongo.MongoClient('localhost', 27017)
		self.db = self.client[database]
		self.collection = self.db[collectionName]

	def getCollection(self):
		return self.collection

	def insertCollection(self, list):
		for item in list:
			self.insertItem(item)

	def insertItem(self, item):
		self.collection.insert_one(item)

	def cloneCollection(self, copyName):
		print(self.collection.find().count())
		newCollection = self.db[copyName]
		newCollection.drop()
		newCollection.insert_many(list(self.collection.find()))
		self.collection = newCollection

	def removeDuplicates(self):
		result = list(self.collection.aggregate([{"$group": {
			"_id": {"url": "$url"},
			"uniqueIds": {"$addToSet": "$_id"},
			"count": {"$sum": 1}
		}},
			{"$match": {
				"count": {"$gte": 2}
			}}, ]))
		for item in result:
			first = True
			for object in item['uniqueIds']:
				if first:
					first = False
					continue
				self.collection.delete_one({"_id":object})
		print(len(result))

	def get_locations_pairs(self):
		pairs = []
		with open('locations_pars.csv', 'w') as out:
			csv_out = unicodecsv.writer(out)
			for post in self.collection.find({"locations": {"$not": {"$size": 0}}}, {"locations": 1} ):
				for i in range(0,len(post['locations'])):
					for j in range(i+1,len(post['locations'])):
						pairs.append( (post['locations'][i],post['locations'][j]))
						csv_out.writerow([post['locations'][i],post['locations'][j]])

	def get_persons_pairs(self):
		pairs = []
		with open('persons_pars.csv', 'w') as out:
			csv_out = unicodecsv.writer(out)
			print self.collection.find({"persons": {"$not": {"$size": 0}},"published": {'$regex': '2015-05-0[1,2,3,4,5,6,7]*'}}, {"persons": 1} ).count()
			for post in self.collection.find({"persons": {"$not": {"$size": 0}},"published": {'$regex': '2015-05-0[1,2,3,4,5,6,7]*'}}, {"persons": 1} ):				
				for i in range(0,len(post['persons'])):
					for j in range(i+1,len(post['persons'])):
						pairs.append( (post['persons'][i],post['persons'][j]))
						csv_out.writerow([post['persons'][i],post['persons'][j]])						

	def removeNonEnglishArticles(self):
		print(self.collection.count())
		self.collection.delete_many({"language": {"$ne": "english"}})

	def mapReduceLocations(self):
		map = Code("function () {"
				"for(var id = 0; id < this.locations.length; id++){"
				   "var key = this.locations[id];"
    			"emit(key, 1);"
				   "}"
					"}")
		reduce = Code("function (k, vals) {"
    					"return Array.sum(vals);"
						"}")
		print(self.collection.count())
		return self.collection.map_reduce(map, reduce, "test").find()

	def findCustom(self, query):
		newCollection = self.db['test']
		newCollection.drop()
		newCollection.insert_many(list(self.collection.find(query)))
		return newCollection



