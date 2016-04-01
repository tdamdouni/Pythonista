https://github.com/jmcmellen/sameeas

===============================================================
License (see the MIT License)

Copyright (c) 2011 John McMellen

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
==============================================================

In other words, use at your own risk. This software is for testing
purposes only. No guarantees of suitability or compatibility
with any FCC approved EAS decoders are expressed or implied. 
Users of the software are encouraged to do extensive testing
before using in a production environment, if ever.

HOW TO USE:
==========================================================

NOTE: Usage examples are listed below this section.

The executable file is a compiled version of the four
Python scripts easencode.py (the commandline interface),
eastestgen.py (EAS message formatting), afsk.py (afsk routines),
and audioroutines.py (library functions for signal generation).
The scripts were developed using Python 2.7 and should run
correctly in any platform where Python 2.7 is installed.

The executable file easencode.exe (easencode.py) provides 
a simple commandline implementation of an EAS encoder. You 
pass it the configuration details and the result is a WAVE
file that *should* be an EAS message according to the 
structure defined by the FCC rules. This flexibility allows
the user the ability to generate a variety of activation
messages and observe the way the decoder reacts. Consult 
the FCC rules for the correct values for FIPS codes and
activation messages.

The software also provides a "fuzzer" mode wherein the user
can generate messages with incorrect or undocumented values.
This can be used to check how the decoder responds to data
that is not-defined or incorrectly formatted.

Some basic help is available on the commandline using the 
(-h) help option.

USAGE EXAMPLES
=============================================================

Generate a simple test, 15 minute duration
    easencode.exe -e RWT -f 029177 -d 0015 -c WXYZ eas-rwt.wav
    easencode.exe -e RWT -f 029177 -d 0015 -t now -c "WXYZ FM" eas-rwt.wav

Generate a test with a voice message from input.wav
    easencode.exe -e RWT -f 037124 -d 0015 -c KXYZ -a input.wav eas-rwt.wav

Fuzz mode: Generate a test with a non-standard EAS message using -z or --fuzz
    easencode.exe --fuzz "WXR-RAT-012345-111111+0123-BLAHBLAH-" output_eas.wav
    Read the FCC rules for the exact format of an EAS message