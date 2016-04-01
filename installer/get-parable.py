# coding: utf-8

# https://gist.github.com/crcx/9ee092d1eac8a09bd849

# This is a small script to download / update the Parable sources
# under Pythonista.

import requests
import os.path
import sys

urls = ['https://raw.githubusercontent.com/crcx/parable/master/py/allegory',
        'https://raw.githubusercontent.com/crcx/parable/master/py/parable.py',
        'https://raw.githubusercontent.com/crcx/parable/master/py/stdlib.p',
        'https://raw.githubusercontent.com/crcx/parable/master/py/listener.py',
       ]

print('Downloading')
for url in urls:
    sys.stdout.write('  ' + os.path.basename(url) + '\t\t')
    r =  requests.get(url)
    with open(os.path.basename(url), 'w') as f:
        f.write(r.content)
    print(str(len(r.content)) + ' bytes')
print('Finished')