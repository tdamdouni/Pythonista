from __future__ import print_function
# https://forum.omz-software.com/topic/1153/url-scheme-and-x-callback-url/7

import webbrowser
import sys

# From: https://github.com/VisionSmarts/pic2shop-client/blob/master/iOS/Classes/pic2shopClientViewController.m
#
# pic2shop always scans UPC-A, UPC-E, EAN13, EAN8 and QR, one cannot restrict to some formats
# pic2shop will replace "EAN" by barcode or "QR" by QR code

if len(sys.argv)>1:
	#print 'args: ' + str(sys.argv[1:])
	if sys.argv[1] != 'EAN':
		print('Barcode: ' + sys.argv[1])
	elif sys.argv[2] != 'QR':
		print('QR: ' + sys.argv[2])
	else:
		print('Scan not recognized')
else:
	webbrowser.open('pic2shop://scan?callback=pythonista%3A//scanner%3Faction%3Drun%26argv%3DEAN%26argv%3DQR')

