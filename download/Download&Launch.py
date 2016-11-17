# coding: utf-8
import urllib
import editor
url = 'https://gist.githubusercontent.com/gillibrand/3271073/raw/155ac9f391db74a1ace1c5c954fa7ed4e74255db/air_hockey.py'
contents = urllib.urlopen(url).read()
editor.make_new_file('AirHockey.py', contents)