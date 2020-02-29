from __future__ import print_function
# Universal screenshot merger for Pythonista.
# Takes any number of screenshots,
# downscales if Retina,
# merges.
#
# by Greg V <http://floatboth.com>

# Settings:

margin = 15  # pixels
background = (255, 255, 255, 255)  # RGBA
retina_pixels = (2048, 1536, 1136, 960, 640)

####################

import sys
import photos
import console
import Image

def clear():
	console.clear()
	console.set_font("Futura-Medium", 20)
	console.set_color(0.40, 0.40, 0.40)

clear()
print("Pick one image at a\ntime, when you're\ndone, tap anywhere\noutside the\npicker.")

images = []
	
while 1:
	img = photos.pick_image(show_albums=True)
	if img:
		images.append(img)
	else:
		break

count = len(images)

clear()

if count == 0:
	console.set_color(0.50, 0.00, 0.00)
	print("No images selected.")
	sys.exit()

print("Merging {0} images...".format(count))

width, height = images[0].size
if width in retina_pixels:
	width, height = map(lambda a: a/2, (width, height))

result = Image.new("RGBA", (width*count + margin*(count-1), height), background)

for i, img in enumerate(images):
	shot = img.resize((width, height), Image.ANTIALIAS)
	result.paste(shot, (width*i+margin*i, 0))

console.set_color(0.25, 0.50, 0.00)
print("Done! Resolution: {0} by {1} pixels.".format(result.size[0], result.size[1]))
console.set_color(0.40, 0.40, 0.40)
print("Tap and hold on the image to copy or save.")
result.show()
