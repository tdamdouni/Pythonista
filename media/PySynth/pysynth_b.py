#!/usr/bin/env python
# -*- coding: latin-1 -*-

#print "*** EXPERIMENTAL PIANO VERSION WITH NOTE CACHING ***"

"""
##########################################################################
#                       * * *  PySynth  * * *
#       A very basic audio synthesizer in Python (www.python.org)
#
#          Martin C. Doege, 2009-06-08 (mdoege@compuserve.com)
##########################################################################
# Based on a program by Tyler Eaves (tyler at tylereaves.com) found at
#   http://mail.python.org/pipermail/python-list/2000-August/049968.html
##########################################################################

# 'song' is a Python list (or tuple) in which the song is defined,
#   the format is [['note', value]]

# Notes are 'a' through 'g' of course,
# optionally with '#' or 'b' appended for sharps or flats.
# Finally the octave number (defaults to octave 4 if not given).
# An asterisk at the end makes the note a little louder (useful for the beat).
# 'r' is a rest.

# Note value is a number:
# 1=Whole Note; 2=Half Note; 4=Quarter Note, etc.
# Dotted notes can be written in two ways:
# 1.33 = -2 = dotted half
# 2.66 = -4 = dotted quarter
# 5.33 = -8 = dotted eighth
"""

import wave, struct
import numpy as np
from math import sin, cos, pi, log, exp

# Example 1: The C major scale
song1 = [
['c',4],['d',4],['e',4],['f',4],['g',4],['a',4],['b',4],['c5',2],['r',1],
['c3',4],['d3',4],['e3',4],['f3',4],['g3',4],['a3',4],['b3',4],['c4',2],['r',1],
['c1*', 1], ['c2*', 1], ['c3*', 1], ['c4*', 1], ['c5*', 1], ['c6*', 1], ['c7*', 1], ['c8*', 1],
]

# Example 2: Something a little more patriotic
song2 = (
  ('g', -8), ('e', 16),
  ('c*', 4), ('e', 4), ('g', 4),
  ('c5*', 2), ('e5', -8), ('d5', 16),
  ('c5*', 4), ('e', 4), ('f#', 4),
  ('g*', 2), ('g', 8), ('g', 8),
  ('e5*', -4), ('d5', 8), ('c5', 4),
  ('b*', 2), ('a', -8), ('b', 16),
  ('c5*', 4), ('c5', 4), ('g', 4),
  ('e*', 4), ('c', 4),
)

# Example 3: Beginning of Nocturne Op. 9 #2 by F. Chopin
song3 = (
  ('bb', 8),
  ('g5*', 2), ('f5', 8), ('g5', 8), ('f5', -4), ('eb5', 4), ('bb', 8),
  ('g5*', 4), ('c5', 8), ('c6', 4), ('g5', 8), ('bb5', -4), ('ab5', 4), ('g5', 8),
  ('f5*', -4), ('g5', 4), ('d5', 8), ('eb5', -4), ('c5', -4),
  ('bb*', 8), ('d6', 8), ('c6', 8), ('bb5', 16), ('ab5', 16), ('g5', 16), ('ab5', 16), ('c5', 16), ('d5', 16), ('eb5', -4),
)

# Example 4: J.S. Bach: Bourrée (from BWV 996)
song4_rh = (
  ('e', 8), ('f#', 8),
  ('g*', 4), ('f#', 8), ('e', 8), ('d#*', 4), ('e', 8), ('f#', 8),
  ('b3*', 4), ('c#', 8), ('d#', 8), ('e*', 4), ('d', 8), ('c', 8),
  ('b3*', 4), ('a3', 8), ('g3', 8), ('f#3*', 4), ('g3', 8), ('a3', 8),
  ('b3*', 8), ('a3', 8), ('g3', 8), ('f#3', 8), ('e3*', 4), ('e', 8), ('f#', 8),
  ('g*', 4), ('f#', 8), ('e', 8), ('d#*', 4), ('e', 8), ('f#', 8),
  ('b3*', 4), ('c#', 8), ('d#', 8), ('e*', 4), ('d', 8), ('c', 8),
  ('b3*', 4), ('a3', 8), ('g3', 8), ('g3*', 32), ('f#3*', 32), ('g3*', 32), ('f#3*', 32), ('g3*', 32), ('f#3*', 32), ('g3*', 32), ('f#3*', 6.4), ('g3', 8), ('g3*', -2),
)
# version without the trill:
#  ('b3*', 4), ('a3', 8), ('g3', 8), ('f#3*', -4), ('g3', 8), ('g3*', -2),

song4_lh = (
  ('g2', 8), ('f#2', 8),
  ('e2*', 4), ('a2', 4), ('b2', 4), ('a2', 4),
  ('g2*', 4), ('f#2', 4), ('e2', 4), ('f#2', 4),
  ('g2*', 4), ('a2', 4), ('b2', 4), ('a2', 4),
  ('g2*', 4), ('b2', 4), ('e2', 8), ('f#2', 8), ('g2', 8), ('f#2', 8),
  ('e2*', 4), ('a2', 4), ('b2', 4), ('a2', 4),
  ('g2*', 4), ('f#2', 4), ('e2', 4), ('f#2', 4),
  ('g2*', 4), ('c3', 4), ('d3', 4), ('d3', 4),
  ('b2*', -2),
)

##########################################################################
# Compute and print piano key frequency table
##########################################################################
pitchhz, keynum = {}, {}
keys_s = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
keys_f = ('a', 'bb', 'b', 'c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab')

# Harmonic intensities (dB) for selected piano keys,
# measured with output from a Yamaha P-85
harmo = (
  (1, -15.8, -3., -15.3, -22.8, -40.7),
  (16, -15.8, -3., -15.3, -22.8, -40.7),
  (28, -5.7, -4.4, -17.7, -16., -38.7),
  (40, -6.8, -17.2, -22.4, -16.8, -75.6),
  (52, -8.4, -19.7, -23.5, -21.6, -76.8),
  (64, -9.3, -20.8, -37.2, -36.3, -76.4),
  (76, -18., -64.5, -74.4, -77.3, -80.8),
  (88, -24.8, -53.8, -77.2, -80.8, -90.),
)

def linint(arr, x):
	"Interpolate an (X, Y) array linearly."
	for v in arr:
		if v[0] == x: return v[1]
	xvals = [v[0] for v in arr]
	ux = max(xvals)
	lx = min(xvals)
	try: assert lx <= x <= ux
	except:
		#print lx, x, ux
		raise
	for v in arr:
		if v[0] > x and v[0] - x <= ux - x:
			ux = v[0]
			uy = v[1]
		if v[0] < x and x - v[0] >= lx - x:
			lx = v[0]
			ly = v[1]		
	#print lx, ly, ux, uy
	return (float(x) - lx) / (ux - lx) * (uy - ly) + ly


#if __name__ == '__main__':
    #print "Piano key frequencies (for equal temperament):"
    #print "Key number\tScientific name\tFrequency (Hz)"
for k in range(88):
    freq = 27.5 * 2.**(k/12.)
    oct = (k+9) // 12
    note = '%s%u' % (keys_s[k%12], oct)
    #if __name__ == '__main__':
    #    print "%10u\t%15s\t%14.2f" % (k+1, note.upper(), freq)
    pitchhz[note] = freq
    keynum[note] = k
    note = '%s%u' % (keys_f[k%12], oct)
    pitchhz[note] = freq
    keynum[note] = k

harmtab = np.zeros((88, 20))

for h in range(1, len(harmo[0])):
	dat = []
	for n in range(len(harmo)):
		dat.append((float(harmo[n][0]), harmo[n][h]))
	for h2 in range(88):
		harmtab[h2,h] = linint(dat, h2+1)

#print harmtab[keynum['c4'],:]
for h2 in range(88):
	for n in range(20):
		ref = harmtab[h2,1]
		harmtab[h2,n] = 10.**((harmtab[h2,n] - ref)/20.)
#print harmtab[keynum['c4'],:]

##########################################################################
#### Main program starts below
##########################################################################
# Some parameters:

# Beats (quarters) per minute
# e.g. bpm = 95

# Octave shift (neg. integer -> lower; pos. integer -> higher)
# e.g. transpose = 0

# Playing style (e.g., 0.8 = very legato and e.g., 0.3 = very staccato)
# e.g. leg_stac = 0.6

# Volume boost for asterisk notes (1. = no boost)
# e.g. boost = 1.2

# Output file name
#fn = 'pysynth_output.wav'

# Other parameters:

# Influences the decay of harmonics over frequency. Lowering the
# value eliminates even more harmonics at high frequencies.
# Suggested range: between 3. and 5., depending on the frequency response
#  of speakers/headphones used
harm_max = 5.
##########################################################################

data = []
note_cache = {}
cache_this = {}

def make_wav(song,bpm=120,transpose=0,leg_stac=.9,boost=1.1,repeat=0,fn="out.wav", silent=False):
	f=wave.open(fn,'w')

	f.setnchannels(1)
	f.setsampwidth(2)
	f.setframerate(44100)
	f.setcomptype('NONE','Not Compressed')

	bpmfac = 120./bpm

	def length(l):
	    return 88200./l*bpmfac

	def waves2(hz,l):
	    a=44100./hz
	    b=float(l)/44100.*hz
	    return [a,round(b)]

	att_len = 3000
	att_bass = np.zeros(att_len)
	att_treb = np.zeros(att_len)
	for n in range(att_len):
		att_treb[n] = linint(((0,0.), (100, .2), (300, .7), (400, .6), (600, .25), (800, .9), (1000, 1.25), (2000,1.15), (3000, 1.)), n)
		att_bass[n] = linint(((0,0.), (100, .1), (300, .2), (400, .15), (600, .1), (800, .9), (1000, 1.25), (2000,1.15), (3000, 1.)), n)
	decay = np.zeros(1000)
	for n in range(900):
		decay[n] = exp(linint(( (0,log(3)), (3,log(5)), (5, log(1.)), (6, log(.8)), (9,log(.1)) ), n/100.))

	def render2(a, b, vol, pos, knum, note):
	    l=waves2(a, b)
	    q=int(l[0]*l[1])

	    lf = log(a)
	    t = (lf-3.) / (8.5-3.)
	    volfac = 1. + .8 * t * cos(pi/5.3*(lf-3.))
	    schweb = waves2(lf*100., b)[0]
	    schweb_amp = .05 - (lf-5.) / 100.
	    att_fac = min(knum / 87. * vol, 1.)
	    snd_len = max(int(3.1*q), 44100)
	    fac = np.ones(snd_len)
	    fac[:att_len] = att_fac * att_treb + (1.-att_fac) * att_bass

	    raw_note = 12*44100
	    if note not in note_cache.keys():
	        x2 = np.arange(raw_note)
	    	sina = 2. * pi * x2 / float(l[0])
		ov = np.exp(-x2/3./decay[int(lf*100)]/44100.)
	   	new = (( np.sin(sina)
	              + ov*harmtab[kn,2]*np.sin(2. * sina)
	              + ov*harmtab[kn,3]*np.sin(3. * sina)
	              + ov*harmtab[kn,4]*np.sin(4. * sina)
	              + ov*harmtab[kn,5]*np.sin(8. * sina)
			) * volfac )
		new *= np.exp(-x2/decay[int(lf*100)]/44100.)
		if cache_this[note] > 1:
			note_cache[note] = new.copy()
			#print "Caching", note
	    else:
		new = note_cache[note].copy()
	    dec_ind = int(leg_stac*q)
	    new[dec_ind:] *= np.exp(-np.arange(raw_note-dec_ind)/3000.)
	    #print snd_len, raw_note
	    data[pos:pos+snd_len] += ( new[:snd_len] * fac * vol *
		       (1. + schweb_amp * np.sin(2. * pi * np.arange(snd_len)/schweb/32.) )  )

	ex_pos = 0.
	t_len = 0
	for y, x in song:
		if x < 0:
			t_len+=length(-2.*x/3.)
		else:
			t_len+=length(x)
		if y[-1] == '*':
			y = y[:-1]
		if not y[-1].isdigit():
			y += '4'
		cache_this[y] = cache_this.get(y, 0) + 1
	#print "Note frequencies in song:", cache_this
	data = np.zeros((repeat+1)*t_len + 441000.)
	#print len(data)/44100., "s allocated"

	for rp in range(repeat+1):
		for nn, x in enumerate(song):
		    if not nn % 4 and silent == False:
		        print "[%u/%u]\t" % (nn+1,len(song))
		    if x[0]!='r':
		        if x[0][-1] == '*':
		            vol = boost
		            note = x[0][:-1]
		        else:
		            vol = 1.
		            note = x[0]
			if not note[-1].isdigit():
			    note += '4'		# default to fourth octave
		        a=pitchhz[note]
			kn = keynum[note]
		        a = a * 2**transpose
		        if x[1] < 0:
		            b=length(-2.*x[1]/3.)
		        else:
		            b=length(x[1])

		        render2(a, b, vol, int(ex_pos), kn, note)
			ex_pos = ex_pos + b

		    if x[0]=='r':
		        b=length(x[1])
			ex_pos = ex_pos + b

	##########################################################################
	# Write to output file (in WAV format)
	##########################################################################
	if silent == False:
		print "Writing to file", fn

	data = data / (data.max() * 2.)
	out_len = int(2. * 44100. + ex_pos+.5)
	data2 = np.zeros(out_len, np.short)
	data2[:] = 32000. * data[:out_len]
	f.writeframes(data2.tostring())
	f.close()
	print

def mix_files(a, b, c, chann = 2, phase = -1.):
	f1 = wave.open(a,'r')
	f2 = wave.open(b,'r')
	f3 = wave.open(c,'w')
	f3.setnchannels(chann)
	f3.setsampwidth(2)
	f3.setframerate(44100)
	f3.setcomptype('NONE','Not Compressed')
	frames = min(f1.getnframes(), f2.getnframes())

	print "Mixing files, total length %.2f s..." % (frames / 44100.)
	d1 = f1.readframes(frames)
	d2 = f2.readframes(frames)
	for n in range(frames):
		if not n%(5*44100): print n // 44100, 's'
		if chann < 2:
			d3 = struct.pack('h',
				.5 * (struct.unpack('h', d1[2*n:2*n+2])[0] +
				struct.unpack('h', d2[2*n:2*n+2])[0]))
		else:
			d3 = ( struct.pack('h',
				phase * .3 * struct.unpack('h', d1[2*n:2*n+2])[0] +
				.7 * struct.unpack('h', d2[2*n:2*n+2])[0]) +
				struct.pack('h',
				.7 * struct.unpack('h', d1[2*n:2*n+2])[0] +
				phase * .3 * struct.unpack('h', d2[2*n:2*n+2])[0]) )
		f3.writeframesraw(d3)
	f3.close()

##########################################################################
# Synthesize demo songs
##########################################################################

if __name__ == '__main__':
	print "*** EXPERIMENTAL PIANO VERSION WITH NOTE CACHING ***"
	print
	print "Creating Demo Songs... (this might take about a minute)"
	print

	#make_wav((('c', 4), ('e', 4), ('g', 4), ('c5', 1)))
	#make_wav(song1, fn = "pysynth_scale.wav")
	#make_wav((('c1', 1), ('r', 1),('c2', 1), ('r', 1),('c3', 1), ('r', 1), ('c4', 1), ('r', 1),('c5', 1), ('r', 1),('c6', 1), ('r', 1),('c7', 1), ('r', 1),('c8', 1), ('r', 1), ('r', 1), ('r', 1), ('c4', 1),('r', 1), ('c4*', 1), ('r', 1), ('r', 1), ('r', 1), ('c4', 16), ('r', 1), ('c4', 8), ('r', 1),('c4', 4), ('r', 1),('c4', 1), ('r', 1),('c4', 1), ('r', 1)), fn = "all_cs.wav")
	make_wav(song4_rh, bpm = 130, transpose = 1, boost = 1.15, repeat = 1, fn = "pysynth_bach_rh.wav")
	make_wav(song4_lh, bpm = 130, transpose = 1, boost = 1.15, repeat = 1, fn = "pysynth_bach_lh.wav")
	mix_files("pysynth_bach_rh.wav", "pysynth_bach_lh.wav", "pysynth_bach.wav")

	make_wav(song3, bpm = 132/2, leg_stac = 0.9, boost = 1.1, fn = "pysynth_chopin.wav")
