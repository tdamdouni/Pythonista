"""
This code takes two screenshots from the camera roll combines them into one image and saves the new image to the camera roll.

This is adapted from Federico Viticci's blog post at:
http://www.macstories.net/stories/automating-ios-how-pythonista-changed-my-workflow/
It removes the option to change which picture is where, automatically assigning the first one chosen as the leftmost image.
It also removes the necessity to copy the images to the clipboard outside of Pythonista using the new photos library in version 1.3. Finally, it removes the clipboard output.
"""

import photos
import Image
import console

im1 = photos.pick_image(show_albums=False)
im2 = photos.pick_image(show_albums=False)

background = Image.new('RGBA', (746,650), (255, 255, 255, 255))

console.clear()
print "Generating image..."
console.show_activity()

_1 = im1.resize((366,650),Image.ANTIALIAS)
_2 = im2.resize((366,650),Image.ANTIALIAS)
background.paste(_1,(0,0))
background.paste(_2,(380,0))
photos.save_image(background)
console.hide_activity()
print "Image saved to camera roll."
