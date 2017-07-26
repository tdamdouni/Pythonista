# https://forum.omz-software.com/topic/4110/reading-pythonistas-apples-plist-file-format/2

import plistlib

path = '/private/var/mobile/Containers/Shared/AppGroup/CB0CD8AB-6A20-4ECC-8312-B0822DFFD9A1/Library/Preferences/group.pythonista.plist'

with open(path, 'rb') as f:
	data = plistlib.load(f)
	
print(data)

