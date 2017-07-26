# https://forum.omz-software.com/topic/3844/photos-asset-get_image_data-is-there-a-memory-leak/2

import photos
from get_available_memory import get_free_mem
import gc
from PIL import Image
photo_count = 1000
photo_index = 0
all_assets = photos.get_assets()
print('Start', get_free_mem()) #Start 814.9 MB
while photo_index < photo_count:
	ass = all_assets[photo_index]
	img_data = ass.get_image_data()
	img_data.__del__()
	del img_data
	del ass
	gc.collect()
	photo_index += 1
del all_assets
gc.collect()
print('Done', get_free_mem()) #Done 165.4 MB

