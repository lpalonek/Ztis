from mongo import Mongo
from heatmap import HeatMap

def execute():
	mongo = Mongo('ztis', 'ztis-test')
	heatMap = HeatMap(mongo.mapReduceLocations())
	heatMap.setMap("map.png")

	# mongo = Mongo('ztis', 'ztis-test')
	# mongo.cloneCollection('ztis-test')

	# mongo.removeNonEnglishArticles()
	# mongo.removeDuplicates()
	# mongo.mapReduceLocations()

	# newMongo = Mongo('ztis', 'ztis-test')
	# newMongo.removeDuplicates()

execute()
