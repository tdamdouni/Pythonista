# @viticci
# Same as ScreenshotsClipboard, but images are fetched from Pythonista's image manager.
# Based on: http://www.macstories.net/tutorials/a-better-way-to-combine-iphone-screenshots-with-keyboard-maestro/
# Uses two screenshots saved in Pythonista's image manager

import Image
import clipboard
im1 = Image.open('_1').convert("RGB")
im2 = Image.open('_3').convert("RGB")
background = Image.new('RGBA', (746,650), (255, 255, 255, 255))
background.paste(im1,(0,0))
background.paste(im2,(380,0))
background.show()

clipboard.set_image(background)