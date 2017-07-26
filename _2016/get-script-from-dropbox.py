# https://gist.github.com/paultopia/23703b934c442a54808e245d9418545a

import requests, appex
from urllib.parse import urlparse
url = appex.get_url().replace("dl=0", "dl=1")
#r = requests.get(url)
filename = urlparse(url).path.rpartition("/")[-1].replace(".py", "-downloaded.py")
with open(filename, "wb") as outfile:
	#outfile.write(r.content)
	outfile.write(requests.get(url).content)
print("script downloaded as " + filename)

