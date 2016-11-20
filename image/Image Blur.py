#Copy and pasted bits of input output in pythonista on iPad
import sys, os
import Image
import ImageFilter
 
inputFile = 'IMAGE NAME'
outputFile = os.path.splitext(inputFile)[0] + ".png"
im = Image.open('IMAGENAME')
im = im.filter(ImageFilter.BLUR)
mask = Image.new((im.mode), (im.size))
out = Image.blend(im, mask, 0.3)
out.save(outputFile)
im.show()
