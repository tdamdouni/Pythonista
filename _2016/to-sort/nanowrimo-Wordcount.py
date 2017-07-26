#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://gist.github.com/ejetzer/f29099adf8e008b3a3b8

from __future__ import print_function

import sys, requests, hashlib
if sys.version_info.major == 2: input = raw_input

# You can get you key from http://nanowrimo.org/api/wordcount
KEY = '8996ghhhftdgn87j'
USER = 'ejetzer'

wordcount = input('How many words?')
hashed = hashlib.sha1(KEY + USER + wordcount).hexdigest()
print(hashed)

content = 'hash={}&name={}&wordcount={}'.format(hashed, USER, wordcount)
print(content)

headers = {'Content-Type': 'application/x-www-form-urlencoded'}


response = requests.put('https://nanowrimo.org/api/wordcount', content, headers=headers)
if response.status_code != 200:
	print('There has been a problem.')
	print(response)
	for i, v in response.headers.items():
		print(i, ':', v)
	print()
	print(response.content)

