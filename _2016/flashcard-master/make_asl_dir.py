# https://github.com/polymerchm/flashcard

# Create a "simple" ASL subdirectory for demo purposes
#
# Create Main Directory
#
import os, Image, ImageDraw, ImageFont

directories = ['Chapter %02d' % (i+1) for i in range(5)]
os.mkdir('ASL')
os.chdir('ASL')
font = ImageFont.truetype('ChalkboardSE-Bold', 48)
for directory in directories:
	os.mkdir(directory)
	os.chdir(directory)
	for count, letter in enumerate('abcdefghij'):
		imagename = "%s test image %02d: %s" % (letter, count+1, directory)
		im = Image.new("RGBA", (512, 512), "white")
		draw = ImageDraw.Draw(im)
		draw.text((10,10), "test image %02d" % (count+1), fill=128, font=font)
		draw.text((20,60), directory, fill=128, font=font)
		del draw
		im.save(imagename + '.jpg' )
	os.chdir('..')
