from mongo import Mongo
from heatmap import HeatMap

def execute():
	mongo = Mongo('ztis', 'ztis-test')
	# mongo.cloneCollection('ztis-test')
	# mongo.removeNonEnglishArticles()
	# mongo.removeDuplicates()


	# heatMap = HeatMap(mongo.mapReduceLocations())
	# heatMap.setMap("map.png")

	mongo.collection = mongo.findCustom({"locations": {"$in": ["Poland", "PL"]}})

	heatMap = HeatMap(mongo.mapReduceLocations())
	heatMap.setMap("map2.png")

	# mongo = Mongo('ztis', 'ztis-test')

	# mongo.mapReduceLocations()

	# newMongo = Mongo('ztis', 'ztis-test')
	# newMongo.removeDuplicates()

execute()
