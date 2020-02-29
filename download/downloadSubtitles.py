#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://gist.github.com/philgruneich/6bd621e9802d23257d1e6d17c23d3e49

# https://onetapless.com/download-subtitles-hazel

# Downloads Subtitles using the Open Subtitles API based on https://github.com/Tulifer/OpenSubtitles and suited for Hazel

from __future__ import unicode_literals
from __future__ import print_function
import xmlrpclib
import base64
import zlib
import random
import os
import struct
import sys

class OpenSubtitle:
	url = 'http://api.opensubtitles.org/xml-rpc'
	infoVideo = infoVideo = {'hash':'', 'imdbid':'', 'name':'', 'year':'', 'season':'', 'episode':'', 'size':'', 'hashSub':'', 'nameData':''}
	subHash = []
	language = {'en': 1, 'pb': 2}
	srtPath = ""
	
	def __init__(self,hashVideo,size,name,path):
		self.infoVideo['hash'] = hashVideo
		self.infoVideo['size'] = size
		self.infoVideo['nameData'] = name
		self.srtPath = path
			
	def serverInfo(self):
		server = xmlrpclib.Server(self.url)
		return server.ServerInfo()
	
	def Login(self):
		server = xmlrpclib.Server(self.url)
		resp = server.LogIn("","","en","MyApp V2")
		self.token = str(resp["token"])
		return (resp)
	
	def CheckSubHash(self):
		server = xmlrpclib.Server(self.url)
		resp = server.CheckSubHash(self.token,[self.infoVideo['hashSub']])
		return (resp)
		
	def CheckMovieHash(self):
		server = xmlrpclib.Server(self.url)
		resp = server.CheckMovieHash(self.token,[self.infoVideo['hash']])

		if len(resp['data'][self.infoVideo['hash']]) != 0:
			self.infoVideo['imdbid'] = str(resp['data'][self.infoVideo['hash']]['MovieImdbID'])
			self.infoVideo['name'] = str(resp['data'][self.infoVideo['hash']]['MovieName'])
			self.infoVideo['year'] = str(resp['data'][self.infoVideo['hash']]['MovieYear'])
			self.infoVideo['season'] = str(resp['data'][self.infoVideo['hash']]['SeriesSeason'])
			self.infoVideo['episode'] = str(resp['data'][self.infoVideo['hash']]['SeriesEpisode'])
		else:
			resp = 'Error'
		return (resp)
	
	def CheckMovieHash2(self):
		server = xmlrpclib.Server(self.url)
		resp = server.CheckMovieHash2(self.token,[self.infoVideo['hash']])

		if self.infoVideo['hash'] in resp['data']:
			self.infoVideo['imdbid'] = resp['data'][self.infoVideo['hash']][0]['MovieImdbID']
			self.infoVideo['name'] = resp['data'][self.infoVideo['hash']][0]['MovieName']
			self.infoVideo['year'] = resp['data'][self.infoVideo['hash']][0]['MovieYear']
			self.infoVideo['season'] = resp['data'][self.infoVideo['hash']][0]['SeriesSeason']
			self.infoVideo['episode'] = resp['data'][self.infoVideo['hash']][0]['SeriesEpisode']
		else:
			resp = 'Error'

		return (resp)
	
	def SearchSubtitles(self,order):
		server = xmlrpclib.Server(self.url)
		content = []
		
		if(order == 1):
			content.append( { 'moviehash':self.infoVideo['hash'],
		   					   'moviebytesize':self.infoVideo['size']} )
		elif(order ==2):
			content.append( { 'imdbid':self.infoVideo['imdbid']} )

		elif(order == 3):
			content.append( { 'name':self.infoVideo['name']} )
		elif(order==4):
			content.append( { 'query':self.infoVideo['name'],
								  'season':self.infoVideo['season'],
							     'episode':self.infoVideo['episode']} )
		else:
			content.append( { 'query':self.infoVideo['nameData']})
		resp = server.SearchSubtitles(self.token, content)
		try:
			for i in range(0,len(resp['data'])):
				self.subHash.append({'id':resp['data'][i]['IDSubtitleFile'],'hashSub':resp['data'][i]['SubHash'],'lang':resp['data'][i]['ISO639'], 'userRank':resp['data'][i]['UserRank'], 'bad': resp['data'][i]['SubBad'], 'count': resp['data'][i]['SubDownloadsCnt']})
		except:
			resp = 'Error'
		
		return (resp)

	def DownloadSubtitles(self,):
		server = xmlrpclib.Server(self.url)
		resp= ""
		sub = sorted([d for d in list({v['id']:v for v in self.subHash}.values()) if str(d['bad']) == '0' and d['lang'] in self.language.keys()], key=lambda x: (self.language[x['lang']], len(x['userRank']), int(x['count'])), reverse=True)
		resp = server.DownloadSubtitles(self.token,[sub[0]['id']])
		resp = base64.standard_b64decode(resp['data'][0]['data'])
		resp = zlib.decompress(resp, 47 )
		rnd = random.randrange(1000,999999)

		sub_file = self.infoVideo['nameData'][:-4] + '.srt'

		f = open(self.srtPath + sub_file,'wb')
		f.write(resp)
		f.close()
		return ()
		
	def InsertMovieHash(self):
		server = xmlrpclib.Server(self.url)
		content = []
		content.append( { 'moviehash':self.infoVideo['hash'], 'moviebytesize':self.infoVideo['size'], 'imdbid':self.infoVideo['imdbid']} )

		self.resp = server.InsertMovieHash(self.token,content)
		return (self.resp)

	def Logout(self):
		server = xmlrpclib.Server(self.url)
		server.LogOut(self.token)

def calc_file_hash(filepath):
	''' Calculates the hash value of a movie.
		 Edited from from OpenSubtitles\'s own examples:
		 http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes'''
		
	try:
		longlongformat = 'q'  # long long
		bytesize = struct.calcsize(longlongformat)

		f = open(filepath, 'rb')

		filesize = os.path.getsize(filepath)
		filehash = filesize

		if filesize < 65536 * 2:
			raise Exception('SizeError: Minimum file size must be 120Kb')

		for x in range(65536 // bytesize):
			buffer = f.read(bytesize)
			(l_value, ) = struct.unpack(longlongformat, buffer)
			filehash += l_value
			filehash = filehash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

		f.seek(max(0, filesize - 65536), 0)
		for x in range(65536 // bytesize):
			buffer = f.read(bytesize)
			(l_value, ) = struct.unpack(longlongformat, buffer)
			filehash += l_value
			filehash = filehash & 0xFFFFFFFFFFFFFFFF

		f.close()
		filehash = '%016x' % filehash
		return filehash
	except IOError:
		raise

if len(sys.argv) > 1:
	locVideo = sys.argv[1]
	splitVideo = locVideo.decode('utf-8').split("/")
	nameFichier = splitVideo[-1]
	srtPath = "/".join(splitVideo[:-1]) + "/"
	taille = os.path.getsize(locVideo)
	valueOfHash = calc_file_hash(locVideo)
	OS = OpenSubtitle(valueOfHash,taille,nameFichier, srtPath)
	OS.serverInfo()
	OS.Login()

	if OS.CheckMovieHash() != 'Error' or OS.CheckMovieHash2() != 'Error':
		if OS.SearchSubtitles(1) != 'Error' or OS.SearchSubtitles(2) != 'Error' or OS.SearchSubtitles(3) != 'Error' or OS.SearchSubtitles(4) != 'Error' or OS.SearchSubtitles(5) != 'Error':
			OS.DownloadSubtitles()
			OS.Logout()
			print(True)
		else:
			OS.Logout()
			print(False)
	else:
		OS.Logout()
		print(False)
else:
	print(False)
