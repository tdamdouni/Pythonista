#!/usr/bin/env python

"""
Audio playback with pyaudio, tkSnack, pyglet or console media player depending on availability.
Pranav Ravichandran <me@onloop.net>
"""

import wave
import os
import sys
import string

pyaudioFound = False
tkSnackFound = False
pygletFound = False

try:
	import pyaudio
	pyaudioFound = True
except ImportError:
	try:
		import tkSnack
		tkSnackFound = True
	except ImportError:
		try:
			import pyglet
			pygletFound = True
		except ImportError:
			print "Audio playback frameworks not found. Install one of pyaudio, tkSnack or pyglet."

class Sound:
	def __init__(self, fn = None):
		pass

	def load(self, fn):
		pass

	def playFile(self, mediaFile, repeat = 0):
		''' Play the .wav file.'''

		for n in range(repeat + 1):
			if pyaudioFound:
				self.play_pyaudio(mediaFile)
			elif tkSnackFound:
				self.play_tkSnack(mediaFile)
			elif pygletFound:
				self.play_pyglet(mediaFile)
			else:
				self.play_media(mediaFile)

	def play_pyaudio(self, mediaFile):
		''' Use pyaudio backend to play the .wav.'''

		chunk = 1024
		wf = wave.open(mediaFile, 'rb')
		p = pyaudio.PyAudio()

		# open stream
		stream = p.open(format =
	         		p.get_format_from_width(wf.getsampwidth()),
        		        channels = wf.getnchannels(),
		                rate = wf.getframerate(),
		                output = True)

		# read data
		data = wf.readframes(chunk)

		# play stream
		while data != '':
			stream.write(data)
			data = wf.readframes(chunk)

		stream.stop_stream()
		stream.close()

		p.terminate()

	def play_tkSnack(self, mediaFile):
		''' Use tkSnack backend to play the .wav.'''

		stream = tkSnack.Sound()
		stream.read(mediaFile)
		stream.play()

	def play_pyglet(self, mediaFile):
		''' Use pyglet backend to play the .wav.'''

		stream = pyglet.resource.media(mediaFile)
		stream.play()
		pyglet.clock.schedule_once(pyglet.app.exit(), stream.duration)
		pyglet.app.run()

	def play_media(self, mediaFile):
		''' In absence of audio playback frameworks, just use an OS-based console media player.'''

		# https://github.com/mdoege/NewsFeed/blob/master/newsfeed.py#L49 Thanks for the code, Martin!
		media_player = os.getenv("MEDIA_PLAYER")
		if not media_player:
			if 'freebsd' in sys.platform or 'linux' in sys.platform:
				media_player = "noatun"	# A nice choice under KDE
			elif 'darwin' in sys.platform:
				media_player = "open"	# Suggested for Mac OS X
			else:
				media_player = ""	# Empty string -> Enclosures get opened
							# in default web browser.
		if media_player:
			command = '%s "%s"' % (media_player, mediaFile)
			os.system(command)
