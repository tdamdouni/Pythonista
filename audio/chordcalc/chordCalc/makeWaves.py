
#makeWaves
"""
This script builds a dictionary of simple plucked note wave files.

written by Steven Pollack (c) September 27, 2014

"""


#Frequency table


Freq_table = """0   16.35   17.32   18.35   19.45   20.60   21.83   23.12   24.50   25.96   27.50   29.14   30.87
1   32.70   34.65   36.71   38.89   41.20   43.65   46.25   49.00   51.91   55.00   58.27   61.74
2   65.41   69.30   73.42   77.78   82.41   87.31   92.50   98.00   103.8   110.0   116.5   123.5
3   130.8   138.6   146.8   155.6   164.8   174.6   185.0   196.0   207.7   220.0   233.1   246.9
4   261.6   277.2   293.7   311.1   329.6   349.2   370.0   392.0   415.3   440.0   466.2   493.9
5   523.3   554.4   587.3   622.3   659.3   698.5   740.0   784.0   830.6   880.0   932.3   987.8
6   1047    1109    1175    1245    1319    1397    1480    1568    1661    1760    1865    1976
7   2093    2217    2349    2489    2637    2794    2960    3136    3322    3520    3729    3951
8   4186    4435    4699    4978    5274    5588    5920    6272    6645    7040    7459    7902"""

note_name= "C Cs D Ds E F Fs G Gs A As B".split()

freq_list = Freq_table.split()
freq_array = []
for octave in range(9):
	this_octave = freq_list[0:13]
	freq_list = freq_list[13:]
	freq_array.append([float(x) for x in this_octave[1:]])



"""Some Specific Notes

Middle C (C4) is C4=261.6Hz

Standard tuning fork A is A4=440Hz

Piano range is A0=27.50Hz to C8=4186Hz

Guitar strings are E2=82.41Hz, A2=110Hz, D3=146.8Hz, G3=196Hz, B3=246.9Hz, E4=329.6Hz

Bass strings are (5th string) B0=30.87Hz, (4th string) E1=41.20Hz, A1=55Hz, D2=73.42Hz, G2=98Hz

Mandolin & violin strings are G3=196Hz, D4=293.7Hz, A4=440Hz, E5=659.3Hz

Viola & tenor banjo strings are C3=130.8Hz, G3=196Hz, D4=293.7Hz, A4=440Hz

Cello strings are C2=65.41Hz, G2=98Hz, D3=146.8Hz, A3=220Hz

"""""

# generate wav file containing sine waves
import math, wave, os, os.path, console, sys, glob
from numpy import linspace,int16, array
import numpy as np

class Envelope():
	def __init__(self,numSamples, attack=20,decay=80):
		self.numSamples = numSamples
		self.attack = attack
		self.decay = decay
		self.last_sample = 0;
		self._normalize()
		self.tAttack = int(float(numSamples)*(float(self.attack)/100))
		self.tDecay = numSamples - self.tAttack
		self.rateAttack = 1.0/self.tAttack
		self.rateDecay = 1.0/self.tDecay

	def _normalize(self): #internal function to normalize the various times to total to 100
		sum = self.attack + self.decay
		self.attack *= 100.0/sum
		self.decay *= 100.0/sum

	def __call__(self,t):
		env=t*self.rateAttack*(t<=self.tAttack)+(1.0-(t-self.tAttack)*self.rateDecay)*(t>self.tAttack)
		env.clip(0.0,1.0)
		return env


if os.path.exists('waves'):
	response = console.alert('', 'DIRECTORY EXISTS. OVERWRITE?', 'yes','no')
	if response == 2:
		sys.exit()
	else:
		files = glob.glob('waves/*')
		for f in files:
			os.remove(f)
		os.rmdir('waves')
		os.mkdir('waves')
else:
	os.mkdir('waves')
	
sampleRate = 221000 # of samples per second (standard)
numChan = 1 # of channels (1: mono, 2: stereo)
dataSize = 2 # 2 bytes because of using signed short integers => bit depth = 16
duration = 1.0 # seconds
volume = 100 # percent
numSamples = int(sampleRate * duration)

t=linspace(0,duration*sampleRate,numSamples)
envelope = Envelope(numSamples)(t)
print len(envelope)

for octave in range(8):
	for note in range(12):
		freq = freq_array[octave][note]
		numSamplesPerCyc = (sampleRate / freq)

		# note and its 1st 2 harmonics
		signal = np.zeros_like(t)
		relative = [1.0,0.4,0.04,0.01,0.01,0.01,0.01,0.01]
		sum = 0
		for term in relative: sum += term
		relative = [x/sum for x in relative]
		for harmonic in range(len(relative)):
			signal += relative[harmonic]*np.sin(np.pi * 2 * ((harmonic+1)*t / numSamplesPerCyc))

		sample = signal * envelope
		max = abs(np.amax(sample))
		min = abs(np.amin(sample))
		if max > min:
			sample = sample * 32767 / max
		else:
			sample = sample * 32767 / min			
		data = sample.astype(int16)

	
		fname = 'waves/{0}_{1}.wav'.format(note_name[note],octave)
		f = wave.open(fname, 'w')
		f.setparams((numChan, dataSize, sampleRate, numSamples, "NONE", "Uncompressed"))
		f.writeframes(data.tostring())
		f.close()
		print "wrote {}".format(fname)
		
		








