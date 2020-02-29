# coding: utf-8

# http://scytale.name/files/2007/11/eurosignal.py

#!/usr/bin/env python

# eurosig.py -- generates a random or predefined Eurosignal as WAV file
# Written Feb 2005 by Gerhard Grimm <gerhard dot grimm at gmx dot net>
# Donated to the Public Domain. Have fun!

# Found in Nov 2007 by Tim Weber <http://scytale.name/> at
# http://forum.mysnip.de/read.php?8773,164803

from __future__ import print_function
import sys
from math import *
import struct
import random


class EurosignalEncoder:
    "Converts a sequence of 6-digit numbers to a Eurosignal PCM waveform"
    freq = [979.8, 903.1, 832.5, 767.4, 707.4, 652.0, 601.0, 554.0, 510.7, 470.8, 1062.9, 1153.1]
    duration = 0.1
    pause = [10, 11, 11, 11, 11, 11, 11, 11]

    def __init__(self, Rate, Load, Limit, NumFile, WavFile):

        "Initialize internal encoder state and set parameters"
        self.rate = Rate        # samples per second
        self.load = Load        # 0.0 .. 1.0
        self.limit = Limit      # how many numbers to produce
        self.count = 0
        self.numfile = NumFile  # text file with numbers, read in player mode,

                                # written in random generator mode
        self.wavfile = WavFile  # WAV file (PCM), always written
        self.phase = 0.0
        self.lastnum = self.pause
        self.lastcount = 0

    def EncodeDigit(self, Digit):

        "Encode a single digit to PCM. 10 = repetition, 11 = pause."
        pcm = ''
        samples = int(self.duration * self.rate)
        omega = 2 * pi * self.freq[Digit]
        for n in range(samples):
            t = n / float(self.rate)

            sample = 32000 * sin(omega * t + self.phase)
            pcm += struct.pack('<h', sample)
        endphase = samples / float(self.rate) * omega + self.phase
        self.phase = fmod(endphase, 2 * pi)
        return pcm


    def DigitSequence(self, Number):
        "Encode a number to a digit sequence, looking for repetitions."
        if len(Number) < 6:
            if self.lastcount == 3:
                self.lastnum = self.pause

            self.lastcount += 1
            return self.lastnum
        digits = []
        for i in range(6):
            digit = int(Number[i])
            if (i > 0) and (digits[-1] == digit):

                digit = 10
            digits += [digit]
        digits += [11, 11]
        self.lastnum = digits
        self.lastcount = 1
        return digits


    def WAVHeader(self):
        "Provide the WAV header for the selected sample rate, 16 bit, mono."
        return struct.pack('<4sL4s4sLHHLLHH4sL', 'RIFF', 36, 'WAVE', 'fmt ',
                           16, 1, 1, self.rate, 2 * self.rate, 2, 16,
                           'data', 0)


    def NextNumber(self):
        "Get the next number from input file or random generator."
        if self.numfile.mode == 'r':
            # Player mode
            return self.numfile.readline()
        # Random generator mode

        self.count += 1
        if self.count > self.limit:
            return ''
        result = ''
        if random.random() < self.load:

            for i in range(6):
                result += chr(random.randint(48, 57))
        result += '\n'
        self.numfile.write(result)
        return result
        

    def DoGenerate(self):
        "Perform the actual encoding."
        self.wavfile.write(self.WAVHeader())
        number = self.NextNumber()
        while number:
            for digit in self.DigitSequence(number):

                self.wavfile.write(self.EncodeDigit(digit))
            number = self.NextNumber()
        # Adjust sizes in WAV header
        size = self.wavfile.tell()
        self.wavfile.seek(4)
        self.wavfile.write(struct.pack('<L', size - 8))

        self.wavfile.seek(40)
        self.wavfile.write(struct.pack('<L', size - 44))

def Usage():
    print('Usage: eurosig.py <numbers file> <wav file>')

    print('(to "play" an existing numbers file to a wav file)')
    print('or:    eurosig.py <numbers file> <wav file> <# numbers> [<load>]')
    print('(to generate a random sequence of numbers which will be logged')

    print('to a numbers file and "played" to a wav file -- load will be')
    print('assumed at 0.5 if not given)')

if __name__ == '__main__':
    limit = 0
    load = 0.5
    if len(sys.argv) == 3:

        # Player mode
        num = open(sys.argv[1], 'r')
    elif len(sys.argv) < 6:
        # Random generator mode
        num = open(sys.argv[1], 'w')

        limit = int(sys.argv[3])
        if len(sys.argv) == 5:
            load = float(sys.argv[4])
    else:
        # wrong number of parameters
        usage()

        sys.exit(1)
    wav = open(sys.argv[2], 'wb')
    es = EurosignalEncoder(4000, load, limit, num, wav)
    es.DoGenerate()
    num.close()
    wav.close()

