from __future__ import print_function
# Allows you to upload simple articles and images from clipboard
# to your Statamic site using Pythonista.
# 
# There are several variables which must be completed for this
# script. Please read below carefully and fill out all of the. See
# options.
# 
# This script was originally based on a script I found at 
# David Spark's Macdrifter site:
# http://macdrifter.com/2012/11/the-power-of-pythonista-12.html

import Image, ImageOps, ImageFilter
import ftplib
from string import Template
import datetime
from io import BytesIO
import cStringIO
import urllib
from unicodedata import normalize
import sys
import keychain
import console
import clipboard
console.clear()

# FTP credentials. Self explanatory. uses keychain
# to store FTP password
userName = "username"
userPass = keychain.get_password("ftp",userName)
host = "mysite.com"
rootDir = "/public_html/"

# These are specific fields that I want to add to my YAML info 
# at the top of my article. You may not have a need for these
# so simply remove them from the code and be sure to clean 
# up the 'template' variable below as well as the 'values'
# template way below.

post_template_name = "blog"
author = "admin"

# This is my post template. You can change it to whatever you need
# yours to look like. However, the values are populated down further
# in the script and you will need to ensure that your '$y' variables
# match up otherwise the script will fail in a not so graceful manner. Also, i have a strange way of creating header images  for posts.
# It's bot common to have that 'photos' list at the bottom of the template 
# you may want to move '$yPhotos' below the dashed lines into your content
template ='''---
title: $yTitle
_templates: $yTemplate
author: $yAuthor
categories:
 - $yCategories
status: $yStatus
photos: 
 - url: $yPhotos
---
$yContent'''

# standard locations for images and content for Statamic
imgBase = "/assets/img/"
contentBase = "/_content/"
imgRemotePath = rootDir + imgBase
txtRemotePath = rootDir + contentBase

# Let's get the image from the clipboard and ask some questions
today = datetime.datetime.now()
image = clipboard.get_image()
imgFileName = console.input_alert("Image Title", "Enter Image File Name")
title = console.input_alert("Article Title", "Enter the article title")
sts = console.alert("Status","Choose the article 	status","Live","Draft","Hidden")
category = console.input_alert("Post category", "Enter a category")
words = console.input_alert("Article Text", "Enter your thoughts")
imgFileName = imgFileName +'_'+ today.strftime("%Y-%m-%d-%H%M%S") +'.png'

if sts == 1:
	status = "live"
elif sts == 2:
	status = "draft"
elif sts == 3:
	status = "hidden"

# Can we connect to the FTP?
try:
	console.show_activity()
	ftp = ftplib.FTP(host, userName, userPass)
	console.hide_activity()
except Exception as e:
	print("Unable to connect to FTP")

# trying to retrieve the folders used in the 'txtRemotePath' directory
# returns a simple dictionary with folders info separated. 
def get_folders():
	try:
		console.show_activity()
		ftp.cwd(txtRemotePath)
		data = []
		ftp.retrlines('MLSD', data.append)
		dir = []
		for line in data:
			facts_found, _, name = line.rstrip('CRLF').partition(' ')
			entry = {}
			for fact in facts_found[:-1].split(";"):
				key, _, value = fact.partition("=")
				entry[key.lower()] = value
			if entry['type'] == 'dir':
				dir.append(name)

		count = 0
		folders = []
		for eachDir in dir:
			folder = eachDir.partition("-")[2]
			folders.append([count,eachDir,folder])
			count +=1
		
		return folders

	except Exception as e:
		print("Unable to get folder listing")

# Generates the actual text for the article with YAML headers
def make_file(template,values):
	yaml_fe = Template(template)
	result = yaml_fe.safe_substitute(values)
	return result

# Found this at https://gist.github.com/4021956
# this will help when we need to slugify your title for the filename
def slug(text, encoding=None, permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
	if isinstance(text, str):
		text = text.decode(encoding or 'ascii')
	clean_text = text.strip().replace(' ', '-').lower()
	while '--' in clean_text:
		clean_text = clean_text.replace('--','-')
	ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
	strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
	return ''.join(strict_text)

# David's code to resize your clipboard image
def customSize(img):
    w, h = img.size
    print('w: ' + str(w))
    print('h: '+ str(h))
    if w > 600:
        wsize = 600/float(w)
        print('wsize: '+str(wsize))
        hsize = int(float(h)*float(wsize))
        print('hsize: ' + str(hsize))
 
        img = img.resize((600, hsize), Image.ANTIALIAS)
    return img

# Nothing to see here. Just the fun stuff coming together.
image = customSize(image)
print(image.size)
image.show()
print(title + " (" + status + ")")
print(words)
 
imgBuffer = BytesIO()
image.save(imgBuffer, 'png')
imgBuffer.seek(0)

folders = get_folders()

# I decided to stop at 3 folders in the assets directory. I only have 2
# and more than 3 seemed like the exception not the rule so I got lazy.
if len(folders) == 1:
	folder_slug = 1
elif len(folders) == 2:
	folder_slug = console.alert("Category","Choose image folder",folders[0][2].title(),folders[1][2].title())
elif len(folders) == 3:
	folder_slug = console.alert("Category","Choose image folder",folders[0][2].title(),folders[1][2].title(),folders[2][2].title())

imgRemoteFilePath = imgRemotePath + folders[folder_slug-1][2] + "/"
txtRemoteFilePath = txtRemotePath + folders[folder_slug-1][1] + "/"

# My site uses the _entry_timestamps variable 
# set to true so you may need to modify the
# date format below
title_slug = slug(title)
txtFileName = today.strftime("%Y-%m-%d-%H%M") +'_'+ title_slug +'.md'

fileURL = urllib.quote(imgFileName)
imageLink = imgRemoteFilePath+fileURL
imgMarkdownFilePath = imgBase + folders[folder_slug-1][2] + "/" + fileURL

# Told you it was way down here. These '$y' keys and their corresponding
# values need to match whatever you have listed at the top in the 
# 'template' variable
values = {
	"yTitle" : title,
	"yTemplate" : post_template_name,
	"yAuthor" : author,
	"yCategories" : category,
	"yStatus" : status,
	"yPhotos" : imgMarkdownFilePath,
	"yContent" : words
}

txtData = make_file(template,values)
 
txtBuffer = cStringIO.StringIO()
txtBuffer.write(txtData)
txtBuffer.seek(0)

# Doing some uploading here.
try:
	console.show_activity()
	ftp.cwd(imgRemoteFilePath)
	ftp.storbinary('STOR '+imgFileName, imgBuffer)
	console.hide_activity()
except Exception as e:
	print("Unable save image file")

try:
	console.show_activity()
	ftp.cwd(txtRemoteFilePath)
	ftp.storbinary('STOR '+txtFileName, txtBuffer)
	console.hide_activity()
except Exception as e:
	print("Unable save article file")

ftp.quit()

print("\n=================\nFinished")
