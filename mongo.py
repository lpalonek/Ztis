import pymongo

class Mongo:

	def __init__(self):
		client = pymongo.MongoClient('localhost', 27017)
		db = client['ztis']
		self.collection = db['ztis']

	def insertCollection(self, list: list):
		for item in list:
			self.insertItem(item)

	def insertItem(self, item):
		self.collection.insert_one(item)
