#!/usr/bin/env python

# See: http://en.wikipedia.org/wiki/Morse_code

alpha2code_dict = {
    'a' : '.-',
    'b' : '-...',
    'c' : '-.-.',
    'd' : '-..',
    'e' : '.',
    'f' : '..-.',
    'g' : '--.',
    'h' : '....',
    'i' : '..',
    'j' : '.---',
    'k' : '-.-',
    'l' : '.-..',
    'm' : '--',
    'n' : '-.',
    'o' : '---',
    'p' : '.--.',
    'q' : '--.-',
    'r' : '.-.',
    's' : '...',
    't' : '-',
    'u' : '..-',
    'v' : '...-',
    'w' : '.--',
    'x' : '-..-',
    'y' : '-.--',
    'z' : '--..',
    '1' : '.----',
    '2' : '..---',
    '3' : '...--',
    '4' : '....-',
    '5' : '.....',
    '6' : '-....',
    '7' : '--...',
    '8' : '---..',
    '9' : '----.',
    '0' : '-----' }
code2alpha_dict = {v:k for k,v in alpha2code_dict.iteritems()}

def morse(msg='... --- ...' or 'sos'):
	msg = msg.lower().strip()
	if msg and msg[0] not in '.-':  # easy case: alpha to morse code
		return ' '.join([alpha2code_dict.get(x, ' ')  for x in msg])
		
	# harder case: morse code to alpha
	out_msg = ''
	while msg:
		letter, _, msg = msg.partition(' ')
		out_msg += code2alpha_dict.get(letter, ' ')
	return out_msg.strip()
	
def test_cases():
	print(morse('sos'))
	print(morse('... --- ...'))
	
	msg = 'I  really  LOVE hacking Morse Code in Python!'  # deal with uppercase, extra spaces, punctuation
	print(morse(msg))
	print(morse(morse(msg)))
	
	msg = ''.join([k for k in sorted(alpha2code_dict)])
	print(morse(morse(msg)))  # test entire translation table
	assert msg == morse(morse(msg)), 'Error in translation!!'
	
def main(args):
	if args:
		print(morse(' '.join(args)))
	else:
		test_cases()
		
if __name__ == "__main__":
	import sys  # put quotes around morse code on commandline or words will run together
	main(sys.argv[1:])  # strip off the script name

