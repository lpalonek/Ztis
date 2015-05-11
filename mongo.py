import pymongo
from bson.code import Code

class Mongo:

	def __init__(self, database, collectionName):
		self.client = pymongo.MongoClient('localhost', 27017)
		self.db = self.client[database]
		self.collection = self.db[collectionName]

	def insertCollection(self, list: list):
		for item in list:
			self.insertItem(item)

	def insertItem(self, item):
		self.collection.insert_one(item)

	def cloneCollection(self, copyName):
		print(self.collection.find())
		newCollection = self.db[copyName]
		newCollection.drop()
		for doc in self.collection.find():
			# i feel sick when I see that O(n^2)
			if doc['language'] == "english" and not newCollection.find_one({"url":doc['url']}):
				newCollection.insert_one(doc)
		print(newCollection)

	def removeDuplicates(self):
		# unfortunately key is too long...
		map = Code("function () {"
    			"emit(this.url, 1);"
					"}")
		reduce = Code("function (k, vals) {"
    					"return Array.sum(vals);"
						"}")
		print(self.collection.count())
		self.collection.map_reduce(map, reduce, "test")



