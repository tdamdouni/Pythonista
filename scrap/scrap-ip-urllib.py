#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/3682/scraping

import urllib
import speech
getsrc = urllib.urlopen('https://disneyland.disney.go.com/calendars/day/')
read = getsrc.read()
print(read[1751:1766])
rate = '1'
speech.say('Your IP is ' + read[1751:1766], rate)
