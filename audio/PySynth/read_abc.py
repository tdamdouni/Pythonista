#!/usr/bin/env python

"""
Parse a file in ABC music notation format and render with PySynth.

Usage:

read_abc.py filename [num_song] [--syn_b/--syn_s]

* num_song selects the song in the file corresponding to the number given
* --syn_b and --syn_s can be added to use the PySynth B or PySynth S
    modules, respectively, instead of the default PySynth A

Some of the definitions are borrowed from PlayABC 1.1

2012-07-17
"""

import sys, urllib2

sel = False
try: num = int(sys.argv[2])
except: num = 1
song = []

if "--syn_b" in sys.argv:
	import pysynth_b as pysynth
elif "--syn_s" in sys.argv:
	import pysynth_s as pysynth
else:
	import pysynth


# flatten or sharpen notes according to key signature
# key_sig is in range [-7 .. + 7] meaning that many
# flats (-ve) or sharps (+ve)

key_sigs = (
  ("C",    "Am",    0),
  ("GMix", "DDor",  0),
  ("G",    "Em",    1),
  ("DMix", "ADor",  1),
  ("F",    "Dm",   -1),
  ("CMix", "GDor", -1),
  ("D",    "Bm",    2),
  ("AMix", "EDor",  2),
  ("HP",   "Hp",    2),         # Highland pipes dontcha know
  ("Bb",   "Gm",   -2),
  ("FMix", "CDor", -2),
  ("A",    "F#m",   3),
  ("EMix", "BDor",  3),
  ("Eb",   "Cm",   -3),         # Suspect that more than this will never be
  ("BbMix","FDor", -3),         # used, but what the hell ...
  ("E",    "C#m",   4),
  ("BMix", "F#Dor", 4),
  ("Ab",   "Fm",   -4),
  ("EbMix","BbDor",-4),
  ("B",    "G#m",   5),
  ("F#Mix","C#Dor", 5),
  ("Db",   "Bbm",  -5),
  ("AbMix","EbDor",-5),
  ("F#",   "D#m",   6),
  ("C#Mix","G#Dor", 6),
  ("Gb",   "Ebm",  -6),
  ("DbMix","AbDor",-6),
  ("C#",   "A#m",   7),
  ("G#Mix","D#Dor", 7),
  ("Cb",   "Abm",  -7),
  ("GbMix","DbDor",-7),
)

# A table of which note is flattened or sharpened next.
# ( 1st flat = B, 2nd = E, 3rd = A ...
#   1st sharp = F, second = C, 3rd = G ...)

flats_and_sharps = '', 'f', 'c', 'g', 'd', 'a', 'e', 'b'

keys_s = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
keys_f = ('a', 'bb', 'b', 'c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab')

piano_s, piano_f = [], []

for k in range(88):
	oct = (k+9) // 12
	note = '%s%u' % (keys_s[k%12], oct)
	piano_s.append(note)
	note = '%s%u' % (keys_f[k%12], oct)
	piano_f.append(note)

def simp_line(a):
	a2, a3 = [], []
	ign = False
	for x in a:
		if x == '"': ign = not ign
		if not ign:
			a2 += x
	for x in range(len(a2)):
		if a2[x] == '[':
			c = x
			found_col = False
			for x2 in range(c, len(a2)):
				if a2[x2] == ':':
					found_col = True
				if a2[x2] == ']' and found_col:
					for x3 in range(c, x2+1):
						a2[x3] = ' '
					break			
	return ''.join(a2)

chord = False
tie_next = 0
second_ver, do_repeat, only_first, triplet = [], False, False, 0

def add_note(a, n):
	global song, chord, measure_sharps_flats, tie_next, second_ver, do_repeat, only_first, triplet, tripfac

	start, note, leng, next_half, firstnote = (
		False, None, float(unit), False, '')
	for x in range(n, len(a)):
		if note and a[x] in (' ', '>', '(', '|', ':'):
			break
		if a[x] == '>':
			l = 1. / song[-1][1]
			l = 1.5 * l
			song[-1][1] = 1. / l
			next_half = True
			continue
		if not note and a[x] == '%':
			return
		if not note and a[x] == '(' and a[x+1].isdigit():
			triplet = int(a[x+1])
			tripfac = triptab[triplet]
			try:
				if a[x+2] == ':':
					tripfac = float(triplet) / float(a[x+3])
					if a[x+4] == ':':
						triplet = int(a[x+5])
			except: pass
		if not note and a[x] == '[':
			chord = True
			continue
		if not note and a[x] == '|':
			firstnote = '*'
			measure_sharps_flats = global_sharps_flats.copy()
			if a[x+1] == ':':
				second_ver, do_repeat = [], True
			if a[x+1] == '1':
				only_first = True
			if a[x+1] == '2':
				only_first = False
			continue
		if not note and a[x] == ':':
			if a[x+1] == ':' or a[x+1] == '|':
				song = song + second_ver
				second_ver, do_repeat = [], False
		if note and a[x] == '-':
			tie_next = 2
			continue
		if a[x] == ',':
			oct -= 1
			note_oct = "%s%u" % (note, oct)
			continue
		if a[x] == "'":
			oct += 1
			note_oct = "%s%u" % (note, oct)
			continue
		if not note and a[x].isalpha():
			note = a[x].lower()
			if a[x].isupper(): oct = 4
			else: oct = 5
			note_oct = "%s%u" % (note, oct)
			if a[x-1] == '_':
				for oct2 in range(9):
					note_oct2 = "%s%u" % (note, oct2)
					orig = measure_sharps_flats.get(note_oct2, 0)
					measure_sharps_flats[note_oct2] = orig - 1
			if a[x-1] == '^':
				for oct2 in range(9):
					note_oct2 = "%s%u" % (note, oct2)
					orig = measure_sharps_flats.get(note_oct2, 0)
					measure_sharps_flats[note_oct2] = orig + 1
			if a[x-1] == '=':
				for oct2 in range(9):
					note_oct2 = "%s%u" % (note, oct2)
					measure_sharps_flats[note_oct2] = 0
			continue
		if note and a[x].isdigit():
			leng = float(unit) / float(a[x])
			continue
		if note and a[x] == '/':
			try: fac = float(a[x-1]) / float(a[x+1])
			except: fac = .5
			leng = float(unit) / fac
		if note and a[x].isalpha() or a[x] == '[':
			break

	if note:
		if triplet:
			leng *= tripfac
			triplet -= 1
		if note[0].lower() == 'z':
			note = 'r'
			song += [["%s" % note, leng]]
			if not only_first:
				second_ver += [["%s" % note, leng]]
		else:
			corr_note = piano[piano.index(note_oct) + measure_sharps_flats.get(note_oct, 0)]
			corr_note = "%s%s" % (corr_note, firstnote)
			if tie_next == 1:
				if corr_note == song[-1][0]:
					song[-1][1] = 1. / (1./song[-1][1] + 1. / leng)
					try:
						second_ver[-1][1] = song[-1][1]
					except: pass
				tie_next = 0
			else:
				song += [[corr_note, leng]]
				if not only_first:
					second_ver += [[corr_note, leng]]
				if next_half:
					leng = 1. / song[-1][1]
					song[-1][1] = 1. / (.5 * leng)
					next_half = False
				if tie_next == 2: tie_next = 1
		return x
	else: return 0

def parse_line(a):
	global chord
	n = 0
	while n < len(a):
		n = add_note(a, n)
		if chord:
			for n2 in range(n, len(a)):
				if a[n2] == ']':
					n = n2
					chord = False
					break
		if not n: break

def mk_triptab(m):
	if int(m.split('/')[0]) % 2:
		n = 3
	else:
		n = 2
	return {2: 2./3., 3: 1.5, 4: 4./3., 5: 5./n, 6: 3., 7: 7./n, 8: 8./3., 9: 9./n}

def get_bpm(s, u = "1/4"):
	if '=' not in s:
		c, d = u.split('/')
		return int(s) * 4. * float(c) / float(d)
	else:
		a, b = s.split('=')
		c, d = a.split('/')
		return int(b) * 4. * float(c) / float(d)

fn = sys.argv[1]
if fn[:5] == 'http:':
	f = urllib2.urlopen(fn)
else:
	f = open(fn)

bpm     = 120
meter   = "4/4"
triptab = None
nunit   = "1/4"
unit    = 4

for l in f:
	if l[0] in ('w', 'W', '%'): continue
	if 'X:' in l:
		sn = int(l.split(':')[1])
		if sn == num:
			sel = True
	if 'L:' in l and sel:
		nunit = l.split(':')[1].strip()
		unit = int(l.split('/')[1])
	if 'M:' in l and sel:
		meter = l.split(':')[1].strip()
		if meter == 'C': meter = "4/4"
	if 'Q:' in l and sel:
		bpm = get_bpm(l.split(':')[1].strip(), nunit)
	if 'K:' in l and sel:
		key = l.split(':')[1].strip().replace('maj', '').replace('min', 'm')
		global_sharps_flats = {}
		fsnum = 0
		for x, y, z in key_sigs:
			if x.lower() == key.lower() or y.lower() == key.lower():
				fsnum = z
		if fsnum < 0:
			fsrange = range(fsnum, 0)
			sign = -1
			piano = piano_f
		else:
			fsrange = range(1, fsnum + 1)
			sign = 1
			piano = piano_s
		for fs in fsrange:
			for oct in range(9):
				global_sharps_flats['%s%u' % (flats_and_sharps[fs], oct)] = sign
		#print global_sharps_flats
		measure_sharps_flats = global_sharps_flats.copy()
	if l.strip() == '' and sel:
		break
	if sel and not (l[0].isalpha() and l[1] == ':'):
		if not triptab: triptab = mk_triptab(meter)
		l2 = simp_line(list(l))
		parse_line(l2)

if do_repeat:
	song = song + second_ver
f.close()

if not sel:
	print
	print "*** Song %u not found in file %s!" % (num, fn)
	print
else:
	print key, unit
	print song
	print
	print len(song)

	pysynth.make_wav(song, bpm = bpm)

