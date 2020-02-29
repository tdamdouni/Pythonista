# coding: utf-8

# https://forum.omz-software.com/topic/3091/print-leaves-console-blank

from __future__ import print_function
import webbrowser
import httplib
import sys
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
	t=''
	def handle_data(self, data):
		if len(data) > 40:
			self.t = self.t + '\n' + data
	def get_text(self):
		return self.t
		
class textfromweb:
	def get_weather_text(self):
		text = ''
		hc=httplib.HTTPConnection('prognoza.hr:80', timeout=50)
		hc.connect()
		hc.request("GET","http://prognoza.hr/prognoze_e.php?id=jadran_n")
		r = hc.getresponse()
		data = r.read()
		parser = MyHTMLParser()
		parser.feed(data)
		self.text = parser.get_text()
		hc.close()
		return self.text
		
t = textfromweb()
print(t.get_weather_text())

# -------------------

# @omz

from HTMLParser import HTMLParser
import requests

class MyHTMLParser(HTMLParser):
	t=''
	def handle_data(self, data):
		if len(data) > 40:
			self.t = self.t + '\n' + data
	def get_text(self):
		return self.t
		
class textfromweb:
	def get_weather_text(self):
		r = requests.get('http://prognoza.hr/prognoze_e.php?id=jadran_n', timeout=50)
		data = r.text
		parser = MyHTMLParser()
		parser.feed(data)
		self.text = parser.get_text()
		return self.text
		
t = textfromweb()
print(t.get_weather_text())

