#!/usr/bin/python

"""
Chord Calculator
Version 0.3
Copyright (c) 28 Dec 2008, Gek S. Low

Modified to operate under Pythonista iOS ui environment
Copyright (c) August 19th, 2014 Steven K. Pollack
Free for personal use. All other rights reserved.

USE AT YOUR OWN RISK!
This software is provided AS IS and does not make any claim that it actually works,
  or that it will not cause your computer to self-destruct or eat up your homework.

Note that some calculated chords may be playable only by aliens with 10 tentacles.
Please use your common sense. The author will not be responsible for any injuries
from attempts at impossible fingerings.

The author reserves the right to change the behavior of this software without prior notice.

View objects:
-------------
tableview_roots     - root tone of chord
tableview_type      - chord type
tableview_inst_tune - instrument/tuning selector
tableview_filters   - filters selection
tableview_find      - display and interogate found chords
tableview_scale     - display vaious scales
view_neck           - drawing of neck/fingering
button_up           - previous chord shape/position
button_down         - next chord shape/position
button_arp          - play arpeggio
button_chord        - play chord
button_tuning       - play the open strings
button_cc_modew     - change mode (show fingering for a chord, or calculate chords from a fingering
                                   of display scales)
button_find         - display ther calculated fingering
slider_volume       - set play volume
slider_arp          - set arpegio and scale playback speed
lbl_fullchord       - displays the notes in the display chord (full chord, no filters)
lbl_definition      - displays the scale tones in a the full chord
                    - display relative major of greek mode
btn_sharpFlat       - forces shaprs for flats for non-standard keys (not in the circle of fifths)
"""

import sys, os.path, re, ui, console, sound, time, math
from PIL import Image
from copy import deepcopy
from chordcalc_constants import *
from debugStream import debugStream

class CurrentState():
	'status of shared state date for the gui'
	def __init__(self):
		self.states = {'instrument' : None,
		               'filters'    : None,
		               'scale'      : None,
		               'chord'      : None,
		               'root'       : None,
		               'fretboard'  : None,
		               'mode'       : 'C'
		               }  #scale/chord mode 
	
	def __getitem__(self,key):
		return self.states.get(key, None)
	
	def __setitem__(self,key,value):
		self.states[key] = value


def rotate(list,index):
	''' take the input list and rotate it by indicated number of positions
			positive index move items form left side of list to right
			so list[0] become list[-1]
			negative is vice versa'''
	return list[index %len(list):] + list[:index % len(list)] if index else list

def instrument_type(): # return the type of instrument based on current selected 
	text = currentState['instrument']['title']
	for instrument in 'guitar mandolin ukulele'.split()
		if re.match('^{}'.format(instrument), text , flags=re.I):
			return instrument
	return 'generic'
			
def uniqify(sequence, idfun=None):
	''' return a unique, order preserved version in input list'''
	if not idfun:
		def idfun(x): return x
	seen = {}
	result = []
	for item in sequence:
		marker = idfun(item)
		if marker in seen.keys(): 
			continue
		seen[marker] = 1
		result.append(item)
	return result
	
def fingeringToString(list):
	''' turn fingering to a text string for hashing'''
	hashcodes = 'abcdefghijklmnopqrstuvwxyz-'
	return ''.join([hashcodes[item] for item in list])

def calc_fingerings():
	'''calculate the fingerings and fretboard positions for the desired chord'''
	global currentState 
	try:
		key = currentState['root']['noteValue']
		note = currentState['root']['title']  # since "C" has a note value of zero, use note title as indicator
		chordtype = currentState['chord']['fingering']	
		tuning = currentState['instrument']['notes']
		instrument = currentState['instrument']
		filters = currentState['filters']
		span = currentState['instrument']['span']
	except:
		return
		
	if note and chordtype and tuning:
		fingerPositions = []	
		fingerings = []
		result = []
		console.show_activity()
		for position in range(0,fretboard.numFrets,span):
			fingeringThisPosition = findFingerings(key, chordtype, tuning, position, span)
			fingerings = fingerings + fingeringThisPosition
		fingerings = uniqify(fingerings,idfun=(lambda x: tuple(x)))
		if fingerings:
			for fingering in fingerings:
				fingerMarker = fretboard.fingeringDrawPositions(key,chordtype,tuning,fingering)
				fingerPositions.append(fingerMarker)
			for fingering,drawposition in zip(fingerings,fingerPositions):
				chordTones = []
				for entry in drawposition:
					chordTones.append(entry[2])
				result.append((drawposition,chordTones,fingering))
			if filters:
				result = apply_filters(filters, result)
				if result:
					result = uniqify(result,idfun=(lambda x: tuple(x[2])))
		console.hide_activity()
	return result
			
def calc_two_octave_scale(startingStringFret):
	''' given a starting (string,scaletoneIndex) calculate a two octave scale across the strings
	    returns a 2D tupple of strings and frets'''
	global currentState
	try:
		key = currentState['root']['noteValue']
		scaleintervals = currentState['scale']['scaleintervals']
		tuning = currentState['instrument']['notes']
		instrument = currentState['instrument']
		fretboard = currentState['fretboard']
	except:
		return None
		
	intervals = [0]
	for letter in scaleintervals:
		if letter == 'S':
			intervals.append(1)
		elif letter == 'T':
			intervals.append(2)
		else:
			intervals.append((int(letter)))
			
	nextNote = key
	notesInScale = [nextNote]
	for interval in intervals[1:]:
		nextNote += interval
		notesInScale.append(nextNote % 12)
		
	scale_notes = fretboard.scale_notes
	notesOnStrings = []
	fretsOnStrings = [] 
	
	for string in scale_notes:
		notes = [x[1] for x in string]
		notesOnStrings.append(notes)
		frets = [x[0] for x in string]
		fretsOnStrings.append(frets)
	
	numNotes = 2*len(scaleintervals) + 1
	numStrings = len(tuning)
	thisString,thisStringFret = startingStringFret
	thisIndex = fretsOnStrings[thisString].index(thisStringFret)
	scaleNotes = [startingStringFret]
	nextStringNote = notesOnStrings[1][0]
	# always look to see if next note is on next string
	for string in range(thisString,numStrings): # look at next string always
		for thisI in range(thisIndex+1,len(fretsOnStrings[0])):
			thisStringNote = notesOnStrings[string][thisI]
			if string == numStrings - 1: # rightmost string, so force to never check
				nextStringNote = 100 # current tone always "smaller"
			else:
				nextStringNote =  notesOnStrings[string+1][0]
			if nextStringNote != thisStringNote: # continue on this string
				scaleNotes.append((string,fretsOnStrings[string][thisI]))
				if len(scaleNotes) == numNotes:
					return scaleNotes
			else:
				scaleNotes.append((string+1,fretsOnStrings[string+1][0]))
				if len(scaleNotes) == numNotes: 
					return scaleNotes
				thisIndex = 0
				nextIndex = 0
				break
	return scaleNotes

def calc_chord_scale():
	global currentState
	try:
		key = currentState['root']['noteValue']
		chord = currentState['chord']['fingering']
		tuning = currentState['instrument']['notes']
		instrument = currentState['instrument']
		fretboard = currentState['fretboard']
	except:
		return []
					
	# calculate notes in the current key
	chordNotes = [(x+key) % 12 for x in chord]
	scale = []
	for string in tuning:
		thisString = []
		for fret in range(fretboard.numFrets+1): # zero is the open string
			tone = (string + fret) %12
			if tone in chordNotes:
				thisString.append((fret-1,(tone-key)%12))
		scale.append(thisString)

	return scale
	
	
	
	
		
def calc_scale_notes():
	''' calculate the scale notes for the curent key, instrument and scale type'''
	global currentState
	try:
		key = currentState['root']['noteValue']
		scaleintervals = currentState['scale']['scaleintervals']
		tuning = currentState['instrument']['notes']
		instrument = currentState['instrument']
	except:
		return
	
	# format of the returned data is [[[fret, scalenote, scaletone, octave],.....numer on string
	#                                                                         ] length = numStrings
	# first unpack the scale spacing from the string
	intervals = [0]
	for letter in scaleintervals:
		if letter == 'S':
			intervals.append(1)
		elif letter == 'T':
			intervals.append(2)
		else:
			intervals.append((int(letter)))
			
	nextNote = key
	notes = [nextNote]
	for interval in intervals[1:]:
		nextNote += interval
		notes.append(nextNote % 12)
		
	scaleNotes= []
	for string in tuning:
		thisString = []  
		for fret in range(fretboard.numFrets+1):
			note = (fret + string) % 12
			if note in notes:
				thisString.append((fret,note))
		scaleNotes.append(thisString)		
	return scaleNotes	
		
		
def apply_filters(filters,fingerings):
	''' for the current fingerings and filters, return only those chords that apply'''
	filter_constraint = {'FULL_CHORD':("R b3 3 #5 5".split(),3)}	
	instrumentType = instrument_type()
	if not filters:
		return fingerings
	filtered = []
	temp_fingerings = fingerings
	if 'FULL_CHORD' in filters:   # must have at least R,3 and 5 triad
		for fingering in temp_fingerings:	
			notes,numNotes = filter_constraint['FULL_CHORD']		
			if len(set(fingering[1]).intersection(notes)) == numNotes:
				filtered.append(fingering)
		temp_fingerings = filtered
		
	filtered = []
	if 'NO_DEAD' in filters : #remove all with dead notes
		for fingering in temp_fingerings:
			if 'X' not in fingering[1]:
				filtered.append(fingering)
		temp_fingerings = filtered
		
	filtered = []
	if 'NO_OPEN' in filters:
		for fingering in temp_fingerings:
			open_check = []
			for string in fingering[0]:
				open_check.append(string[3])
			if 'O' not in open_check:
				filtered.append(fingering)
		temp_fingerings = filtered 
		
	filtered = []
	if 'HIGH_4' in filters:
		for fingering in temp_fingerings:
			validChord = True
			for i,string in enumerate(fingering[0]):
				if i in [0,1]:
					if string[3] != 'X':
						validChord = False
						break
				else:
					if string[3] == 'X':
						validChord = False
						break
			if validChord:
				filtered.append(fingering)
		temp_fingerings = filtered
		
	filtered = []
	if 'LOW_4' in filters:
		for fingering in temp_fingerings:
			validChord = True
			for i,string in enumerate(fingering[0]):
				if i in [4,5]:
					if string[3] != 'X':
						validChord = False
						break
				else:
					if string[3] == 'X':
						validChord = False
						break
			if validChord:
				filtered.append(fingering)
		temp_fingerings = filtered
								
	filtered = []
	if 'HIGH_3' in filters: #for mandolin, allow for root or 5th to be abandoned
		for fingering in temp_fingerings:
			validChord = True
			for i,string in enumerate(fingering[0]):
				if i == 0:
					if string[3] != 'X':
						if fingering[1][i] in ['R','#5', '5']:
							fingering[1][i] = 'X'
							fingering[0][i] = (fretboard.nutPosition[i][0],fretboard.nutPosition[i][1],'X','X')
							break
						validChord = False
						break
				else:
					if string[3] == 'X':
						validChord = False
						break
			if validChord:
				filtered.append(fingering)
		temp_fingerings = filtered
										
	filtered = []
	if 'LOW_3' in filters: 
		for fingering in temp_fingerings:
			validChord = True
			for i,string in enumerate(fingering[0]):
				if i == 3:
					if string[3] != 'X':
						if fingering[1][i] in ['R','#5','5'] :# for mandolin, allow for root or 5th to be abandoned
							fingering[1][i] = 'X'
							fingering[0][i] = (fretboard.nutPosition[i][0],fretboard.nutPosition[i][1],'X','X')
							break
						validChord = False
						break
				else:
					if string[3] == 'X': 
						validChord = False
						break
			if validChord:
				filtered.append(fingering)
		temp_fingerings = filtered
		
	filtered = []
	if 'DOUBLE_STOPS' in filters and instrumentType == 'mandolin': # create adjacent string double stops for the chords
		numStrings = len(fingerings[0][1])
		for fingering in temp_fingerings:			
			for i,string in enumerate(fingering[1]):
				if i+1 == numStrings: 
					break
				else:
					nextString = fingering[1][i+1]
				if string == 'X' or nextString == 'X': continue
				if string != nextString: #rebuild the fingering as a double stop for this pair
					field1 = []
					field2 = []
					field3 = []
					j = 0
					while j < numStrings:
						if j < i or j > i+1:
							field1.append((fretboard.nutPosition[j][0],fretboard.nutPosition[j][1],'X','X'))
							field2.append('X')
							field3.append(-1)
							j += 1
						else:
							for index in [j,j+1]:
								field1.append(fingering[0][index])
								field2.append(fingering[1][index])
								field3.append(fingering[2][index])
							j += 2
					entry = (field1,field2,field3)
					filtered.append(entry)
		temp_fingerings = filtered				
							
	filtered = []
	if 'NO_WIDOW' in filters: #remove isolated dead string (but not first or last)
		numStrings = len(fingerings[0][1])
		for fingering in temp_fingerings:
			validChord = True
			for i,string in enumerate(fingering[1]):
				if (i == 0 or i == numStrings-1) and string == 'X' : #outside strings
					continue
				if string == 'X':
					validChord = False
					break
			if validChord:
				filtered.append(fingering)
		temp_fingerings = filtered				
	unique =  uniqify(temp_fingerings,idfun=(lambda x: fingeringToString(x[2])))	
	return unique
	
	
def tuningLabel(notes):
	'''return the notes for the current tuning'''
	global NOTE_NAMES
	note_string = ''
	for note in notes:
		note_range,base_note = divmod(note,12)
		note_char = re.split('/', NOTE_NAMES[base_note])[0]
		if not note_range:
			note_string += note_char
		elif note_range == 1:
			note_string += note_char.lower()
		elif note_range == 2:
			note_string += note_char.lower() + "'"
		note_string += ' '
	return note_string.strip()
	
def getScaleNotes(key, chordtype, tuning, fingering):
	'''Given a fingering, gets the scale note relative to the key'''
	scalenotes = []
	for i, v in enumerate(fingering):
		if v == -1:
			scalenotes.append('X')
		else:
			fingerednote = (tuning[i] + fingering[i]) % 12
			for chordrelnote in chordtype:
				chordnote = (key + chordrelnote) % 12
				if fingerednote == chordnote:
					scalenotes.append(SCALENOTES[chordrelnote])
	return scalenotes


# Finds the chord fingerings for a given tuning (number of strings implied)
# Pos is the "barre" position, span is how many frets to cover
# Returns a list of fingerings

def findFingerings(key, chordtype, tuning, pos, span):
	# Get valid frets on the strings
	validfrets = findValidFrets(key, chordtype, tuning, pos, span)

	# Find all candidates
	candidates = findCandidates(validfrets)


	# Filter out the invalid candidates
	candidates = filterCandidates(key, chordtype, tuning, candidates)

	# Filter out "impossible" fingerings?
	# To be implemented...

	# Perhaps also some sorting options?

	return candidates

# For a given list of starting frets and span, find the ones that are in the chord for that tuning
# Returns a list of valid frets for each string
# Open strings are included if valid

def findValidFrets(key, chordtype, tuning, pos, span):
	if not tuning:
		return None
	strings = []
	for string in tuning:
		frets = []
		searchrange = range(pos, pos+span+1)
		if pos != 0: # include open strings is not at pos 0
			searchrange = [0] + searchrange
		for fret in searchrange:
			for chordrelnote in chordtype:
				note = (string + fret) % 12
				chordnote = (key + chordrelnote) % 12
				if note == chordnote:
					frets.append(fret)
		strings.append(frets) 
	return strings



# Finds all candidate fingerings, given all valid frets
# Includes strings that should not be played
# Note that this is just a permutation function and is independent of keys, tunings or chords



def findCandidates(validfrets):
	# Set up the counter which will track the permutations
	max_counter = []
	counter = []
	candidatefrets = []
	if not validfrets:
		return None
	for string in validfrets:
		# Include the possibility of not playing the string
		# Current approach prioritises open and fretted strings over unplayed strings
		candidatefrets.append(string + [-1])
		max_counter.append(len(string))
		counter.append(0)
	l = len(counter)-1

	# Number of possible permutations
	numperm = 1
	for c in max_counter:
		numperm *= c+1

	candidates = []
	# Permute
	for perm in range(numperm):
		# get the candidate
		candidate = []
		for string, fret in enumerate(counter):

			candidate.append(candidatefrets[string][fret])

		# increment counter, starting from highest index string
		for i, v in enumerate(counter):
			if counter[l-i] < max_counter[l-i]:
				counter[l-i] += 1
				break
			else:
				counter[l-i] = 0
	
		candidates += [candidate]
	return candidates



# Tests whether a fingering is valid
# Should allow various possibilities - full chord, no 5th, no 3rd, no root, etc

def isValidChord(key, chordtype, tuning, candidate):
	filters = currentState['filters']
	if not filters:
		filters = []
		
	result = True

	# which chord notes are present?
	present = {}
	for chordrelnote in chordtype:
		# assume chord notes are not present
		present[chordrelnote] = False
		chordnote = (key + chordrelnote) %12
		for i, v in enumerate(candidate):
			# ignore unplayed strings
			if candidate[i] != -1:
				note = (tuning[i] + candidate[i]) % 12
				if chordnote == note:
					present[chordrelnote] = True
					break


	# do we accept this fingering? depends on the option
	for note in present.keys():
		if present[note] == False:
			if 'FULL_CHORD' in filters:
				result = False
				break
			if 'NO3RD_OK' in filters:
				if note == 4 or note == 3:
					continue
			if 'NO5TH_OK' in filters:
				if note == 7:
					continue
			if 'NOROOT_OK' in filters:
				if note == 0:
					continue
		result = result & present[note]
	return result


# Tests if a given note is in the chord
# Not used here

def isInChord(key, chordtype, note):
	for chordrelnote in chordtype:
		chordnote = (key + chordrelnote) % 12
		if note == chordnote:
			return True
	return False

# Filter out the invalid chords from the list of candidates
# Criteria for invalid chords may vary
# Returns the list of valid chords

def filterCandidates(key, chordtype, tuning, candidates):
	if not candidates:
		return None
	newlist = []
	for candidate in candidates:
		if isValidChord(key, chordtype, tuning, candidate):
			newlist += [candidate]
	return newlist

# Given a fingering, gets the scale note relative to the key
def getScaleNotes(key, chordtype, tuning, fingering):
	scalenotes = []
	for i, v in enumerate(fingering):
		if v == -1:
			scalenotes.append('X')
		else:
			fingerednote = (tuning[i] + fingering[i]) % 12
			for chordrelnote in chordtype:
				chordnote = (key + chordrelnote) % 12
				if fingerednote == chordnote:
					scalenotes.append(SCALENOTES[chordrelnote])
	return scalenotes
	
def setChordSpelling():
	''' calculate and display the current Chord Spelling'''
	global currentState
	
	try:
		chordTones = currentState['chord']['fingering']
		key = currentState['root']['noteValue']
		keyName = currentState['root']['title']
	except:
		return
	outString = ''
	defString = ''
	for tone in chordTones:
		outChar = NOTE_NAMES[(tone + key) % 12].split('/')
		if len(outChar) == 1:
			outChecked = outChar[0]
		else:
			try:
				sf = CIRCLE_OF_FIFTHS[keyName]
			except:
				sf = 1
			if sf > 0:
				outChecked = outChar[0]
			else:
				outChecked = outChar[1]
		outString += outChecked + ' '
		defString += SCALENOTES[tone] + ' '
	mainView['lbl_fullchord'].hidden = False
	mainView['lbl_fullchord'].text = outString.strip()
	mainView['lbl_definition'].hidden = False
	mainView['lbl_definition'].text = defString.strip()

def relativeMajorDisplay():
	''' display the relative major for a greek mode'''
	global currentState
	try:
		key = currentState['root']['noteValue']
		scale = currentState['scale']['title']
	except:
		return
	
	if scale in TRUE_ROOT.keys():
		text = "relative to {}".format(NOTE_NAMES[(key-TRUE_ROOT[scale])%12])
		mainView['lbl_definition'].text = text		
		mainView['lbl_definition'].hidden = False
	else:
		mainView['lbl_definition'].hidden = True

	
# Fretboard Class

class Fretboard(ui.View): # display fingerboard and fingering of current chord/inversion/file
#note that this is instanciated by the load process.  
	global currentState,middle_label
	def did_load(self):
		self.fbWidth = int(self.bounds[2])
		self.fbHeight = int(self.bounds[3])
		self.nutOffset = 20	
		self.numFrets = 14
		self.offsetFactor = 0.1		
		self.scale = 2*(self.fbHeight - self.nutOffset) 
		self.markerRadius = 10
		self.fingerRadius = 15
		self.image = ''
		self.instrument = currentState['instrument']
		self.chord = currentState['chord']
		self.root = currentState['root']
		self.ChordPositions = [] #set of fingerings for current chord/key/instrument/filter setting
		self.currentPosition = 0 # one currently being displayed
		self.scale_notes = []
		self.fingerings = []
		self.loaded = True
		self.snd = self.set_needs_display
		self.chord_num = None
		self.num_chords = None
		self.nutPositions = []
		self.stringX = []
		self.fretY = []
		self.PrevFretY = 0
		self.touched = {} # a dictionary of touched fret/string tuples as keys, note value
		self.cc_mode = 'C' # versus 'identify6'
		self.scale_display_mode = 'degree'
		self.showChordScale = False
		self.ChordScaleFrets = []
		self.arpMin = 0.05
		self.arpMax = 0.5
		self.arpSpeed = (self.arpMax + self.arpMin)/2.0
		self.sharpFlatState = '#'
		
	def sharpFlat(self,sender): #toggle
		self.sharpFlatState = 'b' if self.sharpFlatState == '#' else '#'
		self.set_needs_display()
		
					
	def set_tuning(self,instrument): # store current value of tuning parameters
		self.tuning = instrument.get_tuning()
		
	def set_chord(self,chordlist): # store current value of chord
		self.chord = chordlist.get_chord()
		
	def set_root(self,root):
		self.root = keylist.get_key() # get value of key
		
	def set_chordnum(self,chord_num,num_chords):
		self.chord_num = chord_num
		self.num_chords = num_chords
		
	def set_fingerings(self,fingerings):
		self.ChordPositions = fingerings
		self.currentPosition = 0
	
	def set_scale_notes(self, scale_notes):
		'''save scale notes'''
		self.scale_notes = scale_notes

	def set_chord_num(self,number):
		self.currentPosition = number
		
	def get_chord_num(self):
		return self.currentPosition
		
	def get_num_chords(self):
		return len(self.ChordPositions)

	def fretDistance(self,scalelength, fretnumber):
		import math
		return int(scalelength - (scalelength/math.pow(2,(fretnumber/float(self.numFrets)))))

	
	def fretboardYPos(self,fret):
		return int((self.fretDistance(self.scale,fret) + self.fretDistance(self.scale,fret-1))/2.0)	
		
	def stringSpacing(self):
		numStrings = len(currentState['instrument']['notes'])
		offset = int(self.offsetFactor*self.fbWidth)
		return (numStrings,offset,int((self.fbWidth-2*offset)/float(numStrings-1)))
		
	def PathCenteredCircle(self,x,y,r):
		""" return a path for a filled centered circle """
		return ui.Path.oval(x -r, y -r, 2*r,2*r)		

	def PathCenteredSquare(self,x,y,r):
		""" return a path for a filled centered circle """
		return ui.Path.rect(x -r, y -r, 2*r,2*r)		
		
	def draw(self):
		self.tuning = currentState['instrument']
		self.root = currentState['root']
		self.chord = currentState['chord']
		try:
			self.key = currentState['root']['noteValue']
			self.keySignature = currentState['root']['title']
		except:
			pass
		
		try:
			self.scaleType = currentState['scale']['title']
		except:
			pass
		
		if self.tuning:
			fretboard = ui.Path.rect(0, 0, self.fbWidth, self.fbHeight)
			ui.set_color('#4C4722')
			fretboard.fill()
		
			nut = ui.Path.rect(0,0,self.fbWidth,self.nutOffset)
			ui.set_color('#ECF8D7')
			nut.fill()
		
			ui.set_color('white')
			fretSpace = int((self.fbHeight - 2*self.nutOffset)/(self.numFrets))

			self.fretY = [0]
			for index in range(self.numFrets):
				yFret = self.fretDistance(self.scale,index+1)
				self.fretY.append(yFret)
				self.PrevFretY = yFret
				fret = ui.Path()
				fret.line_width = 3
				fret.move_to(0,yFret)
				fret.line_to(self.fbWidth,yFret)
				fret.stroke()

			
			markers = [3,5,7]
			if instrument_type() == 'ukulele':
				markers.append(10)
			else:
				markers.append(9)
			for index in markers:		
				markeryPos = self.fretboardYPos(index)
				marker= self.PathCenteredCircle(int(0.5*self.fbWidth), markeryPos, self.markerRadius)
				marker.fill()
			

			markery12 = markeryPos = self.fretboardYPos(12)
			for xfraction in [0.25,0.75]:
				marker= self.PathCenteredCircle(int(xfraction*self.fbWidth), markery12, self.markerRadius)
				marker.fill()
		
		#assume width is 1.5" and strings are 1/8" from edge
			numStrings,offset,ss = self.stringSpacing()
			self.nutPosition = []
			ui.set_color('grey')
			self.stringX = []
			for index in range(numStrings):
				xString = offset + index*ss
				self.stringX.append(xString)
				string = ui.Path()
				string.line_width = 3
				string.move_to(xString,0)
				string.line_to(xString,self.fbHeight)
				string.stroke()
				self.nutPosition.append((xString,int(0.5* self.nutOffset)))

					
			if self.ChordPositions and self.cc_mode == 'C': 
				# if there are some, draw current fingering or chord tone frets
				if not self.showChordScale:
					self.num_chords.text = "{}".format(len(self.ChordPositions))
					self.chord_num.text = "{}".format(self.currentPosition+1)
					middle_field.text = 'of'

				 	fingering,chordTones,fretPositions = self.ChordPositions[self.currentPosition]
				 	ui.set_color('red')
				 	for string in fingering:
						x,y,chordtone,nutmarker = string
	
						if not nutmarker:
							ui.set_color('red')
							marker= self.PathCenteredCircle(x,y,self.fingerRadius)
							marker.fill()
							ui.set_color('white')
							size = ui.measure_string(chordtone,font=('AmericanTypewriter-Bold',
							                                         22),alignment=ui.ALIGN_CENTER)
							ui.draw_string(chordtone,(int(x-0.5*size[0]),int(y-0.5*size[1]),0,0),
							               font=('AmericanTypewriter-Bold',22),alignment=ui.ALIGN_CENTER)
				 		else:
				 			size = ui.measure_string(chordtone,font=('AmericanTypewriter-Bold',26),alignment=ui.ALIGN_CENTER)
							ui.draw_string(chordtone,(int(x-0.5*size[0]),int(y-0.5*size[1]),0,0),
							               font=('AmericanTypewriter-Bold',26),alignment=ui.ALIGN_CENTER,color='black')
							size = ui.measure_string(chordtone,font=('AmericanTypewriter-Bold',22),alignment=ui.ALIGN_CENTER)
							ui.draw_string(chordtone,(int(x-0.5*size[0]),int(y-0.5*size[1]),0,0),
							               font=('AmericanTypewriter-Bold',22),alignment=ui.ALIGN_CENTER,color='red')	
				elif self.ChordScaleFrets:
					for i,string in enumerate(self.ChordScaleFrets):
						for fret,note in string:
							chordtone = SCALENOTES[note]
							x = self.stringX[i]
							if fret != -1:
								y = self.fretboardYPos(fret+1)
							else:
								y = self.nutPosition[0][1]
							ui.set_color('red')
							if note == 0:
								marker= self.PathCenteredSquare(x,y,self.fingerRadius)
							else:
								marker= self.PathCenteredCircle(x,y,self.fingerRadius)
							marker.fill()
							ui.set_color('white')
							size = ui.measure_string(chordtone,font=('AmericanTypewriter-Bold',
							                                         22),alignment=ui.ALIGN_CENTER)
							ui.draw_string(chordtone,(int(x-0.5*size[0]),int(y-0.5*size[1]),0,0),
							               font=('AmericanTypewriter-Bold',22),alignment=ui.ALIGN_CENTER)
						               
			elif self.root and self.chord and self.cc_mode == 'C':
				sound.play_effect('Woosh_1')
				self.chord_num.text = "Try dropping"
				middle_field.text = "root, 3rd" 
				self.num_chords.text = "or 5th"			

			
			elif self.cc_mode == 'I':# identify mode
				for key in self.touched.keys():
					values = self.touched[key]
					x = self.stringX[values[2]]
					y = self.fretboardYPos(values[3])
					if values[3]:
						ui.set_color('red')
						marker= self.PathCenteredCircle(x,y,self.fingerRadius)
						marker.fill()
					else:
						y = self.nutPosition[0][1]
						size = ui.measure_string('O',font=('AmericanTypewriter-Bold',26),alignment=ui.ALIGN_CENTER)
						ui.draw_string('O',(int(x-0.5*size[0]),int(y-0.5*size[1]),0,0),
						               font=('AmericanTypewriter-Bold',26),alignment=ui.ALIGN_CENTER,color='black')
						size = ui.measure_string('O',font=('AmericanTypewriter-Bold',22),alignment=ui.ALIGN_CENTER)
						ui.draw_string('O',(int(x-0.5*size[0]),int(y-0.5*size[1]),0,0),
						               font=('AmericanTypewriter-Bold',22),alignment=ui.ALIGN_CENTER,color='red')	
				               
			elif self.cc_mode == 'S': # display scale notes
				ui.set_color('red')
				if self.scale_notes:
				 	for i,string in enumerate(self.scale_notes):
						for fret,note in string:
							x = self.stringX[i]
							if fret == 1:
								y = self.fretboardYPos(fret) + 12
							elif fret:
								y = self.fretboardYPos(fret)
							else:
								y = self.nutPosition[0][1] + self.fingerRadius*0.3
							ui.set_color('red')
							if note == self.key:
								marker= self.PathCenteredSquare(x,y,self.fingerRadius)
							else:
								marker= self.PathCenteredCircle(x,y,self.fingerRadius)
							marker.fill()
							if self.scale_display_mode == 'degree':
								outchar = SCALENOTES[(note - self.key) % 12]
							else:
								outchar = self.noteName(note)
							ui.set_color('white')
							size = ui.measure_string(outchar,font=('AmericanTypewriter-Bold',
						                                         22),alignment=ui.ALIGN_CENTER)
							ui.draw_string(outchar,(int(x-0.5*size[0]),int(y-0.5*size[1]),0,0),
						               font=('AmericanTypewriter-Bold',22),alignment=ui.ALIGN_CENTER)
				if self.scaleFrets: # mark the scale notes
					ui.set_color('yellow')
					self.fifthPresent = False # prevent 5 and 5# from both being highlighted chord tones.
					for string,fret in self.scaleFrets:
						x = self.stringX[string]				
						if fret == 1:
							y = self.fretboardYPos(fret) + 12
						elif fret:
							y = self.fretboardYPos(fret)
						else:
							y = self.nutPosition[0][1] + self.fingerRadius*0.3
						self.chordtone_color(string,fret)
						marker= self.PathCenteredCircle(x,y,self.fingerRadius + 10)
						marker.line_width = 3
						marker.stroke()
			else:
				pass

	def chordtone_color(self,string,fret):
		# convert from string/fret to note
		key = fretboard.key
		thisString = self.scale_notes[string]
		for thisFret,thisNote in thisString:
			color = 'red'
			if fret == thisFret:
				scaleTone = (thisNote - key) % 12
				if scaleTone == 0:
					color = 'green'
					break
				elif scaleTone in (3,4): # b3 and 3
					color = 'yellow'
					break
				elif scaleTone in (7,8): # 5 and 5#
					if scaleTone == 7:
						color = 'white'
						self.fifthPresent = True
						break
					elif scaleTone == 8 and not self.fifthPresent:
						color = 'white'
						break
				elif scaleTone in (10,11):
					color = 'orange'
					break
		ui.set_color(color)
		return

	def noteName(self,note):
		'''return the name of the note with proper use of sharps or flats'''
		key = self.key
		keySig = self.keySignature
		if keySig in CIRCLE_OF_FIFTHS.keys():
			sf = CIRCLE_OF_FIFTHS[keySig]
		else:
			print 'not in cof'
			sf = 1 if self.sharpFlatState == '#' else -1 # use preference
			print "sf = ",sf
		if self.scaleType in TRUE_ROOT.keys():
			origKeySig = keySig	
			key = (key - TRUE_ROOT[self.scaleType]) % 12
			keySig = NOTE_NAMES[key].split('/')
			origSF = sf 
			if len(keySig) == 1:
				keySig = keySig[0]
			else:
				if origKeySig in CIRCLE_OF_FIFTHS.keys():
					origSF = CIRCLE_OF_FIFTHS[origKeySig]
				else:
					origSF = 1 if self.sharpFlatState == '#' else -1
					print "origSF =", origSF
			sf = origSF
		outchar = NOTE_NAMES[note].split('/')
		index = 0
		if len(outchar) > 1:
			if sf < 0:
				index = 1
		return outchar[index]
				
	def distance(self,x,a): 
		'''return a list of distances from x to each element in a'''
		return [math.sqrt((x-item)*(x-item)) for item in a]
		
	def closest(self,x,a):
		''' return index of closest element in a to x'''	
		deltas = self.distance(x,a)
		index,value = min(enumerate(deltas),key=lambda val:val[1])
		return index

	def touch_began(self,touch):
		if self.cc_mode == 'I':
			x,y = touch.location
			string = self.closest(x,self.stringX)
			fret = self.closest(y,self.fretY)
			location = (string,fret)
			if location in self.touched.keys():
				del self.touched[location]
			else:	
				for key in self.touched.keys():
					if key[0] == string:
						del self.touched[key]
						break
				self.touched[location] = (self.tuning['notes'][string]+fret,self.tuning['octave'],string,fret)
				octave,tone = divmod((self.tuning['notes'][string]+fret),12)
				waveName = 'waves/' + NOTE_FILE_NAMES[tone] + "{}.wav".format(octave+self.tuning['octave'])
				sound.play_effect(waveName)
			self.set_needs_display()
		elif self.cc_mode == 'S': # label the two octave scale starting at this root
			x,y = touch.location
			string = self.closest(x,self.stringX)
			fret = self.closest(y,self.fretY)
			location = (string,fret)
			octave,tone = divmod((self.tuning['notes'][string]+fret),12)
			if tone != self.key: 
				sound.play_effect('Drums_01')
				return None
			self.scaleFrets = calc_two_octave_scale(location)
			self.set_needs_display()
		elif self.cc_mode == 'C': # switch display to chord tones
			self.showChordScale = not self.showChordScale
			if self.showChordScale:
				#toggle on the scaleortone buttons
				self.ChordScaleFrets = calc_chord_scale()
			else:
				#toggle off the scaleotone buttons
				self.ChordScaleFrets = []
			self.set_needs_display()
			
		

#####################################
# fingering positions for drawing

	def fingeringDrawPositions(self,key,chordtype,tuning,fingering):
		""" given a fingering,chord and tuning information and virtual neck info,
		    return the center positions all markers.  X and open strings will be 
		    marked at the nut"""
		scaleNotes = getScaleNotes(key, chordtype, tuning, fingering)
		chordDrawPositions = []
		numStrings,offset,ss = self.stringSpacing()
		for i,fretPosition in enumerate(fingering): #loop over strings, low to high
			note = scaleNotes[i]
			atNut = None
			xpos = offset + i*ss	
			if fretPosition in [-1,0]: #marker at nut
				ypos = int(0.5* self.nutOffset) 
				atNut = 'X' if fretPosition else 'O'
			else:
				ypos = self.fretboardYPos(fretPosition)
			chordDrawPositions.append((xpos,ypos,note,atNut))		
			
		
		return chordDrawPositions		

	def get_instrument(self):
		return self.instrument
		
##########################################################
# instrument/tuning object
	
class Instrument(object):	
	global currentState
	def __init__(self, items, fb):
		self.items = items
		self.fb = fb
		self.instrument = currentState['instrument']
		
	def __getitem__(self,key):
		try:
			return self.tuning[key]
		except:
			return None
			 
	def reset(self):
		for item in self.items:
			item['accessory_type'] = 'none'
			
	
	
		
# when new instrument is chosen, update the global and 
# redraw the fretboard
# also draw first chord for the current root/type 
##############################
# Chapter ListView Select

	def isChecked(self,row): # is a checkbox set in a tableview items attribute
		return self.items[row]['accessory_type'] == 'checkmark'
		
#####################################################################
# Support routine to switch checkmark on and off in table view entry
		
	def toggleChecked(self,row):
		self.items[row]['accessory_type'] = 'none' if self.isChecked(row) else 'checkmark'


##############################################
# action for select
		
	def tableview_did_select(self,tableView,section,row): # Instrument
		global tuningDisplay
	
		self.toggleChecked(row)
		try:
			self.toggleChecked(self.tuning['row'])
		except:
			pass
		tableView.reload_data()	
		thisRow = self.items[row]
		self.tuning = { 
		               'title':		thisRow['title'],
		                'notes':	thisRow['notes'],
		                'span':		thisRow['span'],
		                'octave':	thisRow['octave'],
		                'row':		row
		               }
		currentState['instrument'] = self.tuning
		

		self.filters.set_filters() 
		self.tvFilters.reload_data()

		self.fb.scaleFrets = []
		mode = currentState['mode']
		
		if mode == 'C':
			self.fingerings = calc_fingerings()
			if self.fb.showChordScale:
				self.fb.ChordScaleFrets = calc_chord_scale()
			self.fb.set_fingerings(self.fingerings)
		elif mode == 'S':
			self.scale_notes = calc_scale_notes()
			self.fb.set_scale_notes(self.scale_notes)
		
		self.fb.touched = {}
		self.fb.set_needs_display()
		tuningDisplay.title = tuningLabel(self.tuning['notes'])
		
		
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		import ui
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]['title']
		cell.accessory_type = self.items[row]['accessory_type']
		return cell
				
###################################################
# chord type



class Chord(object):
	global curentState
	def __init__(self,items,fb):
		self.items = items
		self.chord = currentState['chord']
		self.fb = fb
		
	def __getitem__(self,key):
		try:
			return self.chord[key]
		except:
			return None	
			
	def reset(self):
		for item in self.items:
			item['accessory_type'] = 'none'
		
# when new chord is chosen, update the global

##############################
# Chapter ListView Select

	def isChecked(self,row): # is a checkbox set in a tableview items attribute
		return self.items[row]['accessory_type'] == 'checkmark'
		
#####################################################################
# Support routine to switch checkmark on and off in table view entry
		
	def toggleChecked(self,row):
		self.items[row]['accessory_type'] = 'none' if self.isChecked(row) else 'checkmark'

##############################################
# action for select
		
	def tableview_did_select(self,tableView,section,row):	#Chord
	
		self.toggleChecked(row)
		try:
			self.toggleChecked(self.chord['row'])
		except:
			pass
		tableView.reload_data()	
		self.chord = {'title': self.items[row]['title'], 'fingering': self.items[row]['fingering'], 'row':row}
		currentState['chord'] = self.chord
		
		setChordSpelling()
		
		fingerings = calc_fingerings()
		self.fb.set_fingerings(fingerings)
		if self.fb.showChordScale:
			self.fb.ChordScaleFrets = calc_chord_scale()
		self.fb.set_needs_display()
		
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]['title']
		cell.accessory_type = self.items[row]['accessory_type']
		return cell
		
	def get_chord(self):
		return self.chord
		
		

class Scale(object):
	global currentState
	def __init__(self, items,fb):
		self.items = items
		self.fb = fb
		
	def __getitem__(self,type):
		try:
			return self.scale[type]
		except:
			return None

	def reset(self):
		for item in self.items:
			item['accessory_type'] = 'none'
		
# when new chord is chosen, update the global

##############################
# Chapter ListView Select

	def isChecked(self,row): # is a checkbox set in a tableview items attribute
		return self.items[row]['accessory_type'] == 'checkmark'
		
#####################################################################
# Support routine to switch checkmark on and off in table view entry
		
	def toggleChecked(self,row):
		self.items[row]['accessory_type'] = 'none' if self.isChecked(row) else 'checkmark'

##############################################
# action for select
		
	def tableview_did_select(self,tableView,section,row):	#Scale
	
		self.toggleChecked(row)
		try:
			self.toggleChecked(self.scale['row'])
		except:
			pass
		tableView.reload_data()	
		self.scale = {'title': self.items[row]['title'], 
									'scaleintervals': self.items[row]['scaleintervals'], 'row':row}
		currentState['scale'] = self.scale
		
		self.scale_notes = calc_scale_notes()		
		relativeMajorDisplay()
		self.fb.set_scale_notes(self.scale_notes)
		self.fb.scaleFrets = []
		self.fb.set_needs_display()	
		
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]['title']
		cell.accessory_type = self.items[row]['accessory_type']
		return cell
		
	def get_scale(self):
		return self.scale
		
	
###################################################
# root tone


import ui

class Root(object):
	global currentState
	def __init__(self, items,fb):
		self.items = items
		self.root = currentState['root']
		self.fb = fb
		
	def __getitem__(self,key):
		try:
			return self.root[key]
		except:
			return None
			
	def reset(self):
		for item in self.items:
			item['accessory_type'] = 'none'
			
##############################
# Chapter ListView Select

	def isChecked(self,row): # is a checkbox set in a tableview items attribute
		return self.items[row]['accessory_type'] == 'checkmark'
		
#####################################################################
# Support routine to switch checkmark on and off in table view entry
		
	def toggleChecked(self,row):
		self.items[row]['accessory_type'] = 'none' if self.isChecked(row) else 'checkmark'

##############################################
# action for select
		
	def tableview_did_select(self,tableView,section,row): #Root
		
		self.toggleChecked(row)
		try:
			self.toggleChecked(self.root['row'])
		except:
			pass
		tableView.reload_data()	
		self.root = {'title': self.items[row]['title'], 'noteValue': self.items[row]['noteValue'], 'row':row}
		currentState['root'] = self.root
		
		mode = currentState['mode']
		if mode == 'C':
			self.fingerings = calc_fingerings()
			setChordSpelling()
			self.fb.set_fingerings(self.fingerings)
			if self.fb.showChordScale:
				self.fb.ChordScaleFrets = calc_chord_scale()
		elif mode == 'S':
			relativeMajorDisplay()
			self.scale_notes = calc_scale_notes()
			self.fb.scaleFrets = []
			self.fb.set_scale_notes(self.scale_notes)			
		

		self.fb.set_needs_display()
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]['title']
		cell.accessory_type = self.items[row]['accessory_type']
		return cell
		
	def get_root(self):
		try:
			return self.root
		except:
			return None
			
			
##################################################			
# 

class Filters(ui.View):
	global currentState,instrument_type
	def __init__(self,fb):
		self.fb = fb
		self.filter_list = []
		self.items = deepcopy(FILTER_LIST_CLEAN)
	
	def set_filters(self):
		self.filter_list = []
		self.items = deepcopy(FILTER_LIST_CLEAN)
		it = instrument_type()
		if it == 'guitar':
			self.items = self.items + deepcopy(GUITAR_LIST_CLEAN) 
		elif it == 'mandolin':
			self.items = self.items + deepcopy(MANDOLIN_LIST_CLEAN)
		else: # generic
			pass
		for item in self.items:
			item['accessory_type'] = 'none'
			
	
	def reconsile_filters(self,filter):
		if filter in FILTER_MUTUAL_EXCLUSION_LIST.keys():
			
			exclude = FILTER_MUTUAL_EXCLUSION_LIST[filter]
			for exclusion in exclude:
				if exclusion in self.filter_list:
					self.filter_list.remove(exclusion)
					for item in self.items:
						if item['title'] == exclusion:
							item['accessory_type'] = 'none'
					
			
		

##############################
# Chapter ListView Select

	def isChecked(self,row): # is a checkbox set in a tableview items attribute
		return self.items[row]['accessory_type'] == 'checkmark'
		
#####################################################################
# Support routine to switch checkmark on and off in table view entry
		
	def toggleChecked(self,row):
		self.items[row]['accessory_type'] = 'none' if self.isChecked(row) else 'checkmark'

	def offChecked(self,row):
		self.items[row]['accessory_type'] = 'none'
		
	def onChecked(self,row):
		self.items[row]['accessory_type'] = 'checkmark'

##############################################
# action for select
		
	def tableview_did_select(self,tableView,section,row):	#Filters
	
		self.toggleChecked(row)
		filtername = self.items[row]['title']

		if self.isChecked(row):
			if not filtername in self.filter_list:
				self.filter_list.append(filtername)
				self.reconsile_filters(filtername)		
		else:
			if filtername in self.filter_list:
				self.filter_list.remove(filtername)
				

		tableView.reload_data()	
		currentState['filters'] = self.filter_list
		self.fingerings = calc_fingerings()
		self.fb.set_fingerings(self.fingerings)
		self.fb.set_needs_display()		
				
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]['title']
		cell.accessory_type = self.items[row]['accessory_type']
		return cell
		
	def get_chord(self):
		return self.chord
		
		

#
# Display routines

def parseChordName(chordstr):
	p = re.compile('([A-G][#b]{0,1})(.*)', re.IGNORECASE)
	m = p.match(chordstr)
	if m != None:
		return m.group(1,2) # key and chordtype
	else:
		return ['','']

##########################################
##########################################
# S. Pollack Code below



###################################################
# previous/next chord form

def onPrevNext(button):
	global currentState
	try:
		fretboard = currentState['fretboard']
	except:
		return
	if fretboard.ChordPositions:
		cn = fretboard.get_chord_num()
		nc = fretboard.get_num_chords()
		if button.name == 'button_down':
			if cn < nc-1:
				cn +=1 
		else:
			cn -= 1
			if cn < 0:
				cn = 0
		fretboard.set_chord_num(cn)
		fretboard.set_needs_display()
					
	
###################################################
# play arpeggio

def play(button):
	global currentState
	fretboard = currentState['fretboard']
	if os.path.exists('waves'):
		baseOctave = currentState['instrument']['octave']
		strings = currentState['instrument']['notes']
		if fretboard.cc_mode == 'C':
			cc = fretboard.ChordPositions[fretboard.currentPosition]
			frets = cc[2]
			dead_notes = [item[3] == 'X' for item in cc[0]]
			tones = []
			for fret,string,dead_note in zip(frets,strings,dead_notes):
				if  dead_note:
					continue
				octave,tone = divmod(string + fret,12) 
				tones.append((tone,octave+baseOctave))
		elif fretboard.cc_mode == 'I': # identify
			positions = [string_fret for string_fret in fretboard.touched.keys()]
			positions = sorted(positions,key=lambda x:x[0])
			position_dict = {}
			for string,fret in positions:
				position_dict[string] = fret
			tones = []
			for i,pitch in enumerate(strings):
				if position_dict.has_key(i):
					octave,tone = divmod(pitch + position_dict[i],12)
					tones.append((tone,octave+baseOctave))
		
		else: #scale
			pass
			
		for tone,octave in tones:
			waveName = 'waves/' + NOTE_FILE_NAMES[tone] + "{}.wav".format(octave)
			sound.play_effect(waveName)
			time.sleep(0.05)
			if button.name == 'button_arp':
				time.sleep(fretboard.arpSpeed)
	

def play_tuning(button):
	global currentState
	fretboard = currentState['fretboard']
	if os.path.exists('waves'):
		try:
			cc = fretboard.ChordPositions[fretboard.currentPosition]
			frets = cc[2]
			dead_notes = [item[3] == 'X' for item in cc[0]]
		except:
			pass
		strings = currentState['instrument']['notes']
		baseOctave = currentState['instrument']['octave']
		tones = []
		for string in strings:
			octave,tone = divmod(string,12)
			tones.append((tone,octave+baseOctave))
		for tone,octave in tones:
			waveName = 'waves/' + NOTE_FILE_NAMES[tone] + "{}.wav".format(octave)
			sound.play_effect(waveName)
			time.sleep(fretboard.arpSpeed)
			
def playScale(button):	
	global currentState
	fretboard = currentState['fretboard']
	if os.path.exists('waves') and fretboard.scaleFrets:
		for string,fret in fretboard.scaleFrets:
			octave,tone = divmod((fretboard.tuning['notes'][string]+fret),12)
			waveName = 'waves/' + NOTE_FILE_NAMES[tone] + "{}.wav".format(octave+fretboard.tuning['octave'])
			sound.play_effect(waveName)	
			time.sleep(fretboard.arpSpeed)

def toggle_mode(button):
	global currentState #,fretboard,tvFind,tvScale
	fretboard = currentState['fretboard']
	tvFind = currentState['tvFind']
	tvScale = currentState['tvScale']
	mainView = currentState['mainView']


	mode = button.title
	hideshow = {}
	hideshow = {'I':  {'hide':
	                					'tableview_root tableview_type tableview_scale label1 label_type_scale button_scale_notes button_scale_tones chord_num label_middle button_play_scale num_chords lbl_chord lbl_fullchord lbl_definition btn_sharpFlat'.split(),
											'show':
														('tableview_find', 'button_find', 'button_chord', 'button_arp')
										},						
 							'C':	{'hide':
										 				'tableview_find button_find button_scale_tones button_scale_notes tableview_scale button_play_scale lbl_chord lbl_fullchord btn_sharpFlat'.split(),
										'show': 'tableview_root tableview_type label1 label_type_scale chord_num num_chords label_middle button_chord button_arp'.split()
										},
							'S': 	{'hide': 
										 					'tableview_type tableview_find button_find chord_num num_chords label_middle button_chord button_arp lbl_chord lbl_fullchord lbl_definition'.split(),
											'show': 'tableview_scale tableview_root button_scale_tones button_scale_notes label_type_scale button_play_scale btn_sharpFlat'.split()
										}
								}

	fretboard.cc_mode = mode
	currentState['mode'] = mode
	mode_hs = hideshow[mode]
	for view in mode_hs['hide']:		
		mainView[view].hidden = True
	for view in mode_hs['show']:			
		mainView[view].hidden = False
	
	if mode == 'C': # special stuff for identify
		mainView['label_type_scale'].text = 'type'
	elif mode == 'S':
		mainView['label_type_scale'].text = 'mode'
	else: # 'I'
		mainView['label_type_scale'].text = ''		
		tvFind.data_source.items = []
		
	fretboard.set_needs_display()
	mainView.set_needs_display()
	
	
def set_scale_display(button):
	global currrentState
	fretboard = currentState['fretboard']
	fretboard.scale_display_mode = button.title
	fretboard.set_needs_display()
	
def find_chords(button):
	global currentState
	fretboard = currentState['fretboard']
	tvFind = currentState['tvFind']
	fingered = [fretboard.touched[key][0] for key in fretboard.touched.keys()]
	if fingered:
		fingered = sorted([x%12 for x in fingered])
		pure = []
		missing_1 = []
		missing_2 = []
		chord_list = []
		for root in range(12):
			notes_in_key = rotate(range(12),root)
			present = {}
			notevals = []
			for i,note in enumerate(notes_in_key):
				present[i] = True if note in fingered else False
				if present[i]: 
					notevals.append(i)
			for chord in CHORDTYPE:
				deltas = set(notevals) ^ set(chord[1]) #those notes not in both (symmetric difference)
				if not deltas:
					pure.append("{}{}".format(NOTE_NAMES[root],chord[0]))
				if deltas == set([0]):
					missing_1.append("{}{} (no root)".format(NOTE_NAMES[root],chord[0]))
				if deltas == set([3]) or deltas == set([4]):
					missing_1.append("{}{} (no 3rd)".format(NOTE_NAMES[root],chord[0]))				
				if deltas == set([7]):
					missing_1.append( "{}{} (no 5th)".format(NOTE_NAMES[root],chord[0]))
				if deltas == set([0,7]):
					missing_2.append("{}{} (no root or 5th)".format(NOTE_NAMES[root],chord[0]))
		for list in [pure,missing_1,missing_2]:
			if list:
				chord_list += list
				chord_list.append("-------")
		tvFind.data_source.items = chord_list
		tvFind.reload_data()	
		
def on_slider(sender):
	sound.set_volume(sender.value)
	
def on_slider_arp(sender):
	global currentState
	fretboard = currentState['fretboard']
	v = sender.value
	fretboard.arpSpeed = fretboard.arpMin*v + (1.0-v)*fretboard.arpMax
		
##############################################
##############################################
if __name__ == "__main__":	
	if not os.path.exists('waves'):
		console.alert('waves sound files not present, run makeWave.py')
		sys.exit(1)
	currentState = {'root':None,'chord':None,'instrument':None,'filters':None,'scale': None,'mode':'C'}	
	mainView = ui.load_view()
	num_chords = mainView['num_chords']
	chord_num = mainView['chord_num']
	middle_field = mainView['label_middle']
	fretboard = mainView['fretboard']
	tvRoot = mainView['tableview_root']
	root_list = deepcopy(ROOT_LIST_CLEAN)
	root = Root(root_list,fretboard)
	tvRoot.data_source = tvRoot.delegate = root
	
	tvType = mainView['tableview_type']
	chord_list = deepcopy(CHORD_LIST_CLEAN)
	chord = Chord(chord_list,fretboard)
	chord.reset()
	tvType.data_source = tvType.delegate = chord
	
	tvInst = mainView['tableview_inst_tune']
	tuningDisplay = mainView['button_tuning']
	tuningDisplay.title = ''
	tuningDisplay.action = play_tuning

	# fretboard is a custom view and is instanciated by the ui.load_view process
	tuning_list = deepcopy(TUNING_LIST_CLEAN)
	instrument = Instrument(tuning_list,fretboard)
	instrument.reset()
	tvInst.data_source = tvInst.delegate = fretboard.instrument = instrument
	
	tvFilters = mainView['tableview_filters']
	filter_list = deepcopy(FILTER_LIST_CLEAN)
	filters = Filters(fretboard)
	instrument.tvFilters = tvFilters
	instrument.filters = filters
	filters.instrument = instrument
	tvFilters.data_source = tvFilters.delegate = filters
	tvFilters.hidden = False

	tvFind = mainView['tableview_find']
	tvFind.data_source.items = []
	tvFind.hidden = True

	tvScale = mainView['tableview_scale']
	tvScale.data_source.items = []
	tvScale.hidden = True	
	scale_list = deepcopy(SCALE_LIST_CLEAN)
	scale = Scale(scale_list,fretboard)
	tvScale.data_source = tvScale.delegate = scale
	
	mainView['button_arp'].action = play
	mainView['button_chord'].action = play
	mainView['button_ident'].action = toggle_mode
	mainView['button_calc'].action = toggle_mode
	mainView['button_scale'].action = toggle_mode
	mainView['button_scale_notes'].action = set_scale_display
	mainView['button_scale_tones'].action = set_scale_display
	mainView['button_find'].action = find_chords
	mainView['button_find'].hidden = True
	mainView['button_up'].action = mainView['button_down'].action = onPrevNext
	mainView['button_scale'].action = toggle_mode
	mainView['button_play_scale'].action = playScale
	mainView['btn_sharpFlat'].action = fretboard.sharpFlat
	mainView['btn_sharpFlat'].hidden = True
	mainView['slider_arp'].action = on_slider_arp
	mainView['lbl_chord'].hidden = True
	mainView['lbl_fullchord'].hidden = True
	mainView['lbl_definition'].hidden = True
	
	currentState['tvFind'] = tvFind
	currentState['tvScale'] = tvScale
	currentState['fretboard'] = fretboard
	currentState['mainView'] = mainView

	fretboard.set_chordnum(chord_num,num_chords)
	toggle_mode(mainView['button_calc'])
	sound.set_volume(0.5)
	mainView.present(style='full_screen',orientations=('landscape',))
