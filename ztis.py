import time
import requests
import urllib.parse
import random

from mongo import Mongo

def getBaseUrl():
	return "https://webhose.io/"

def getKey():
	# this is very bad, but I don't care
	with open('api_keys.txt', 'r') as f:
		lines = f.readlines()
	return lines[random.randint(0,len(lines)-1)].strip()

def getUrl(query):
	webhoseKey = getKey()
	print(webhoseKey)
	webhoseUrl = getBaseUrl()+"search?token="+webhoseKey+"&format=json&q="+query
	return webhoseUrl

def getResponseQuery(query):
	parsedQuery = parseStringToUrl(query)
	result = requests.get(getUrl(parsedQuery))
	return result

def getResponseNext(url):
	print(url)
	return requests.get(getBaseUrl()+url)

def parseStringToUrl(string):
	parse = urllib.parse
	return parse.quote(string)

def getPosts(response):
	json = response.json()
	return json['posts']

def execute(string):
	response = getResponseQuery(string)
	posts = getPosts(response)
	counter = len(posts)
	while(counter > 0):
		response = getResponseNext(response.json()['next'])
		print(response.json()['next'])
		newPosts = getPosts(response)
		posts += newPosts
		counter = len(newPosts)
		print(counter)
	print(len(posts));
	mongo = Mongo("ztis","ztis")
	mongo.insertCollection(posts)

execute("nato europe")
execute("nato poland")
execute("army poland")
execute("isis")
execute("isis nato")
execute("europe army")
