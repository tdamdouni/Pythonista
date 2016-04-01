# Resize some photos and save back to camera roll

import photos
import clipboard
import Image
import console
import sys

# Here is where you set the amount of original size 
# that you'd like the final images to be, e.g. 100
# would be original size (and would break the script)
# and 25 would result in images 1/4 original size.

reduction_amounts = {'Retina iPhone': 35, 'Non-retina iPhone': 50,
                     'Retina iPad': 60, 'Non-retina iPad': 75 }

for amount in reduction_amounts:
	if reduction_amounts[amount] >= 100:
		print 'One of your reduction_amounts is too high, must be lower than 100.\nExample: If you want the resulting image to be 1/4 its original size, the reduction_amounts would be 25.'
		sys.exit()

# This takes a max of 5 arguments including the title and message, 
# so you can really only put in 2 devices and 'Custom'. Set the two
# you want here.
# Make sure they match the string in reduction_amounts exactly!
q1 = 'Retina iPhone'
q2 = 'Non-retina iPad'

if not clipboard.get_image(idx=0):
	print 'I don\'t think there are any images on the clipboard.'
	sys.exit()

resizeAmountQ = console.alert('What percent of original size?','','{0}% (default for {1})'.format(reduction_amounts[q1], q1),'{0}% (default for {1})'.format(reduction_amounts[q2], q2), 'Custom')
if resizeAmountQ == 1 :
	resizeAmount = float(reduction_amounts[q1]) / 100
elif resizeAmountQ == 2 :
	resizeAmount = float(reduction_amounts[q2]) / 100
elif resizeAmountQ == 3 :
	resizeAmount = float(console.input_alert('What percent of original size?','Number only','40')) / 100
else:
	print 'Whups!'
	sys.exit()
	
x = 0
while True:
	img = clipboard.get_image(idx=x)

	if img:
		width, height = img.size

		smaller = img.resize( (int(width * resizeAmount), int(height * resizeAmount) ), Image.ANTIALIAS)
		photos.save_image(smaller)
		
		x += 1
		
	else:
		print 'Looks like it worked. The downsampled images should be in your camera roll.'
		break 


