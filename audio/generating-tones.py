# coding: utf-8

# https://forum.omz-software.com/topic/918/generating-tones-and-pitches-ie-square-sine-in-x-hz-gps-lat-long

`function_name_here()`

#==============================

# generate wav file containing sine waves
import math, wave, array
duration = 3 # seconds
freq = 440 # of cycles per second (Hz) (frequency of the sine waves)
volume = 100 # percent
data = array.array('h') # signed short integer (-32768 to 32767) data
sampleRate = 44100.0 # of samples per second (standard)
numChan = 1 # of channels (1: mono, 2: stereo)
dataSize = 2 # 2 bytes because of using signed short integers => bit depth = 16
numSamplesPerCyc = (sampleRate / freq)
numSamples = int(sampleRate * duration)
for i in range(numSamples):
    sample = 32767 * float(volume) / 100
    sample *= math.sin(math.pi * 2 * (i / numSamplesPerCyc))
    data.append(int(sample))
f = wave.open('440hz.wav', 'w')
f.setparams((numChan, dataSize, sampleRate, numSamples, "NONE", "Uncompressed"))
f.writeframes(data.tostring())
f.close()
import sound
sound.play_effect('440hz.wav')

#==============================

# ...
import sound
player = sound.Player('440hz.wav')
player.play()

#==============================

import numpy as np

th=np.linspace(0, 2*np.pi*freq*duration, numSamples, endpoint=False)
data = (32767*volume/100.0*np.sin(th)).astype(np.int16)
