from __future__ import print_function
# Show an image picker dialog (allowing multiple selection) and print the result

import photos
assets = photos.pick_asset(title='Pick some assets', multi=True)
print(assets)

