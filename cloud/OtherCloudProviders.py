# coding: utf-8

# https://forum.omz-software.com/topic/2917/other-cloudproviders

import DAVServer, DAVClient, threading, pprint

port = DAVServer.getFreePort()

s = DAVServer.DAVServer(('localhost', port), DAVServer.DAVRequestHandler, DAVServer.DirCollection('./', '/'), '')
t = threading.Thread(target = s.serve_forever)
t.start()

c = DAVClient.DAVClient('localhost', port)
pprint.pprint(c.ls('site-packages'))

# ============


class __CloudProvider(object):
	"""implementation using WebDAV server modified to mimic secret Gist"""
	def putFileToURL(self, f):
		response = requests.session().request('PUT', 'http://localhost:' + str(port) + '/-', data = f)
		return response.headers['URL']
		
	def getFileFromURL(self, sURL):
		return urllib.urlopen('http://localhost:' + str(port) + '/' + sURL)

