import math, struct, random, array

pi = math.pi

def getFIRrectFilterCoeff(fc, sampRate, filterLen=20):
    'Calculate FIR lowpass filter weights using hamming window'
    'y(n) = w0 * x(n) + w1 * x(n-1) + ...'

    ft = float(fc) / sampRate
    #print ft
    m = float(filterLen - 1)

    weights = []
    for n in range(filterLen):
	try:
	    weight = math.sin( 2 * pi * ft * (n - (m / 2))) / (pi * (n - (m / 2)))
	    hamming = 0.54 - 0.46 * math.cos( 2 * pi * n / m)
	    weight = weight * hamming
	except:
	    weight = 2 * ft
	    hamming = 0.54 - 0.46 * math.cos( 2 * pi * n / m)
	    weight = weight * hamming
	    
	weights.append(weight)

    return weights

def filterPCMaudio(fc, sampRate, filterLen, sampWidth, numCh, data):
    'Run samples through a filter'

    samples = array.array('h', data)
    filtered = ""

    w = getFIRrectFilterCoeff(fc, sampRate, filterLen)

    for n in range(len(w), len(samples) - len(w)):
	acc = 0
	for i in range(len(w)):
	    acc += w[i] * samples[n - i]
	filtered += struct.pack('<h', int(math.floor(acc)))

    return filtered

def recursiveFilterPCMaudio(fc, sampRate, sampWidth, numCh, data):
    'Predefined filter values, Butterworth lowpass filter'
    
    a0 = 0.02008337 #0.01658193
    a1 = 0.04016673 #0.03316386
    a2 = a0
    b1 = -1.56101808 #-1.60413018
    b2 = 0.64135154 #0.67045791

    samples = array.array('h', data)
    filtered = data[0:2]
    y = [0, 0, 0]

    for n in range(2, len(samples) - 2):
	sample = (a0 * samples[n] + a1 * samples[n -1] + a2 * samples[n-2] -
		    b1 * y[1] - b2 * y[2])
	y[2] = y[1]
	y[1] = sample
	filtered += struct.pack('<h', int(math.floor(sample)))

    return filtered

def bpButterworthFilter6(fc, sampRate, sampWidth, numCh, data):
    a0 = 1
    a1 = -4.16740087e+00
    a2 = 9.56715918e+00
    a3 = -1.52777374e+01
    a4 = 1.88165959e+01
    a5 = -1.84592133e+01
    a6 = 1.46959044e+01
    a7 = -9.50055587e+00
    a8 = 4.97057565e+00
    a9 = -2.04987349e+00
    a10 = 6.42775774e-01
    a11 = -1.38591530e-01
    a12 = 1.72096260e-02
    b0 = 3.36990647e-03
    b1 = 0
    b2 = -2.02194388e-02
    b3 = 0
    b4 = 5.05485971e-02
    b5 = -2.15330343e-17
    b6 = -6.73981294e-02
    b7 = 2.15330343e-17
    b8 = 5.05485971e-02
    b9 = 0
    b10 = -2.02194388e-02
    b11 = 0
    b12 = 3.36990647e-03

    samples = array.array('h', data)
    print len(samples)
    filtered = data[0:12]
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for n in range(12, len(samples) - 12):
	sample = (a0 * samples[n] + a1 * samples[n -1] + a2 * samples[n-2] + a3 * samples[n-3] +
		  a4 * samples[n-4] + a5 * samples[n-5] + a6 * samples[n-6] + a7 * samples[n-7] + 
		  a8 * samples[n-8] + a9 * samples[n-9] + a10 * samples[n-10] + a11 * samples[n-11] + 
		  a12 * samples[n-12] -
		  b0 * y[0] - b1 * y[1] - b2 * y[2] - b3 * y[3] - b4 * y[4] - b5 * y[5] -
		  b6 * y[6] - b7 * y[7] - b8 * y[8] - b9 * y[9] - b10 * y[10] - b11 * y[11] -
		  b12 * y[12] )
	y[12] = y[11]
	y[11] = y[10]
	y[10] = y[9]
	y[9] = y[8]
	y[8] = y[7]
	y[7] = y[6]
	y[6] = y[5]
	y[5] = y[4]
	y[4] = y[3]
	y[3] = y[2]
	y[2] = y[1]
	y[1] = sample
	filtered += struct.pack('<h', int(math.floor(sample)))

    return filtered

def convertdbFStoInt( level, sampWidth):
    return math.pow(10, (float(level) / 20)) * 32767

def generateSimplePCMToneData(startfreq, endfreq, sampRate, duration, sampWidth, peakLevel, numCh):
    """Generate a string of binary data formatted as a PCM sample stream. Freq is in Hz,
    sampRate is in Samples per second, duration is in seconds, sampWidth is in bits, 
    peakLevel is in dBFS, and numCh is either 1 or 2."""

    phase = 0 * pi
    level = convertdbFStoInt(peakLevel, sampWidth)
    pcm_data = ''
    freq = startfreq
    slope = 0.5 * (endfreq - startfreq) / float(sampRate * duration)
    fade_len = int(0.001 * sampRate) * 0
    numSamples = int( round( sampRate * duration))

    #print duration * sampRate

    for i in range(0, numSamples):
	freq = slope * i + startfreq
	fade = 1.0
	if i < fade_len:
	    fade = 0.5 * (1 - math.cos(pi * i / (fade_len - 1)))
	elif i > (numSamples - fade_len):
	    fade = 0.5 * (1 - math.cos(pi * (numSamples - i) / (fade_len - 1))) 
	for ch in range(numCh):
	    sample =  int(( fade * level * math.sin(
	                   (freq * 2 * pi * i)/ sampRate + phase) ))
	    #print sample
	    pcm_data += struct.pack('<h', sample)

    return pcm_data

def generateDualTonePCMData(freq1, freq2, sampRate, duration, sampWidth, peakLevel, numCh):
    """Generate a string of binary data formatted as a PCM sample stream. Mix two freq
    together such as in alert tones or DTMF"""

    phase = 0 * pi
    level = convertdbFStoInt(peakLevel, sampWidth)
    pcm_data = ''
    fade_len = int(0.001 * sampRate) * 0
    numSamples = int( round( sampRate * duration))

    #print duration * sampRate

    for i in range(0, numSamples):
	fade = 1.0
	if i < fade_len:
	    fade = 0.5 * (1 - math.cos(pi * i / (fade_len - 1)))
	elif i > (numSamples - fade_len):
	    fade = 0.5 * (1 - math.cos(pi * (numSamples - i) / (fade_len - 1))) 
	for ch in range(numCh):
	    sample =  int(( fade * level * (0.5 * math.sin(
	                   (freq1 * 2 * pi * i)/ sampRate + phase) +
			   0.5 * math.sin((freq2 * 2 * pi * i)/ sampRate + phase) )))
	    #print sample
	    pcm_data += struct.pack('<h', sample)

    return pcm_data

def main():
    import wave

    numCh = 1
    peakLevel = -10
    sampWidth = 16
    sampRate = 44100

    
    file = wave.open('testchirp.wav', 'rb')
    samples = file.readframes( file.getnframes())
    file.close()
    #data = generateDualTonePCMData(853, 960, sampRate, 8, sampWidth, peakLevel, numCh)
    data = bpButterworthFilter6(0, sampRate, sampWidth, numCh, samples)
    fileout = wave.open( 'test.wav', 'wb')
    fileout.setparams( (numCh, sampWidth/8, sampRate, sampRate, 'NONE', '') )
    fileout.writeframes(data)
    fileout.close()

if __name__ == "__main__":
    main()
