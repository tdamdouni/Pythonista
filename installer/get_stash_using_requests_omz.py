# https://forum.omz-software.com/topic/2545/stash-for-pythonista-2-and-3/32

# I usually use requests like this to download a file without having to load it in memory completely. Works in Python 2 and 3.

import requests
url = 'https://github.com/ywangd/stash/archive/master.zip'
r = requests.get(url, stream=True)
with open('dest.zip', 'wb') as f:
    for chunk in r.iter_content(1024):
        f.write(chunk)
