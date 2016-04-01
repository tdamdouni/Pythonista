import logging
import math
import struct 
import wave

LOG = logging.getLogger("pysynth_beeper")
SAMPLING_RATE = 44100

PITCHHZ = {}
keys_s = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
for k in range(88):
    freq = 27.5 * 2. ** (k / 12.)
    oct = (k + 9) // 12
    note = '%s%u' % (keys_s[k % 12], oct)
    PITCHHZ[note] = freq

def make_wav(song, tempo=120, transpose=0, fn="out.wav"):
    f = wave.open(fn, 'w')

    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLING_RATE)
    f.setcomptype('NONE', 'Not Compressed')

    # Define a waveform that looks something like this
    # \        /
    #__\_____ /__
    #   \  /\/        
    #    \/
    
    # Format:  [(start, end, start_level, end_level), ...]        
    waveform = [(0.0, 0.3,  1.0, -1.0), 
                (0.3, 0.5, -1.0,  0.0), 
                (0.5, 0.6,  0.0, -0.5), 
                (0.6, 1.0, -0.5,  1.0)]

    # BPM is "quarter notes per minute"
    full_notes_per_second = float(tempo) / 60 / 4 
    full_note_in_samples = SAMPLING_RATE / full_notes_per_second

    def sixteenbit(sample):
        return struct.pack('h', round(32000 * sample))

    
    def beep_single_period(period):
        asin = lambda x: math.sin(2. * math.pi * x)
        
        period_waveform = []
        for x in xrange(period):
            # Position inside current period, 0..1            
            pos = float(x) / period
            
            # Synth 1, using sine waves
            level1 = (asin(pos) + asin(pos * 2)) / 2
            
            # Synth 2, discrete, using waveform definition
            for start, finish, start_level, finish_level in waveform:
                if pos >= start and pos <= finish:
                    localpos = (pos - start) / (finish - start)
                    level2 = (finish_level - start_level) * localpos + start_level
                    break
            
            # Put both samples together, apply fadein/fadeout
            level = (level1 + level2) / 2
            period_waveform.append(level)
            #period_waveform_packed.append(sixteenbit(level))    
    
        return period_waveform, "".join(sixteenbit(l) for l in period_waveform)
    
    def beep(freq, duration, sink):
        ow = ""

        period = int(SAMPLING_RATE / 4 / freq)
        period_waveform, period_waveform_packed = beep_single_period(period)

        x = 0 
        while x < duration:
            if x < 100 or duration - x < 100:
                # At borders we do fade in and fade out
                fade_multiplier = min(x, duration - x) / 100.0
                ow += sixteenbit(period_waveform[x % period] * fade_multiplier)
                x += 1
            else:
                if x % period == 0:
                    # Optimization:
                    # We're aligned with waveform, can fill ow in batches!
                    while x + period + 100 < duration:
                        ow += period_waveform_packed
                        x += period

                # Go sample-by-sample
                ow += sixteenbit(period_waveform[x % period])
                x += 1

        sink.writeframesraw(ow)

    def silence(duration, sink):
        sink.writeframesraw(sixteenbit(0) * int(duration))

    for note_pitch, note_duration in song:
        # note_duration is 1, 2, 4, 8, ... and actually means 1, 1/2, 1/4, ...
        duration = int(full_note_in_samples / note_duration) 
        
        if note_pitch == "r":
            LOG.debug("Silence for %d samples" % duration)
            silence(duration, f)
        else:
            freq = PITCHHZ[note_pitch]
            freq *= 2 ** transpose
            LOG.debug("%d Hz for %d samples" % (freq, duration))
            beep(freq, duration, f)

    f.close()
