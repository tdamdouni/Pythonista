# coding: utf-8

# https://forum.omz-software.com/topic/2637/is-it-possible-to-read-a-file-say-txt-file-from-other-app/6

import appex
print appex.get_attachments()

#==============================

text=open(appex.get_attachments()[0]).read()
open('a.txt','w').write(text)

#==============================

>>> import appex
>>> appex.get_attachments()
[u"/var/mobile/Containers/Data/Application/E2D89A6E-FD16-4428-BAC4-2E01276796E6/Documents/What's new in GoodReader 4.11.pdf", u"/var/mobile/Containers/Data/Application/E2D89A6E-FD16-4428-BAC4-2E01276796E6/Documents/What's new in GoodReader 4.11.pdf"]

#==============================

>>> import appex
>>> import json
>>> print(json.dumps(appex.get_input(), indent=4))
[
    {
        "attachments": [
            {
                "com.adobe.pdf": "/var/mobile/Containers/Data/Application/E2D89A6E-FD16-4428-BAC4-2E01276796E6/Documents/What's new in GoodReader 4.11.pdf",
                "public.file-url": "/var/mobile/Containers/Data/Application/E2D89A6E-FD16-4428-BAC4-2E01276796E6/Documents/What's new in GoodReader 4.11.pdf"
            }
        ]
    }
]

#==============================

import appex, shutil

if appex.is_running_extension():
	file_path = appex.get_file_path()
	if file_path:
		shutil.copy(file_path, '.')

