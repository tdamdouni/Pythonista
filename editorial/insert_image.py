# coding: utf-8

# https://github.com/cclauss/editorial

# Editorial Workflows

# insert_image.py

# - Prompt for image selection from the camera roll.
# - Save selection as as a jpeg in the current document's directory using the current date as filename.
# - Aappend an incrementing number if multiple images are inserted.
# - Preserve the original image orientation.
# - Insert a markdown image reference.

# The workflow is forked from [Insert Image... ](http://www.editorial-workflows.com/workflow/5896882052136960/tbnRcIh3c38) written by [@pastrunho](http://twitter.com/pastrunho). The code for orientation was found in post from [scabbiaza](http://stackoverflow.com/users/1350976/scabbiaza) on [StackOverflow](http://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in). Putting it together and any other modifications and/or creations of code come from me.

from PIL import Image, ExifTags
import photos
import workflow
import console
import editor
import os
import io
import time

timestr = time.strftime("%Y-%m-%d")

img = photos.pick_image()
if not img:
	workflow.stop()

try:
	for orientation in ExifTags.TAGS.keys():
		if ExifTags.TAGS[orientation]=='Orientation':
      break
	exif=dict(img._getexif().items())

	if exif[orientation] == 3:
		img=image.rotate(180, expand=True)
	elif exif[orientation] == 6:
		img=img.rotate(270, expand=True)
	elif exif[orientation] == 8:
		img=image.rotate(90, expand=True)
# cases: image don't have getexif
except (AttributeError, KeyError, IndexError):
	pass

doc_path = editor.get_path()
doc_dir, fn = os.path.split(doc_path)
default_name = '%s' % timestr + '_' + 'image'

i = 1
while True:
	if not os.path.exists(os.path.join(doc_dir, default_name + '.jpg')):
		break
	default_name = '%s' % timestr + '_' + 'image' + '_' + str(i)
	i += 1

root, rel_doc_path = editor.to_relative_path(editor.get_path())
filename = default_name + '.jpg'

if not filename:
	workflow.stop()

img_data = io.BytesIO()
img.save(img_data, 'jpeg')

rel_doc_dir, fn = os.path.split(rel_doc_path)
dest_path = os.path.join(rel_doc_dir, filename)
editor.set_file_contents(dest_path, img_data.getvalue(), root)
workflow.set_output(filename)
