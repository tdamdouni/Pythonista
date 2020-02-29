from __future__ import print_function
# @viticci
# Taken from Viticci :: https://github.com/viticci/pythonista-scripts
# Takes two iPhone 5 screenshots, places them side-by-side in a single image set to the clipboard.
# Python version of this Keyboard Maestro macro: http://www.macstories.net/tutorials/a-better-way-to-combine-iphone-screenshots-with-keyboard-maestro/
# Unlike ScreenshotsClipboard, this script lets you set the placement of screenshots in the final image
# You can, for instance, decide to paste the first Photos.app screenshot (index starts at 0) as the second image on the right
# If you choose "the second image", the second file copied in Photos.app will be pasted first.
# Inspired by Gabe Weatherhead: http://www.macdrifter.com/pythonista-app-from-toy-to-tool.html

import photos
import clipboard
import Image

if clipboard.get_image(idx=0) and clipboard.get_image(idx=1):
  im1 = clipboard.get_image(idx=0)
  im2 = clipboard.get_image(idx=1)
else: 
  im1 = photos.get_image(-1)
  im2 = photos.get_image(-2)
  
_1 = im1.resize((366,650),Image.ANTIALIAS)
_2 = im2.resize((366,650),Image.ANTIALIAS)
background = Image.new('RGBA', (746,650), (255, 255, 255, 255))

print("Which image goes on the left? (in Photos.app order)")

print("[1] The first image")

print("[2] The second image")

formatType = raw_input("Select an image: ")

if formatType == "x":

    print("Exited")

else:

    #userInput = raw_input("Input String: ")

    print("\n\n")

if formatType == "1":

		background.paste(_1,(0,0))
		background.paste(_2,(380,0))
		background.show()

elif formatType == "2":

		background.paste(_1,(380,0))
		background.paste(_2,(0,0))
		background.show()


clipboard.set_image(background)