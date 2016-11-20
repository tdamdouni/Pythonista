# coding: utf-8

# See: https://forum.omz-software.com/topic/2407/images-not-loading-from-camera-roll

import console, photos, ui

filename = 'my_super_special_image.jpg'

img, metadata = photos.pick_image(include_metadata=True, raw_data=True)
# import pprint ; pprint.pprint(metadata)
filename = metadata.get('filename', '').lower() or filename
with open(filename, 'w') as out_file:
    out_file.write(img)
    console.hud_alert(filename + ' written...')
view = ui.ImageView()
view.image = ui.Image.named(filename)
view.present()
