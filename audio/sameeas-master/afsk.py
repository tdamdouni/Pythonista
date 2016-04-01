from audioroutines import *

def generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel, numCh,
	                stringData):
    "Generate a string of binary data of AFSK audio"

    pcm_data = ''
    bitstream = ''
    bitduration = 1.0 / bitrate
    print stringData
    for byte in stringData:
	bytebits = "{0:08b}".format( ord(byte))
	bitstream += bytebits[::-1]
	#bitstream += bytebits
    #print bitstream
    one_bit = generateSimplePCMToneData(markF, markF, sampRate, bitduration, sampWidth,
		           peakLevel, numCh)
    zero_bit = generateSimplePCMToneData(spaceF, spaceF, sampRate, bitduration, sampWidth,
			   peakLevel, numCh)
    for bit in bitstream:
	if bit == '1':
	    pcm_data += one_bit
	else:
	    pcm_data += zero_bit

    return pcm_data
