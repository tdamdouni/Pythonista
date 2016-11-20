# https://forum.omz-software.com/topic/3605/how-do-i-transfer-code-such-as-pc-to-ipad/6

It is mainly due to Apple's restrictions such a utility is not built-in. I use the following simple steps to do the transfer.

## Save to gist

From the file navigation panel (script library - left side of editor panel), you can select multiple files (including .pyui files) and tap the share sheet icon at the bottom to save it to gist. You can save it as anonymous if you do not have gist account. The url will be available in clipboard and you can either store the url in a file using 'paste' or you can use the following script (stored as editor action) to mail the url to your friends.

	import dialogs, clipboard
	dialogs.share_text(clipboard.get())  

## Get from gist

Open the gist url in safari and run the share script savefile (utility from JonB). It will get all the files in gist and store them in the predefined directory.

You can get the share script by running the folowing script.

import requests as r
with open('savefile.py', 'w', encoding='utf-8') as f:
	f.write(r.get('https://gist.githubusercontent.com/jsbain/fcb3f42932dde9b0ff6c122893d1b230/raw/ab19fcd73598b829413da4c487bf5896b7cddeb0/savefile.py').text)
