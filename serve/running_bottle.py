# coding: utf-8

# https://forum.omz-software.com/topic/2451/running-bottle-in-pythonista-and-another-script-also/2

from __future__ import print_function
import requests

msg_url = 'http://localhost:8080/hello'

def msg_get(url):
	x= requests.request('GET', url)
	print(x.json())


if __name__ == '__main__':
	msg_get(msg_url)