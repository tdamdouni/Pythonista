# coding: utf-8

# https://medium.com/@jmoreno78/workflow-de-editorial-para-publicar-en-medium-8202a829aa45#.1ye2t8sqk

from __future__ import print_function
import urllib2
import json

contentTypeHeader = 'application/json'
acceptHeader =  'application/json'
acceptCharsetHeader = 'utf-8'
integrationToken = 'tu propio token de integracion'

urlUserInfo = 'https://api.medium.com/v1/me'

request = urllib2.Request(urlUserInfo)
request.add_header("Authorization", "Bearer %s" % integrationToken)
request.add_header("Content-Type", contentTypeHeader)
request.add_header("Accept", acceptHeader)
request.add_header("Accept-Charset", acceptCharsetHeader)
try:
	response = urllib2.urlopen(request)
except urllib2.HTTPError as e:
	if e.code == 401:
		print("The integration token is invalid")
		print(e.reason)
else:
	responseJson =  json.loads(response.read())
	authorId = responseJson["data"]["id"]
	
	urlPost = 'https://api.medium.com/v1/users/%s/posts' % authorId
	
	values = dict()
	values['title'] = "Hola Medium!"
	values['contentFormath'] = "html"
	values['content'] = "<h1>Hola Medium!</h1><p>Probando el API de Medium desde Pythonista.</p>"
	values['publishStatus'] = "draft"
	data = json.dumps(values)
	
	request = urllib2.Request(urlPost)
	request.add_header("Authorization", "Bearer %s" % integrationToken)
	request.add_header("Content-Type", contentTypeHeader)
	request.add_header("Accept", acceptHeader)
	request.add_header("Accept-Charset", acceptCharsetHeader)
	request.add_data(data)
	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError as e:
		if e.code == 400:
			print("Incorrect fields. Bad request")
			print(e.reason)
		elif e.code == 401:
			print("The integration token is invalid")
			print(e.reason)
		elif e.code == 403:
			print("User without permission to publish.")
			print(e.reason)
		elif e.code == 404:
			print("User unknown")
			print(e.reason)
		else:
			print("Ups! something is wrong with the world today...")
			print(e.reason)
	else:
		print(response.read())

