import pymongo
from bson.code import Code


class Mongo:
	def __init__(self, database, collectionName):
		self.client = pymongo.MongoClient('localhost', 27017)
		self.db = self.client[database]
		self.collection = self.db[collectionName]

	def getCollection(self):
		return self.collection

	def insertCollection(self, list: list):
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

	def removeNonEnglishArticles(self):
		self.collection
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



