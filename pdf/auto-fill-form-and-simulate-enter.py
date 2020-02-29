# -*- coding: utf-8 -*-

# https://forum.omz-software.com/topic/3004/auto-fill-form-and-simulate-enter/6

from __future__ import print_function
import requests
import re

def convert_url(url):
    html = re.sub('src="/(?!/)', 'src="' + url, requests.get(url).text) #attempt to get resources from base url
    input_files = {'input_files[]': ('html.html', html)}
    fields = {'from' : 'html', 'to' : 'pdf'}
    r = requests.post('http://c.docverter.com/convert', data=fields, files=input_files)
    with open('converted.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size = 1024):
            fd.write(chunk)

convert_url('http://www.google.com')

# --------------------

# -*- coding: utf-8 -*-

# https://forum.omz-software.com/topic/3004/auto-fill-form-and-simulate-enter/6

import requests
import re

def convert_url(url):
    html = re.sub('src="/(?!/)', 'src="' + url, requests.get(url).text) #attempt to get resources from base url
    html = re.findall('<h3 class=\'post-title entry-title\'.*<div id=\'post-livres\'>', html, re.DOTALL)[0]
    html = re.sub('<div.*?>|</div>', '', html)
    html = re.sub('<img ', '<img width=100% ', html)
    input_files = {'input_files[]': ('html.html', html)}
    fields = {'from' : 'html', 'to' : 'pdf'}
    r = requests.post('http://c.docverter.com/convert', data=fields, files=input_files)
    with open('converted.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size = 1024):
            fd.write(chunk)
    print('done')

convert_url('http://www.lacuisinedebernard.com/2016/03/galettes-de-son-davoine-aux-carottes.html')

# --------------------
