# Meme Generator 1
# Demonstrates how to draw text on images using PIL
# (Python Imaging Library)
#
# The script loads an image from the clipboard (or uses
# a default one if the clipboard is empty) and asks for
# two captions (top and bottom) that are then drawn onto
# the image.

import Image
import ImageDraw
import ImageFont
import clipboard

def draw_caption(img, text, top=False):
	draw = ImageDraw.Draw(img)
	#Find a suitable font size to fill the entire width:
	w = img.size[0]
	s = 100
	while w >= (img.size[0] - 20):
		font = ImageFont.truetype('HelveticaNeue-CondensedBlack', s)
		w, h = draw.textsize(text, font=font)
		s -= 1
		if s <= 12: break
	#Draw the text multiple times in black to get the outline:
	for x in xrange(-3, 4):
		for y in xrange(-3, 4):
			draw_y = y if top else img.size[1] - h + y
			draw.text((10 + x, draw_y), text, font=font, fill='black')
	#Draw the text once more in white:
	draw_y = 0 if top else img.size[1] - h
	draw.text((10, draw_y), text, font=font, fill='white')
	
def main():
	print 'Loading image from clipboard...'
	img = clipboard.get_image()
	if img is None:
		print 'No image in clipboard, using default image instead...'
		img = Image.open('Test_Mandrill')
	img.show()
	print 'Enter the top caption (press return for none):'
	caption_top = unicode(raw_input(), 'utf-8')
	caption_top = caption_top.upper()
	if caption_top != '':
		draw_caption(img, caption_top, top=True)
	print 'Enter the bottom caption (press return for none):'
	caption_btm = unicode(raw_input(), 'utf-8')
	caption_btm = caption_btm.upper()
	if caption_btm != '':
		draw_caption(img, caption_btm, top=False)
	img.show()
	# If you want to copy the result to the clipboard automatically,
	# uncomment the following line:
	#clipboard.set_image(img.convert('RGBA'))
	# You can also copy an image from the console output or save it
	# to your camera roll by touching and holding it.
	
if __name__ == '__main__':
	main()

