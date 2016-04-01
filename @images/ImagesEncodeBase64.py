# https://forum.omz-software.com/topic/2353/encoding-images-in-base64

# coding: utf-8

import workflow
import clipboard
import photos
import base64

source_selection = workflow.get_variable('source')

if source_selection == 'photo':
    image_selection = photos.pick_image()
else:
    image_selection = clipboard.get_image()
    if not image_selection:
        console.alert('No Image', 'Clipboard does not contain an image')
        
w, h = image_selection.size

encoded = base64.b64encode(str(image_selection)

workflow.set_variable('encodedImage', str(encoded))
        
workflow.set_variable('origSize', str(w))