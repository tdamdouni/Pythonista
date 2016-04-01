from bisect import bisect
import console
import random
import time
import warnings

import clipboard
import photos
from PIL import Image, ImageFont, ImageDraw

#Characters grouped into 'visual weight'
grayscale = (" ",
             " ",
             ".,-",
             "_ivc=!/|\\~",
             "gjez2]/(YL)t[+T7Vf"
             "mdK4ZGbNDXY5P*Q",
             "W8KMA",
             "$&#%")

#Benchmarks for when to use which character set
thresholds = (36, 72, 108, 144, 180, 216)

def resize(im, base=200):
	#Resize so the smaller image dimension is always 200
	if im.size[0] > im.size[1]:
		x = im.size[1]
		y = im.size[0]
		a = False
	else:
		x = im.size[0]
		y = im.size[1]
		a = True
	
	percent = (base / float(x))
	size = int((float(y) * float(percent)))
	if a:
		return im.resize((base, int(size * 0.5)), Image.ANTIALIAS)
	else:
		return im.resize((size, int(base * 0.5)), Image.ANTIALIAS)


def image2ASCII(im, scale=200, showimage=False):
	if showimage:
		im.show()
	#Make sure an image is selected
	if not im:
		raise ValueError("No Image Selected")
	
	#Make sure the output size is not too big
	if scale > 500:
		warnings.warn("Image cannot be more than 500 characters wide")
		scale = 500
	
	im = resize(im).convert("L")  # Luminosity returns a single brightness value rather than three color values
	
	#Begin with an empty string that will be added on to
	output=''
	#Create the ASCII string by assigning a character
	#of appropriate weight to each pixel
	for y in range(im.size[1]):
		for x in range(im.size[0]):
			luminosity = 255 - im.getpixel((x, y))
			row = bisect(thresholds, luminosity)
			possible_chars = grayscale[row]
			#output += possible_chars[random.randint(0, len(possible_chars)-1)]
			output += random.choice(possible_chars)
		output += '\n'
	#return  the final string
	return output


def RenderASCII(text, fontsize=5, bgcolor='#EDEDED'):
	'''Create an image of the ASCII text'''

	linelist=text.split('\n')
	try:
		font = ImageFont.truetype("DejaVuSansMono", fontsize * 4)
	except:
		import _font_cache
		font = ImageFont.truetype(_font_cache.get_font_path('DejaVuSansMono'))
	width, height = font.getsize(linelist[1])
	
	image = Image.new("RGB", (width, height * len(linelist)), bgcolor)
	draw = ImageDraw.Draw(image)
	
	for i, line in enumerate(linelist):
		draw.text((0, i * height), line, (0, 0, 0), font=font)
	return image


def stitchImages(im1,im2):
	'''Takes 2 PIL Images and returns a new image that 
	appends the two images side-by-side. '''
	
	im2 = im2.resize((im2.size[0]/2, im2.size[1]/2), Image.ANTIALIAS)
	im1 = im1.resize(im2.size, Image.ANTIALIAS)
	
	#store the dimensions of each variable
	w1, h1 = im1.size
	w2, h2 = im2.size
	
	#Take the combined width of both images, and the greater height
	width = w1 + w2
	height = max(h1, h2)
	
	im = Image.new("RGB", (width, height), "white")
	im.paste(im1, (0, 0))
	im.paste(im2, (w1, 0))
	
	return im


if __name__ == "__main__":
	while 1:
		#Ask the user to either take a photo or choose an existing one
		capture = console.alert("Image2ASCII", button1="Take Photo", button2="Pick Photo")
	
		if capture == 1:
			im = photos.capture_image()
		elif capture == 2:
			im = photos.pick_image(original=False)
		
		console.show_activity()
	
		out = image2ASCII(im, 200)
		outim = RenderASCII(out, bgcolor = '#ff0000')
		stitchImages(im, outim).show()
	
		console.hide_activity()
		
		outim.save('image.jpg')
		console.quicklook('image.jpg')
		
		mode = console.alert("Image2ASCII", "You can either:", "Share Text", "Share Image")
		if mode == 1:
			with open('output.txt', 'w') as out_file:
				out_file.write(out)
			console.open_in('output.txt')
		elif mode == 2:
			console.open_in('image.jpg')
		
		time.sleep(5)
		console.clear()
