#!/usr/bin/env python

"""
Python Command Line Musical Interpreter for PySynth.
Pranav Ravichandran (me@onloop.net)
"""

import play_wav
import pysynth, pysynth_b, pysynth_s
import wave
import sys
import os
import string

#Type 'help' to access.
helpContent = "------------------------------\nPySynth musical note interpreter.\nUsage: <Duration><Note> <Duration2><Note2> .... <DurationN><NoteN>\nOptional arguments:\n\t--bpm=Beats per minute [Default:120]\n\t--repeat=Number of bars [Default:1]\n\t--sound=Instrument [a = Flute/Organ, b = piano, s = plucked string, Default = a]\n\t--save=filename (Filename to save the file to. Appends .wav to filename)\nSamples:\n8g 8g 8g 2eb 8r 8f 8f 8f 1d --sound=a\n4e4 4e4 4f4 4g4 4g4 4f4 4e4 4d4 4c4 4c4 4d4 4e4 4e4 4d4 2d4 4e4 4e4 4f4 4g4 4g4 4f4 4e4 4d4 4c4 4c4 4d4 4e4 4d4 4c4 2c4 --bpm=200 --repeat=1 --sound=s --save=Ode_to_Joy\nCommands: 'exit' and 'help'\n------------------------------"

usageHelp = "Notes are 'a' through 'g' of course,\noptionally with '#' or 'b' appended for sharps or flats.\nFinally the octave number (defaults to octave 4 if not given).\nAn asterisk at the end makes the note a little louder (useful for the beat).\n'r' is a rest.\n\nNote value is a number:\n1=Whole Note; 2=Half Note; 4=Quarter Note, etc.\nDotted notes can be written in two ways:\n1.33 = -2 = dotted half\n2.66 = -4 = dotted quarter\n5.33 = -8 = dotted eighth\n--------------------------------"

warningStr = "Improper Syntax - Type 'help' to see usage."

invalidCmd = "Command does not exist."

invalidOption = "Invalid Option."

class mEnv:
	cliInput = ''
	synthParam = []
	bpmVal = 0
	repeatVal = 0
	inputEntered = False
	instrument = ''
	outFile = ''
	trashFile = True
	def __init__(self):
		''' Constructor class. '''

		# Get the user input.
		cliInput = raw_input(">>> ")

		self.parse(cliInput)

		# Different cases of input, when optional argument 'sound' is given.
		if self.instrument == 'a' or self.instrument == '':
			self.synthSounds(pysynth, self.outFile)
		elif self.instrument == 'b':
			self.synthSounds(pysynth_b, self.outFile)
		elif self.instrument == 's':
			self.synthSounds(pysynth_s, self.outFile)
		else:
			print invalidOption
			mEnv()

	def parse(self, cliInput):
		''' Parse command line input.'''

		# 'exit' command.
		if cliInput == 'exit':
			sys.exit()
		# 'help' command.
		if cliInput == 'help':
			print '\n' + helpContent + '\n' + usageHelp + '\n'
			mEnv()

		# List with whitespace as delimiter.
		cliInput = cliInput.split()
		self.synthParam = []

		for comp in cliInput:
			# Optional arguments.
			if comp.startswith('--'):
				comp = comp.strip('-')
				comp = comp.split('=')
				if comp[0] == 'bpm':
					try:
						self.bpmVal = int(comp[1])
					except IndexError:
						print warningStr
						mEnv()
				elif comp[0] == 'repeat':
					try:
						self.repeatVal = int(comp[1])
					except IndexError:
						print warningStr
						mEnv()
				elif comp[0] == 'sound':
					try:
						self.instrument = str(comp[1])
					except IndexError:
						print warningStr
						mEnv()
				elif comp[0] == 'save':
					try:
						self.outFile = str(comp[1]) + '.wav'
						self.trashFile = False
					except IndexError:
						print warningStr
						mEnv()

				continue

			# Notes and beats.
			i = 0
			for alphanum in comp:
				if alphanum.isalpha():
					try:
						self.synthParam.append((comp[i:], int(comp[:i])))
					except ValueError:
						print invalidCmd
						mEnv()

					break
				i += 1

	def play(self, outFile):
		''' Open the .wav file and play it.'''

		if outFile == '':
			outFile = 'temp.wav'

		a = play_wav.Sound()
		a.playFile(outFile)

	def removeFile(self, outFile):
		''' Delete the .wav file.'''

		if outFile == '':
			outFile = 'temp.wav'

		if self.trashFile:
			os.remove(outFile)

	def synthSounds(self, renderSound, outFile):
		''' Render sound with pysynth_a, pysynth_b or pysynth_s based on user preference.'''

		if outFile == '':
			outFile = 'temp.wav'

		try:
			# Different cases of input, when optional arguments 'bpm' and 'repeat' are given.
			if self.bpmVal and self.repeatVal:
				renderSound.make_wav(self.synthParam, fn = outFile, silent = True, bpm = self.bpmVal, repeat = self.repeatVal)
			elif self.bpmVal:
				renderSound.make_wav(self.synthParam, fn = outFile, silent = True, bpm = self.bpmVal)
			elif self.repeatVal:
				renderSound.make_wav(self.synthParam, fn = outFile, silent = True, repeat = self.repeatVal)
			else:
				renderSound.make_wav(self.synthParam, fn = outFile, silent = True)
		except KeyError:
			print warningStr
			mEnv()



if __name__ == "__main__":
	# Print introductory help content.
	print helpContent

	# Interpreter loop.
	while True:
		a = mEnv()
		try:
			a.play(a.outFile)
		except:
			a.trashFile = False
			if a.outFile == '':
				a.outFile = 'temp.wav'
			print 'Could not play file. Saved to ' + a.outFile
		a.removeFile(a.outFile)
