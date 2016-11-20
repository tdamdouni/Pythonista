# https://forum.omz-software.com/topic/3605/how-do-i-transfer-code-such-as-pc-to-ipad/7

import requests as r
with open('image_carousel.pyui', 'w', encoding='utf-8') as f:
	f.write(r.get('https://gist.githubusercontent.com/balachandrana/de389c3bd84f006ad4c8d5e3d1cd4a8d/raw/63fc6110035e17472a41c160c733c003f3989b67/image_carousel.pyui').text)

