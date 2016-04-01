# coding: utf-8

# https://forum.omz-software.com/topic/2353/encoding-images-in-base64

# I need to encode images in base64 for the purposes of passing them through an x-callback-url. I have this code but it's not working

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

# One issue that might be happening is that when its encoded to an callback URL, it's including characters that aren't URL safe. Try using base64.urlsafe_b64encode(str(encoded))