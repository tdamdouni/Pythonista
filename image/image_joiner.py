from __future__ import print_function
import sys, Image, math

# Join two images together, either horizontally or vertically, 
# with resizing to match joined dimension. Works on Mac OS X or iOS.
# On Mac OS X, the Python Imaging Library is required
# On iOS, Pythonista is required
# Michelle L. Gill, 2014/01/20

# Padding and borders
padding = 10
border = 10

# Background color
bkgcolor = (255,255,255)
transparency = (255,)

# Are we on Mac ('darwin') or iOS ('unknown')
platform = sys.platform

if platform == 'darwin':
	# Get the files on Mac
	import subprocess as sp

	# The applescript command to open dialog boxes for file selection
	# A second file dialog will open if only one file is selected--this allows for files in different directories
	# If more than two files are selected, only the first two are taken
	cmd = """set theFileList to choose file with prompt "Choose both images if in the same directory or choose the second later." with multiple selections allowed
	if (number of items in theFileList is 1) then
		set theFileList2 to choose file with prompt "Choose second image."
		copy theFileList2 to the end of theFileList
	end if

	if (number of items in theFileList is greater than 2) then
		set theFileList to items 1 through 2 of theFileList
	end if

	set theFileListPath to {}
	repeat with theFileAlias in theFileList
		set theFileTmp to "'" & (the POSIX path of theFileAlias) & "'"
		copy theFileTmp to the end of theFileListPath
	end repeat
	theFileListPath"""

	# Run the applescript command and get the output
	proc = sp.Popen(['osascript', '-'], stdin=sp.PIPE, stdout=sp.PIPE)
	stdout = proc.communicate(cmd)

	# Somtimes this list needs to be cleaned up because there is a stray None at the end
	fileString = [x.strip() for x in stdout if x is not None][0]

	# Split the string by looking for this: ', '
	# Assumes this string doesn't occur in file name
	fileList = fileString.split('\', \'')

	# Remove remaining single quote
	fileList[0] = fileList[0][1:]
	fileList[1] = fileList[-1][:-1]

	# Open the files
	im1 = Image.open(fileList[0])
	im2 = Image.open(fileList[1])

else:
	# On iOS copy the files to the clipboard before running the script
	import clipboard
	import photos

	# Get the images from the clipboard
	#im1 = clipboard.get_image(idx=0)
	#im2 = clipboard.get_image(idx=1)
	im1 = photos.pick_image()
	im2 = photos.pick_image()

# Determine stacking type and order
print('Are images to be stacked [v]ertically or [h]orizontally?')
stacktype = raw_input('Enter selection [v|h]:').strip().lower()

if stacktype == 'h':
	print('Does the first image go on the [l]eft or on the [r]ight?')
	ordertype = raw_input('Enter selection [l|r]:').strip().lower()
else:
	print('Does the first image go on the [t]op or on the [b]ottom?')
	ordertype = raw_input('Enter selection [t|b]:').strip().lower()

# Determine border and padding
print('Set padding between images in pixels.')
padding_str = raw_input('Enter value or leave blank for 0:').strip()
if len(padding_str) > 0:
	padding = abs(int(padding_str))

print('Set border around combined image in pixels.')
border_str = raw_input('Enter value or leave blank for 0:').strip()
if len(border_str) > 0:
	border = abs(int(border_str))

# Set background color if there is a border or padding
### TODO: This is transparency not color, fix this
colordict = {'w':(255,255,255), 'b':(0,0,0)}
bkgcolor_str = 'w'
if (padding > 0) or (border > 0):
	print('Choose background color of [w]hite or [b]lack.')
	bkgcolor_str = raw_input('Enter selection [w|b]:').strip().lower()
	if bkgcolor_str not in colordict.keys():
		bkgcolor_str = 'w'
bkgcolor = colordict[bkgcolor_str]

# Set transparency
if (padding >0) or (border>0):
	print('Set transparency percentage.')
	transparency_str = raw_input('Enter percentage from 0 (opaque) to 100 (transparent):').strip()
	transparency = int(float(255)*(100-float(transparency_str)))
	
	if transparency < 0:
		transparency = 0
	
	if transparency > 255:
		transparency = 255
	
	transparency = tuple([transparency])

# Setup a list of the images and of their dimensions
if (ordertype == 'l') or (ordertype == 't'):
	imlist = [im1, im2]
else:
	imlist = [im2, im1]

imdim = [list(x.size) for x in imlist]

# Scale larger figure if necessary
if stacktype == 'h':
	scalelist = [x[1] for x in imdim]
else:
	scalelist = [x[0] for x in imdim]

if abs(scalelist[0] - scalelist[1]) > 0:
	scaleratio = float(min(scalelist))/float(max(scalelist))

	if scalelist[0] > scalelist[1]:
		scalenum = 0
	else:
		scalenum = 1

	# Calculate the resized dimensions and shrink the appropriate image	
	imdim[scalenum] = [int(float(x)*scaleratio) for x in imdim[scalenum]]
	imlist[scalenum] = imlist[scalenum].resize(tuple(imdim[scalenum]), Image.ANTIALIAS)

# Calculate dimensions of the new image and create it
if stacktype == 'h':
	newdims = (sum([x[0] for x in imdim])+(padding+2*border), max([x[1] for x in imdim])+(2*border))
else:
	newdims = (max([x[0] for x in imdim])+int(2*border), sum([x[1] for x in imdim])+(padding+2*border))

newimage = Image.new('RGBA', newdims, bkgcolor+transparency)

# Add the two original images to the joined one
newimage.paste(imlist[0],(border,border))
if stacktype == 'h':
	newimage.paste(imlist[1],(imdim[0][0]+border+padding,border))
else:
	newimage.paste(imlist[1],(border,imdim[0][1]+border+padding))


if platform == 'darwin':
	# Save image to a tmp file
	filename = '/var/tmp/image.jpg'
	fh = open(filename,'w')
	newimage.save(fh, 'JPEG', quality=90)
	fh.close()
	# View the file using default image viewer
	proc = sp.Popen(['/bin/sh','-'], stdin=sp.PIPE, stdout=sp.PIPE)
	stdout = proc.communicate('open '+ filename)
else:
	# Save image to clipboard
	clipboard.set_image(newimage)
	# View the file
	newimage.show()

