import Image
import ImageChops
import ImageDraw
import ImageFont
import ImageFilter
import clipboard

def draw_caption(img, text, outline=2, top=False):
	text_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
	draw = ImageDraw.Draw(text_img)
	w = img.size[0]
	s = 100
	while w >= (img.size[0] - 20):
		font = ImageFont.truetype('HelveticaNeue-CondensedBlack', s)
		w, h = draw.textsize(text, font=font)
		s -= 1
		if s <= 12: break
	text_y = 0 if top else img.size[1] - h
	draw.text((10, text_y), text, font=font, fill='black')
	kernel = [0, 1, 2, 1, 0,
	1, 2, 4, 2, 1,
	2, 4, 0, 4, 1,
	1, 2, 4, 2, 1,
	0, 1, 2, 1, 0]
	myfilter = ImageFilter.Kernel((5, 5), kernel, scale = 0.25 * sum(kernel))
	for i in xrange(outline):
		print 'Processing image... ' + str(int(float(i)/outline * 100)) + '%'
		text_img = text_img.filter(myfilter)
	print 'Processing done.'
	draw = ImageDraw.Draw(text_img)
	draw.text((10, text_y), text, font = font, fill = 'white')
	mask_img = ImageChops.invert(text_img)
	result_img = Image.composite(img, text_img, mask_img)
	return result_img
	
if __name__ == '__main__':
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
		img = draw_caption(img, caption_top, outline=3, top=True)
	print 'Enter the bottom caption (press return for none):'
	caption_btm = unicode(raw_input(), 'utf-8')
	caption_btm = caption_btm.upper()
	if caption_btm != '':
		img = draw_caption(img, caption_btm, outline=3, top=False)
	img.show()
	# If you want to copy the result to the clipboard automatically,
	# uncomment the following line:
	#clipboard.set_image(img.convert('RGBA'))
	# You can also copy an image from the console output or save it
	# to your camera roll by touching and holding it.

