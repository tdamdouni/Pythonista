# coding: utf-8



def convert_to_hsl(r, g, b):

	#Figure out which color is weakest....
	if r <= g and r <= b:
		min = r
	elif g <= r and g <= b:
		min = g
	else:
		min = b


	#Then the strongest
	if r >= g and r >= b:
		max = r
	elif g >= r and g >= b:
		max = g
	else:
		max = b

	#Luminance is easy
	l = (max + min) / 2

	#Just a shortcut for the following code
	diff = (max - min)

	#Calculate Saturation
	if l < 0.5:
		s = diff / (max + min)
	elif l > 0.5:
		s = diff / (2 - diff)
	else:
		s = 0

	#Calculate Hue (this is the important one)
	if max == r:
		h = (g - b) / diff
	elif max == g:
		h = 2 + (b - r) / diff
	elif max == b:
		h = 4 + (r - g) / diff

	#This should convert it to degrees and correct it if it turns out negative
	h = (h * 60)
	if h < 0:
		h += 360

	#Return all three
	return h, s, l


def calculate_difference(r1, g1, b1, r2, g2, b2):
	
	#Convert both colors into HSL
	h1, s1, l1 = convert_to_hsl(r1, g1, b1)
	h2, s2, l2 = convert_to_hsl(r2, g2, b2)

	#Find the difference
	diff = h1 - h2

	#If it's a negative number, flip it
	if diff < 0:
		diff = (diff * -1)
	
	#Return difference
	return diff


