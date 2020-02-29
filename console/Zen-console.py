#!python2

# https://gist.github.com/jefflovejapan/5076080

# Zen
#
# Prints the Zen of Python with a color gradient.
# This demonstrates the use of the console module to set
# the output's font and color.

from __future__ import print_function
import console
import sys
import codecs
from colorsys import hsv_to_rgb
from StringIO import StringIO

#Suppress the output while importing 'this':
prev_out = sys.stdout
sys.stdout = StringIO()
import this
sys.stdout = prev_out
console.clear()

#Decode the 'Zen of Python' text and split to a list of lines:
decoder = codecs.getdecoder('rot_13')
text = decoder(this.s)[0]
lines = text.split('\n')

#Print the title (first line):
console.set_font('Futura', 22)
console.set_color(0.2, 0.2, 0.2)
print(lines[0])

#Print the other lines in varying colors:
hue = 0.45
for line in lines[1:]:
	r, g, b = hsv_to_rgb(hue, 1.0, 0.8)
	console.set_color(r, g, b)
	console.set_font('Futura', 16)
	print(line)
	hue += 0.02
	
#Reset output to default font and color:
console.set_font()
console.set_color()

