# https://forum.omz-software.com/topic/3499/simple-file-download/10

import requests

print()

destpath = 'ex24file.txt'
url = "https://raw.githubusercontent.com/grrrr/py/741ba0500bc49e8f6268f02d23e461649e8d457b/scripts/buffer.py"

with open(destpath,'wb') as file:
	file.write(requests.get(url).content)

