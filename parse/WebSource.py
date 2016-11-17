# coding: utf-8

# https://forum.omz-software.com/topic/2582/get-web-source-code/7

import urllib2
html_file_url = "" # set your file's url here
download_to = "" # set the name of the file you want to save the html to
open(download_to,"w").write(urllib2.url_open(html_file_url).read())

# http://stackoverflow.com/questions/7395542/is-explicitly-closing-files-important

with open(download_to, "w") as out_file:  # will automatically close()
	out_file.write(urllib2.url_open(html_file_url).read())

