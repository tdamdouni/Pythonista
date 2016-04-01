# coding: utf-8

# https://forum.omz-software.com/topic/2451/running-bottle-in-pythonista-and-another-script-also/3

import pprint, requests

url = 'http://localhost:8080/hello'

if __name__ == '__main__':
	pprint.pprint(requests.get(url).json())