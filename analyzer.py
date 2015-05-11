from mongo import Mongo

def execute():
	mongo = Mongo('ztis', 'ztis')
	mongo.cloneCollection('ztis-test')

	# newMongo = Mongo('ztis', 'ztis-test')
	# newMongo.removeDuplicates()

execute()
