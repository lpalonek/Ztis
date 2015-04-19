import json
import requests
import urllib.parse

from mongo import Mongo

def getBaseUrl():
	return "https://webhose.io/"

def getKey():
	return "38b97d09-9393-49f7-8d86-38fc688df1bc"

def getUrl(query):
	webhoseKey = getKey()
	webhoseUrl = getBaseUrl()+"search?token="+webhoseKey+"&format=json&q="+query
	return webhoseUrl

def getResponseQuery(query):
	parsedQuery = parseStringToUrl(query)
	result = requests.get(getUrl(parsedQuery))
	return result

def getResponseNext(url):
	return requests.get(getBaseUrl()+url)

def parseStringToUrl(string):
	parse = urllib.parse
	return parse.quote(string)

def getPosts(response):
	json = response.json()
	return json['posts']

def execute():
	response = getResponseQuery("military poland")
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
	mongo = Mongo()
	mongo.insertCollection(posts)

	return posts

execute()