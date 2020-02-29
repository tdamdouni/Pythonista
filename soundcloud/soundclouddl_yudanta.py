# coding: utf-8

# https://gist.github.com/yudanta/9929507

#!/usr/bin/env python

#usage : python soundclouddl.py <soundcloud url track/list>

from __future__ import print_function
import soundcloud
import urllib
import re
import time
import os
import sys

CLIENT_ID = '6e481ce437f388ffa1701eca3689df15'
MEDIA_STREAM_URL = 'http://media.soundcloud.com/stream/'
DOWNLOAD_PATH = './downloads/'

class soundcloudDownloader:

	client = soundcloud.Client(client_id = CLIENT_ID)

	def __init__(self, url, *args, **kwargs):
		self.url = url
		self.download_progress = 0
		self.current_time = time.time()
		self.resolveMedia = self.resolve(url)
		self.mediaURl = self.getTrackMediaStreamUrl(self.resolveMedia)
		self.download_progress = 0

	#resolve return track_id, title, uri, waveform_url, streamable, downloadable in list
	def resolve(self, url):
		returnMedia = []

		resolveurl = self.client.get('/resolve', url=url);
		if resolveurl.kind == 'track':
			print('downloading track')
			returnMedia.append(self.getTrackDetail(resolveurl.id))
			
		elif resolveurl.kind == 'playlist':
			print('downloading playlist')
			for song in resolveurl.tracks:
				returnMedia.append(self.getTrackDetail(song['id']))

		return returnMedia

	def getTrackDetail(self, track_id):
		song = self.client.get('/tracks/' + str(track_id))

		song_data = {'track_id':song.id, 'title':song.title, 'uri':song.uri, 'waveform_url':song.waveform_url, 'streamable':song.streamable, 'downloadable':song.downloadable}

		return song_data

	#get direct url from waveform url
	def getTrackMediaStreamUrl(self, songs, *args, **kwargs):
		trackMediaURL = []
		regex = re.compile('\/([a-zA-Z0-9]+)_')

		for song in songs:
			r_url = regex.search(song['waveform_url'])
			stream_id = r_url.groups()[0]
			media_url = MEDIA_STREAM_URL + str(stream_id)
			trackMediaURL.append({'media_url':media_url, 'title':song['title']})

		return trackMediaURL

	def downloaStream(self, songs, *args, **kwargs):
		#download
		if not os.path.isdir(DOWNLOAD_PATH):
			os.mkdir(DOWNLOAD_PATH)

		for song in songs:
			filename = DOWNLOAD_PATH + "{0}.mp3".format(song['title'])
			#retrive file
			sys.stdout.write("\nDownloading: {0}\n".format(filename))
			urllib.urlretrieve(url=song['media_url'], filename=filename, reporthook=self.downloadProgress)

		return None

	def downloadProgress(self, block_no, block_size, file_size):
		self.download_progress += block_size
		if int(self.download_progress / 1024 * 8) > 1000:
			speed = "{0} Mbps".format(round((self.download_progress / 1024 / 1024 * 8) / (time.time() - self.current_time), 2))
		else:
			speed = "{0} Kbps".format(round((self.download_progress / 1024 * 8) / (time.time() - self.current_time), 2))
		rProgress = round(self.download_progress / 1024.00 / 1024.00, 2)
		rFile = round(file_size / 1024.00 / 1024.00, 2)
		percent = round(100 * float(self.download_progress) / float(file_size))
		sys.stdout.write("\r {3} ({0:.2f}/{1:.2f}MB): {2:.2f}%".format(rProgress, rFile, percent, speed))
		sys.stdout.flush()
		

#testing track url or sets url
link = sys.argv[1]

soundcloudDownload = soundcloudDownloader(link)
#media = soundcloudDownload.resolveMedia
streamUrl = soundcloudDownload.mediaURl
#downloading media
soundcloudDownload.downloaStream(streamUrl)