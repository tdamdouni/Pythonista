#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
##########################################################################
#                       * * *  PySynth  * * *
#       A very basic audio synthesizer in Python (www.python.org)
#
#          Martin C. Doege, 2009-04-07 (mdoege@compuserve.com)
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
pitchhz = {}
keys_s = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
keys_f = ('a', 'bb', 'b', 'c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab')

if __name__ == '__main__':
    print "Piano key frequencies (for equal temperament):"
    print "Key number\tScientific name\tFrequency (Hz)"
for k in range(88):
    freq = 27.5 * 2.**(k/12.)
    oct = (k+9) // 12
    note = '%s%u' % (keys_s[k%12], oct)
    if __name__ == '__main__':
        print "%10u\t%15s\t%14.2f" % (k+1, note.upper(), freq)
    pitchhz[note] = freq
    note = '%s%u' % (keys_f[k%12], oct)
    pitchhz[note] = freq

##########################################################################
#### Main program starts below
##########################################################################
# Some parameters:

# Beats (quarters) per minute
# e.g. bpm = 95

# Octave shift (neg. integer -> lower; pos. integer -> higher)
# e.g. transpose = 0

# Pause between notes as a fraction (0. = legato and e.g., 0.5 = staccato)
# e.g. pause = 0.05

# Volume boost for asterisk notes (1. = no boost)
# e.g. boost = 1.2

# Output file name
#fn = 'pysynth_output.wav'

# Other parameters:

# Influences the decay of harmonics over frequency. Lowering the
# value eliminates even more harmonics at high frequencies.
# Suggested range: between 3. and 5., depending on the frequency response
#  of speakers/headphones used
harm_max = 4.
##########################################################################

import wave, math, struct

def make_wav(song,bpm=120,transpose=0,pause=.05,boost=1.1,repeat=0,fn="out.wav", silent=False):
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

	def sixteenbit(x):
	    return struct.pack('h', round(32000*x))

	def asin(x):
	    return math.sin(2.*math.pi*x)

	def render2(a,b,vol):
	    b2 = (1.-pause)*b
	    l=waves2(a,b2)
	    ow=""
	    q=int(l[0]*l[1])

	    # harmonics are frequency-dependent:
	    lf = math.log(a)
	    lf_fac = (lf-3.) / harm_max
	    if lf_fac > 1: harm = 0
	    else: harm = 2. * (1-lf_fac)
	    decay = 2. / lf
	    t = (lf-3.) / (8.5-3.)
	    volfac = 1. + .8 * t * math.cos(math.pi/5.3*(lf-3.))

	    for x in range(q):
	         fac=1.
	         if x<100: fac=x/80.
	         if 100<=x<300: fac=1.25-(x-100)/800.
	         if x>q-400: fac=1.-((x-q+400)/400.)
	         s = float(x)/float(q)
	         dfac =  1. - s + s * decay
	         ow=ow+sixteenbit((asin(float(x)/l[0])
	              +harm*asin(float(x)/(l[0]/2.))
	              +.5*harm*asin(float(x)/(l[0]/4.)))/4.*fac*vol*dfac*volfac)
	    fill = max(int(ex_pos - curpos - q), 0)
	    f.writeframesraw((ow)+(sixteenbit(0)*fill))
	    return q + fill

	##########################################################################
	# Write to output file (in WAV format)
	##########################################################################

	if silent == False:
		print "Writing to file", fn
	curpos = 0
	ex_pos = 0.
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
			try:
		            a=pitchhz[note]
			except:
		            a=pitchhz[note + '4']	# default to fourth octave
		        a = a * 2**transpose
		        if x[1] < 0:
		            b=length(-2.*x[1]/3.)
		        else:
		            b=length(x[1])
			ex_pos = ex_pos + b
		        curpos = curpos + render2(a,b,vol)

		    if x[0]=='r':
		        b=length(x[1])
			ex_pos = ex_pos + b
		        f.writeframesraw(sixteenbit(0)*int(b))
			curpos = curpos + int(b)

	f.writeframes('')
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
	print
	print "Creating Demo Songs... (this might take about a minute)"
	print

	# SONG 1
	make_wav(song1, fn = "pysynth_scale.wav")

	# SONG 2
	make_wav(song2, bpm = 95, boost = 1.2, fn = "pysynth_anthem.wav")

	# SONG 3
	make_wav(song3, bpm = 132/2, pause = 0., boost = 1.1, fn = "pysynth_chopin.wav")

	# SONG 4
	#   right hand part
	make_wav(song4_rh, bpm = 130, transpose = 1, pause = .1, boost = 1.15, repeat = 1, fn = "pysynth_bach_rh.wav")
	#   left hand part
	make_wav(song4_lh, bpm = 130, transpose = 1, pause = .1, boost = 1.15, repeat = 1, fn = "pysynth_bach_lh.wav")
	#   mix both files together
	mix_files("pysynth_bach_rh.wav", "pysynth_bach_lh.wav", "pysynth_bach.wav")
