from __future__ import print_function
# ** Universal iOS screenshot merge **
# Script will take two images of same orientation and merge them together. 
#
# By: Jason Verly (@mygeekdaddy)
# Date: 2014-10-13
# Ver: 1.02

import clipboard
import Image
import console
import photos

console.clear()

console.alert("Pick first image", "", "Select")
im1 = photos.pick_image(show_albums=True)

console.alert("Pick second image", "", "Select")
im2 = photos.pick_image(show_albums=True)

console.show_activity()

w,h = im1.size

print(im1.size)
print('Ratio is ' + str((w*1.0)/h))

def image_merge(img):
	if (w*1.0)/h > 1:
		print('Landscape screenshot...')
		#(2048, 1536)
		#Landscape screenshot
		background = Image.new('RGB', ((w+20), ((h*2)+30)), (255,255,255))
		print("Generating image...")
		background.paste(im1,(10,10))
		background.paste(im2,(10,(h+20)))
		# background.show()
		photos.save_image(background)	
	else:
		print('Portrait screenshot...')
		#(1536, 2048)
		#Portrait screenshot
		background = Image.new('RGB', (((w*2)+30),(h+20)), (255, 255, 255))
		print("Generating image...")
		background.paste(im1,(10,10))
		background.paste(im2,((w+20),10))
		# background.show()
		photos.save_image(background)	

image = image_merge(im1)
print("\n\nImage saved to camera roll.")