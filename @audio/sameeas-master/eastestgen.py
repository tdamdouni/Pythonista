from afsk import *

eastestgen_core_version = "1.1"

def generateEASpcmData(org, event, fips, eventDuration, timestamp, stationId, sampRate, sampWidth, 
	                peakLevel, numCh, msgaudio=None, customMsg=None):
    "Put together info to generate an EAS message"

    markF = 2083.3
    spaceF = 1562.5
    bitrate = 520.5
    pcm_data = ''

    preamble = '\xab' * 16
    if customMsg is not None:
	message = 'ZCZC-' + customMsg
    else:
	message = 'ZCZC-{0}-{1}-{2}+{3}-{4}-{5: <8}-'.format(org, event, "-".join(fips[0:31]), 
		    eventDuration, timestamp, stationId[0:8])
    endOfMessage = 'NNNN'
    header = generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel,
	                 numCh, preamble + message.upper())
    eom = generateAFSKpcmData(markF, spaceF, bitrate, sampRate, sampWidth, peakLevel,
	                 numCh, preamble + endOfMessage)
    silence = generateSimplePCMToneData(10000, 10000, sampRate, 1, sampWidth, -94, numCh)
    
    pcm_data = silence + silence

    for i in range(3):
	pcm_data = pcm_data + header + silence
    if msgaudio is not None:
	attn_tones = generateDualTonePCMData(853, 960, sampRate, 8, sampWidth, peakLevel, numCh)
	pcm_data = pcm_data + silence + attn_tones + silence + msgaudio + silence
    for i in range(3):
	pcm_data = pcm_data + eom + silence

    return pcm_data

if __name__ == "__main__":
    import wave, time

    sampRate = 44100
    duration = 10
    sampWidth = 16
    peakLevel = -10
    numCh = 1
    now = time.gmtime()
    timestamp = time.strftime('%j%H%M', now) 

    data = generateEASpcmData('EAS', 'RWT', '029077', '0030', timestamp, 'KXYZ/FM', sampRate, 
	    sampWidth, peakLevel, numCh)
    data = recursiveFilterPCMaudio(4000, sampRate, sampWidth, numCh, data)
    file = wave.open('testfile-filt.wav', 'wb')
    file.setparams( (numCh, sampWidth/8 , sampRate, duration * sampRate, 'NONE', '') )
    file.writeframes(data)
    file.close()

