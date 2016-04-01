#!/usr/bin/python
#===============================================================
#  easencode.py - A utility to make EAS audio files
#  February 25, 2011
#
#===============================================================
#
#===============================================================
#License (see the MIT License)
#
#Copyright (c) 2011 John McMellen
#
#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation
#files (the "Software"), to deal in the Software without
#restriction, including without limitation the rights to use,
#copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the
#Software is furnished to do so, subject to the following
#conditions:
#
#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#OTHER DEALINGS IN THE SOFTWARE.
#
#=================================================================

from eastestgen import *
import argparse #from optparse import OptionParser
import sys, os
import re
import time, wave


def main():
    numCh = 1
    peakLevel = -10
    sampWidth = 16
    sampRate = 44100
    msgaudio = None

    try:
        for option, value in args.__dict__.iteritems():
	    if value is not None:
	        if option is 'fips':
		    value = " ".join(value)
		if args.custom_msg is None:
		    print option, value
		if not re.match(arg_patterns[option], str(value), re.I):
		    parser.error("Invalid {0} '{1}'".format(option, value ))
	
	if re.match(r'\d{2}/\d{2}/(\d{4})\s+\d{2}:\d{2}',
		args.timestamp, re.I):
	    ts_val = time.strftime('%j%H%M', time.strptime(args.timestamp,
		                      r'%m/%d/%Y %H:%M'))
	else:
	    ts_val = time.strftime('%j%H%M', time.gmtime())
	if len(args.fips) > 31:
	    print "WARNING: only 31 FIPS codes allowed. Truncating..."
	if len(args.callsign) > 8:
	    print "WARNING: callsign max width is 8 characters. Truncating..."

	if args.audioin is not None:
	    infile = wave.open(args.audioin, 'rb')
	    numCh, sampWidth, sampRate, audio_dur, compression, comment = infile.getparams()
	    sampWidth = sampWidth * 8
	    #print infile.getparams()
	    msgaudio = infile.readframes(infile.getnframes())
	    infile.close()
	else:
	    infile = None
	data = generateEASpcmData(args.originator, args.event, args.fips, 
		args.duration, ts_val, args.callsign, sampRate, sampWidth, 
		peakLevel, numCh, msgaudio, args.custom_msg)
	data = filterPCMaudio(3000, sampRate, 20, sampWidth, numCh, data)
	file = wave.open(args.outputfile, 'wb')
	file.setparams( (numCh, sampWidth/8 , sampRate, sampRate, 'NONE', '') )
	file.writeframes(data)
	file.close()

    except Exception as inst:
	print "Exception:", inst, inst.args, sys.exc_info()[1]

program_version = "1.2"
events = ('ean', 'eat', 'nic', 'npt', 'rmt', 'rwt', 'toa', 'tor', 'sva', 'svr',
	  'svs', 'sps', 'ffa', 'ffw', 'ffs', 'fla', 'flw', 'fls', 'wsa', 'wsw',
	  'bzw', 'hwa', 'hww', 'hua', 'huw', 'hls', 'tsa', 'tsw', 'evi', 'cem',
	  'dmo', 'adr')
originators = ('pep', 'wxr', 'civ', 'eas')
arg_patterns = {'event':r'|'.join(events), 'fips':r'^(\d{6})(\s+\d{6})*$', 
	        'timestamp':r'(now)|(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', 'originator':r'|'.join(originators), 
		'duration':r'([0-1][0-9][03]0)|(00[14]5)|(2[0-3][03]0)|(2400)',
		'callsign':r'.*', 'audioin':r'.+\.wav', 'outputfile':r'.+\.wav',
		'custom_msg':r'.*'}

first_parser = argparse.ArgumentParser(add_help=False)
first_parser.add_argument("-z", "--fuzz", dest="custom_msg")
#first_parser.add_argument("outputfile", metavar='OUTPUT.WAV', type=str)

parser = argparse.ArgumentParser(description="A script to generate EAS messages",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog="""Usage examples:

Generate a simple test, 15 minute duration
    %(prog)s -e RWT -f 029177 -d 0015 -c WXYZ eas-rwt.wav
    %(prog)s -e RWT -f 029177 -d 0015 -t now -c "WXYZ FM" eas-rwt.wav

Generate a test in the future
    %(prog)s -e RWT -f 029177 -d 0100 -t "12/31/2020 15:30" -c "WXYZ" eas-rwt.wav

Generate a test with a voice message from input.wav
    %(prog)s -e RWT -f 037124 -d 0015 -c KXYZ -a input.wav eas-rwt.wav

Fuzz mode: Generate a test with a non-standard EAS message using -z or --fuzz
    %(prog)s --fuzz "WXR-RAT-012345-111111+0123-BLAHBLAH-" output_eas.wav

""")
parser.add_argument("-v", "--ver", "--version", action='version', 
	version="EASEncode Version {0}/Core version {1}".format(program_version,
		eastestgen_core_version) )
parser.add_argument("-z", "--fuzz", dest="custom_msg", 
	help="pass a non-standard EAS message string to encoder")
parser.add_argument("-o", "--org", dest="originator",  
	help="set the message originator", default='EAS')
parser.add_argument("-e", "--event", dest="event", 
	help="set the event type", required=True)
parser.add_argument("-f", "--fips", dest="fips", nargs='+', metavar=('FIPS',
        'FIPS2'), help="set the destination fips codes", required=True)
parser.add_argument("-d", "--dur", dest="duration",
	help="set the event duration HHMM, 15 minute increment work up" \
	" to one hour, after that it is 30 minutes, i.e. 0015, " \
	"0130, etc.", required=True)
parser.add_argument("-t", "--start", dest="timestamp", default="now",
	help="override the start timestamp, format is 'MM/DD/YYYY HH:MM'" \
		" UTC timezone or use 'now' (default)")
parser.add_argument("-c", "--call", dest="callsign",
	help="set the originator call letters or id", required=True)
parser.add_argument("-a", "--audio-in", dest="audioin", type=str,
	help="insert audio file between EAS header and eom; max length"
	" is 2 minutes")
parser.add_argument('outputfile', metavar='OUTPUT.WAV', type=str)

try:
    args1, args2 = first_parser.parse_known_args()
    #print args1, args2
    if args1.custom_msg is None:
        args = parser.parse_args(args2)
    else:
	default_cmd = ['-z', args1.custom_msg, '-e', 'RWT', '-f', '000000', 
		'-d', '0015', '-c', '0']
	default_cmd.extend(args2)
	#print default_cmd
	args = parser.parse_args(default_cmd) 

except Exception as inst:
    print inst
    parser.exit()


timeslanguage = {r'now': time.time(), r'tomorrow': time.time() + 24 * 60 * 60,
	         r'1 days*': time.time() + 24 * 60 * 60  }


if __name__ == "__main__":
    main()

