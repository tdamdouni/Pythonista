from __future__ import print_function
# https://forum.omz-software.com/topic/3178/intro-and-question-re-google-app-engine-and-web-stuff-in-pythonista/9

def test_upper(self):
	self.assertEqual('foo'.upper(), 'FOO')
	
def test_isupper(self):
	self.assertTrue('FOO'.isupper())
	self.assertFalse('Foo'.isupper())
	
def test_split(self):
	s = 'hello world'
	self.assertEqual(s.split(), ['hello', 'world'])
	# check that s.split fails when the separator is not a string
	with self.assertRaises(TypeError):
		s.split(2)
		
# --------------------

# coding: utf-8

# example from https://docs.python.org/2/library/socketserver.html

import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
	"""
	The request handler class for our server.
	
	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""
	
	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		print("ron jeffries has gotten something working part 2")
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		# just send back the same data, but upper-cased
		back = "here you go\n" + self.data.upper()
		self.request.sendall(back)
		
if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	
	# Create the server, binding to localhost on port 9999
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
	
# --------------------

# localhost:9999/?add&key=k1&val=v1

# --------------------

