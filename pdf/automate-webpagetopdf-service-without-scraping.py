# coding: utf-8 

# https://forum.omz-software.com/topic/3004/auto-fill-form-and-simulate-enter/8

# @omz If you want to use webpagetopdf.com, you don't really have to parse the page, emulate clicks etc. You can bypass all that by doing essentially the same as the JavaScript on that page (which isn't much, it basically just generates a random session/conversion ID, makes one GET request to start the conversion, and a couple more to check its status, and to download the result when the conversion has finished). I've made a little script to automate that process without scraping the page:
	
from __future__ import print_function
import requests
import urllib
import random
import time

def random_string():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(alphabet) for i in range(16))

def convert_to_pdf(page_url, verbose=True):
    sid = random_string()
    cid = random_string()
    conv_url = 'http://webpagetopdf.com/convert/%s/%s/?url=%s' % (sid, cid, urllib.quote(page_url, ''))
    if verbose:
        print('Requesting conversion...')
    r = requests.get(conv_url)
    pid = r.json()['pid']
    if verbose:
        print('pid:', pid)
    filename = 'result.pdf'
    while True:
        print('Checking conversion status...')
        r = requests.get('http://webpagetopdf.com/status/%s/%s/%s' % (sid, cid, pid))
        status_info = r.json()
        if 'file' in status_info:
            filename = status_info['file']
        if verbose:
            print(status_info)
        if status_info['status'] == 'processing':
            time.sleep(1)
        elif status_info['status'] == 'success':
            break
        else:
            return None
    urllib.urlretrieve('http://webpagetopdf.com/download/%s/%s' % (sid, cid), filename)
    return filename

if __name__ == '__main__':
    print('Running demo...')
    page_url = 'http://pythonista-app.com'
    filename = convert_to_pdf(page_url)
    if filename:
        import console, os
        console.quicklook(os.path.abspath(filename))
    else:
        print('Conversion failed')
