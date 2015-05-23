from mongo import Mongo

def execute():
	mongo = Mongo('ztis', 'ztis-test')
	# mongo.cloneCollection('ztis-test')
	# mongo.removeNonEnglishArticles()
	# mongo.removeDuplicates()
	mongo.mapReduceLocations()

	# newMongo = Mongo('ztis', 'ztis-test')
	# newMongo.removeDuplicates()

execute()
