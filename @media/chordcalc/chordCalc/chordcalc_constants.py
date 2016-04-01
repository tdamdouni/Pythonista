#chord_calc

#Constants


# Note numbers - add multiples of 12 for higher octaves

NOTE_C = 0
NOTE_Cs = NOTE_Db = 1
NOTE_D = 2
NOTE_Ds = NOTE_Eb = 3
NOTE_E = 4
NOTE_F = 5
NOTE_Fs = NOTE_Gb = 6
NOTE_G = 7
NOTE_Gs = NOTE_Ab = 8
NOTE_A = 9
NOTE_As = NOTE_Bb = 10
NOTE_B = 11

NOTE_NAMES = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
NOTE_FILE_NAMES = ['C_', 'Cs_','D_', 'Ds_','E_','F_','Fs_','G_','Gs_','A_','As_','B_']



NOTES = {
	'C': NOTE_C,
	'C#': NOTE_Cs,
	'Db': NOTE_Db,
	'D': NOTE_D,
	'D#': NOTE_Ds,
	'Eb': NOTE_Eb,
	'E': NOTE_E,
	'F': NOTE_F,
	'F#': NOTE_Fs,
	'Gb': NOTE_Gb,
	'G': NOTE_G,
	'G#': NOTE_Gs,
	'Ab': NOTE_Ab,
	'A': NOTE_A,
	'A#': NOTE_As,
	'Bb': NOTE_Bb,
	'B': NOTE_B,
	}
	
#noteTemp = sorted( NOTES.items())
ROOT_LIST_CLEAN = [{'title':root, 'noteValue':note, 'accessory_type': 'none'} for root, note in sorted(NOTES.items())]
#del noteTemp


SCALENOTES = ['R','b2','2','b3','3','4','b5','5','#5','6','b7','7','R','b9','9','#9','3','11','#11','5','b13','13']

# Chordtype definitions
# These are guitar-centric

CHORDTYPE = [
	('maj', (0,4,7)),
	('min', (0,3,7)),
	('dim', (0,3,6)), # note, not dim7
	('aug', (0,4,8)),
	('M7', (0,4,7,11)),
	('m7', (0,3,7,10)),
	('7', (0,4,7,10)),
	('m7b5', (0,3,6,10)), # half dim
	('dim7', (0,3,6,9)),
	('6', (0,4,7,9)),
	('9', (0,4,7,10,14)),
	('sus2', (0,2,7)),
	('sus4', (0,5,7)),
	('omit3',(0,7)),
	('#5', (0,4,8)),
	('(b5)', (0,4,6)),
	('+', (0,4,8)),
	('+7', (0,4,8,10)),
	('+7b9#11', (0,4,8,10,13,18)),
	('+9', (0,4,8,10,14)),
	('+9M7', (0,4,8,11,14)),
	('+M7', (0,4,8,11)),
	('11', (0,7,10,14,17)), # no 3rd
	('11b9', (0,4,7,10,13,17)),
	('13', (0,4,7,10,21)), # no 9th and 11th
	('13#11', (0,4,7,10,18,21)), # no 9th
	('13#9', (0,4,7,10,15,21)), # no 11th
	('13b5', (0,4,6,10,21)), # no 9th and 11th
	('13b9', (0,4,7,10,13,21)), # no 11th
	('13sus', (0,5,7,10,14,21)),
	('13susb9', (0,5,7,10,13,21)),
	('5', (0,7)),

	('6(add9)', (0,4,7,9,14)),
	('69', (0,4,7,9,14)),
	('6/9', (0,4,7,9,14)),

	('7#11', (0,4,7,10,18)), # no 9th
	('7#5', (0,4,8,10)),
	('7#5#9', (0,4,8,10,15)),
	('7#5b9', (0,4,8,10,13)),
	('7#9', (0,4,7,10,15)),
	('7#9#11', (0,4,7,10,15,18)),
	('7#9b13', (0,4,7,10,15,20)),
	('7(omit3)', (0,7,10)),
	('7+', (0,4,8,10)),
	('7+5', (0,4,8,10)),
	('7+9', (0,4,7,10,15)),
	('7-5', (0,4,6,10)),
	('7-9', (0,4,7,10,13)),
	('7alt', (0,4,6,10,13)),
	('7b5', (0,4,6,10)),
	('7b5#9', (0,4,6,10,15)),
	('7b5b9', (0,4,6,10,13)),
	('7b9', (0,4,7,10,13)),
	('7b9#11', (0,4,7,10,13,18)),
	('7sus', (0,5,7,10)),
	('7sus2', (0,2,7,10)),
	('7sus4', (0,5,7,10)),
	('7susb9', (0,5,7,10,13)),

	('9#11', (0,4,7,10,14,18)),
	('9#5', (0,4,8,10,14)),
	('9+5', (0,4,8,10,14)),
	('9-5', (0,4,6,10,14)),
	('9b5', (0,4,6,10,14)),
	('9sus', (0,5,7,10,14)),
	('9sus4', (0,5,7,10,14)),
	('M13', (0,4,7,11,21)), # no 9th and 11th
	('M13#11', (0,4,7,11,18,21)), # no 9th
	('M6', (0,4,7,9)),

	('M7#11', (0,4,7,11,18)), # no 9th
	('M7#5', (0,4,8,11)),
	('M7(add13)', (0,4,7,10,13,21)), # no 11th
	('M7+5', (0,4,8,11)),
	('M7-5', (0,4,6,11)),
	('M7b5', (0,4,6,11)),
	('M9', (0,4,7,11,14)),
	('M9#11', (0,4,7,11,14,18)),
	('add9', (0,4,7,14)),

	('aug7', (0,4,8,10)),
	('aug7#9', (0,4,8,10,15)),
	('aug7b9', (0,4,8,10,13)),
	('aug9', (0,4,8,10,14)),
	('aug9M7', (0,4,8,11,14)),


	('dim7(addM7)', (0,3,6,11)),
	('m', (0,3,7)),
	('m#5', (0,3,8)),
	('m#7', (0,3,7,11)),
	('m(add9)', (0,3,7,14)),
	('m(b5)', (0,3,6)),
	('m(maj7)', (0,3,7,11)),
	('m(sus9)', (0,3,7,14)),
	('m+5', (0,3,8)),
	('m+7', (0,3,7,11)),
	('m+7#9', (0,3,7,10,15)),
	('m+7b9', (0,3,7,10,13)),
	('m+7b9#11', (0,3,7,10,13,18)),
	('m11', (0,3,7,10,14,17)),
	('m11b5', (0,3,6,10,17)),
	('m13', (0,3,7,10,21)), # no 9th and 11th
	('m6', (0,3,7,9)),
	('m6(add9)', (0,3,7,9,14)),
	('m69', (0,3,7,9,14)),
	('m6/9', (0,3,7,9,14)),

	('m7#9', (0,3,7,10,15)),
	('m7(#9)', (0,3,7,10,15)),
	('m7(add11)', (0,3,7,10,17)),
	('m7(add13)', (0,3,7,10,21)),
	('m7(b9)', (0,3,7,10,13)),
	('m7(omit5)', (0,3,10)),
	('m7-5', (0,3,6,10)), # half dim
	('m7b5b9', (0,3,6,10,13)),
	('m7b9', (0,3,7,10,13)),
	('m7b9#11', (0,3,7,10,13,18)),
	('m7omit5', (0,3,10)),
	('m9', (0,3,7,10,14)),
	('m9#11', (0,3,7,10,14,18)),
	('mM7', (0,3,7,11)),
	('mM7(add9)', (0,3,7,11,14)),
	('maj13', (0,4,7,11,21)), # no 9th and 11th
	('maj7', (0,4,7,11)),
	('maj9', (0,4,7,11,14)),
	('mb5', (0,3,6)),
	('min#7', (0,3,7,11)),
	('min(maj7)', (0,3,7,11)),
	('omit3(add9)', (0,7,14)),
	('omit3add9', (0,7,14)),


	('sus', (0,5,7)),
	('sus9', (0,5,7,10,14)),
	]


CHORD_LIST_CLEAN = [{'title':chord, 'fingering':fingering, 'accessory_type':'none'} for chord,fingering in CHORDTYPE]

SCALETYPE =[ #  T = Whole, S = Semitone, # = number of semitones 
						('Major',  						'TTSTTTS'),
						('Minor',  						'TSTTTTS'),
						('Dorian', 						'TSTTTST'),
						('Phrygian',					'STTTSTT'),
						('Lydian',						'TTTSTTS'),
						('Mixolydian', 				'TTSTTST'),
						('Aoelian',						'TSTTSTT'),
						('Locrian',						'STTSTTT'),
						('Blues Major', 			'TSS3T3'),
						('Blues Minor', 			'3TSS3T'),
						('Penta Major', 			'TT3T3'),
						('Penta Minor', 			'3TT3T'),
						('Harm Minor', 				'TSTTS3S'),
						('Melod Minor', 			'TSTTTTS'),
						('Whole Tone',				'TTTTTT'),
						('Dimin (WH)',				'TSTSTST'),
						('Bebop Major',				'TTSTTSSS')					
					]
					
TRUE_ROOT = {						
             	'Dorian': 		2, # second scale degree
             	'Phrygian':		4, # third scale degree
             	'Lydian':			5, # fourth scale degree
             	'Mixolydian':	7, # fifth scale degree
							'Aoelian': 		9, # sixth scale degree
							'Locrian':		11, # seventh scale degree						
						}
					
CIRCLE_OF_FIFTHS = {"C":0,
                    "G":1,
                    'D':2,
                    'A':3,
                    'E':4,
                    'B':5,
                    'F#':6,
                    'C#':7,
                    'G#':8,
                    'F':-1,
                    'Bb':-2,
                    'Eb':-3,
                    'Ab':-4,
                    'Db':-5,
                    'Gb':-6,
                    'Cb':-7,
                    'Fb':-8
                    }


					
SCALE_LIST_CLEAN = [{'title': scale, 'scaleintervals': intervals, 'accessory_type':'none'} for scale,intervals in SCALETYPE]

# Tunings and their corresponding default spans
# Instruments I don't play has default span = 3
# I only care about the relative pitches of the open strings against the lowest bass note
# But actually the pitches are currently not used in any way

SPAN_DEFAULT_UNKNOWN = 3
SPAN_DEFAULT_GUITAR = 4
SPAN_DEFAULT_BASS = 3
SPAN_DEFAULT_UKULELE = 5
SPAN_DEFAULT_MANDOLIN = 7

TUNINGS = [
	# Guitar
	('GUITAR', [[NOTE_E, NOTE_A, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('MANDOLIN', [[NOTE_G, NOTE_D+12, NOTE_A+12, NOTE_E+24], SPAN_DEFAULT_MANDOLIN],3),
	('BOUZOUKI (Celtic)', [[NOTE_G, NOTE_D+12, NOTE_A+12, NOTE_D+24], SPAN_DEFAULT_MANDOLIN],2),
	('4 STRING GUITAR OPEN G', [[NOTE_G, NOTE_D+12, NOTE_G+12, NOTE_B+12], SPAN_DEFAULT_GUITAR],2),
	('UKULELE', [[NOTE_G+12, NOTE_C, NOTE_E, NOTE_A], SPAN_DEFAULT_UKULELE],3),
	('UKULELE Low G', [[NOTE_G, NOTE_C, NOTE_E, NOTE_A], SPAN_DEFAULT_UKULELE],3),
	('3 String OPEN G', [[NOTE_G, NOTE_D, NOTE_G+12], SPAN_DEFAULT_GUITAR],2),
	('3 String OPEN D', [[NOTE_D, NOTE_Fs, NOTE_A], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_DROPD', [[NOTE_D, NOTE_A, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_DROPDG', [[NOTE_D, NOTE_G, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_G', [[NOTE_D, NOTE_G, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_DADGAD', [[NOTE_D, NOTE_A, NOTE_D+12, NOTE_G+12, NOTE_A+12, NOTE_D+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_LUTE', [[NOTE_E, NOTE_A, NOTE_D+12, NOTE_Fs+12, NOTE_B+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_OPEN_A', [[NOTE_E, NOTE_A, NOTE_E+12, NOTE_A+12, NOTE_Cs+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_OPEN_C', [[NOTE_C, NOTE_G, NOTE_C+12, NOTE_E+12, NOTE_G+12, NOTE_C+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_OPEN_D', [[NOTE_D, NOTE_A, NOTE_D+12, NOTE_Fs+12, NOTE_A+12, NOTE_D+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_OPEN_Db', [[NOTE_Db, NOTE_Ab, NOTE_Db+12, NOTE_F+12, NOTE_Ab+12, NOTE_Db+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_OPEN_E', [[NOTE_E, NOTE_B, NOTE_E+12, NOTE_Gs+12, NOTE_A+12, NOTE_C+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_OPEN_F', [[NOTE_C, NOTE_F, NOTE_C+12, NOTE_F+12, NOTE_A+12, NOTE_C+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_OPEN_G', [[NOTE_D, NOTE_G, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_D+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_BIG_D', [[NOTE_D, NOTE_A, NOTE_D+12, NOTE_Fs+12, NOTE_A+12, NOTE_A+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_Bm7', [[NOTE_D, NOTE_A, NOTE_D+12, NOTE_Fs+12, NOTE_B+12, NOTE_D+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_Am', [[NOTE_C, NOTE_G, NOTE_C+12, NOTE_G+12, NOTE_A+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_DOBRO', [[NOTE_G, NOTE_B, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_D+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_EM7', [[NOTE_E, NOTE_B, NOTE_E+12, NOTE_Gs+12, NOTE_B+12, NOTE_Ds+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_HAWAIIAN1', [[NOTE_C, NOTE_G, NOTE_E+12, NOTE_G+12, NOTE_A+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_HAWAIIAN2', [[NOTE_C, NOTE_G, NOTE_C+12, NOTE_G+12, NOTE_A+12, NOTE_D+24], SPAN_DEFAULT_GUITAR],2),

	('GUITAR_SLACK_C', [[NOTE_C, NOTE_G, NOTE_C+12, NOTE_E+12, NOTE_A+12, NOTE_C+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_WAHINE1', [[NOTE_C, NOTE_G, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_D+24], SPAN_DEFAULT_GUITAR],2),
	('GUITAR_WAHINE2', [[NOTE_D, NOTE_A, NOTE_D+12, NOTE_Fs+12, NOTE_A+12, NOTE_Cs+24], SPAN_DEFAULT_GUITAR],2),
	# Bass
	('BASS', [[NOTE_E, NOTE_A, NOTE_D+12, NOTE_G+12], SPAN_DEFAULT_BASS],0),
	# Ukulele

	('UKULELE_C', [[NOTE_G, NOTE_C, NOTE_E, NOTE_A], SPAN_DEFAULT_UKULELE],3),
	('UKULELE_D', [[NOTE_A, NOTE_D, NOTE_Fs, NOTE_B], SPAN_DEFAULT_UKULELE],3),
	('UKULELE_BARITONE', [[NOTE_D, NOTE_G, NOTE_B, NOTE_E+12], SPAN_DEFAULT_GUITAR],3),
	# Mandolin

	('MANDOCELLO', [[NOTE_C, NOTE_G, NOTE_D+12, NOTE_A+12], SPAN_DEFAULT_UNKNOWN],2),
	('MANDOLA', [[NOTE_C, NOTE_G, NOTE_D+12, NOTE_A+12], SPAN_DEFAULT_UNKNOWN],2),
	# Bouzouki
	('BOUZOUKI', [[NOTE_C, NOTE_F, NOTE_A, NOTE_D+12], SPAN_DEFAULT_UNKNOWN],2),
	# Banjo
	('BANJO', [[NOTE_C, NOTE_G, NOTE_B, NOTE_D+12], SPAN_DEFAULT_UNKNOWN],2),
	('BANJO_CGBD', [[NOTE_C, NOTE_G, NOTE_B, NOTE_D+12], SPAN_DEFAULT_UNKNOWN],2),
	('BANJO_DGBD', [[NOTE_D, NOTE_G, NOTE_B, NOTE_D+12], SPAN_DEFAULT_UNKNOWN],2),
	('BANJO_CGDA', [[NOTE_C, NOTE_G, NOTE_D+12, NOTE_A+12], SPAN_DEFAULT_UNKNOWN],2),
	('BANJO_CGCD', [[NOTE_C, NOTE_G, NOTE_C+12, NOTE_D+12], SPAN_DEFAULT_UNKNOWN],2),
	# Balalaika
	('BALALAIKA', [[NOTE_E, NOTE_E, NOTE_A], SPAN_DEFAULT_UNKNOWN],2),
	# Charango
	('CHARANGO', [[NOTE_G, NOTE_C+12, NOTE_E+12, NOTE_A, NOTE_E+12], SPAN_DEFAULT_UNKNOWN],2),
	# Vihuela (da mano)
	('VIHUELA', [[NOTE_G, NOTE_C+12, NOTE_F+12, NOTE_A+12, NOTE_D+24, NOTE_G+24], SPAN_DEFAULT_GUITAR],2),
	('VIHUELA_C', [[NOTE_C, NOTE_F, NOTE_Bb+12, NOTE_D+12, NOTE_G+12, NOTE_C+24], SPAN_DEFAULT_GUITAR],2),
	# Others
	('BAROQUE_GUITAR', [[NOTE_A, NOTE_D+12, NOTE_G+12, NOTE_B+12, NOTE_E+24], SPAN_DEFAULT_GUITAR],2),
	('VIHUELA_MEXICANA', [[NOTE_A+12, NOTE_D+24, NOTE_G+24, NOTE_B+12, NOTE_E+24], SPAN_DEFAULT_UNKNOWN],2)
]


TUNING_LIST_CLEAN = [{'title':type, 'notes':ns[0], 'span':ns[1], 'octave':oct,'accessory_type':'none'} 
for type,ns,oct in TUNINGS]
	



FILTER_LIST_CLEAN = [
	{'title':'FULL_CHORD', 'desc':"R, 3rd and 5th must be present",'accessory_type':'none'},
	{'title':'NOROOT_OK', 'desc':"Can omit root",'accessory_type':'none'},
	{'title':'NO3RD_OK', 'desc':"Can omit 3rd",'accessory_type':'none'},
	{'title':'NO5TH_OK', 'desc':"Can omit 5th",'accessory_type':'none'},
	{'title':'NO_OPEN', 'desc': "No open string fingerings",'accessory_type':'none'},
	{'title':'NO_DEAD', 'desc': 'No dead strings','accessory_type': 'none'},
	{'title':'NO_WIDOW', 
	 'desc':'No dead strings in middle unless next to outside dead string','accessory_type':'none'}
	]
	
GUITAR_LIST_CLEAN = [
	{'title':'LOW_4', 'desc': 'Lower four strings', 'accessory_type':'none'},
	{'title':'HIGH_4', 'desc': 'High four strings', 'accessory_type':'none'}
	]

MANDOLIN_LIST_CLEAN = [
	{'title':'LOW_3', 'desc': 'Lower three strings', 'accessory_type':'none'},
	{'title':'HIGH_3', 'desc':'Upper thrree strings', 'accessory_type':'none'},
	{'title': 'DOUBLE_STOPS', 'desc': 'Double stops only', 'accessory_type': 'none'}
	]
	
FILTER_MUTUAL_EXCLUSION_LIST ={
                         'FULL_CHORD': "NOROOT_OK NO3RD_OK NO5TH_OK AUTO_REDUCE DOUBLE_STOPS".split(),
                         'NOROOT_OK': ['FULL_CHORD'],
                         'NO3RD_OK': ['FULL_CHORD'],
                         'NO5TH_OK': ['FULL_CHORD'],
                         'DOUBLE_STOPS': ['FULL_CHORD'],
                         'LOW_4': ['HIGH_4'],
                         'HIGH_4':['LOW_4'],
                         'HIGH_3': ['LOW_3'],
                         'LOW_3': ['HIGH_3']
                         }
	
