# https://forum.omz-software.com/topic/4004/raw-jpeg

import photos
from objc_util import *
for a in photos.get_assets():
	if ObjCInstance(a).isRAW():
		a.delete()
		print('deleted ', a)

