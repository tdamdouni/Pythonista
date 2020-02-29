from __future__ import print_function
import Image, ImageOps, ImageFilter
import ftplib
import console
import clipboard
import datetime
from io import BytesIO
import urllib

today = datetime.datetime.now()
image = clipboard.get_image()
fileName = console.input_alert("Image Title", "Enter Image File Name")
if fileName != '':
	fileName = fileName+'_'+today.strftime("%Y-%m-%d-%H%M%S") +'.png'
else:
	fileName = today.strftime("%Y-%m-%d-%H%M%S") +'.png'
	
userName = "server_username"
userPass = "server_password"
host = "server_ip"
port = 22
urlBase = "http://www.jayhickey.com/media/mobile/"

remotePath = "/Dropbox/Blog/media/mobile/"

# datePath = today.strftime("%Y/%m/")
# Used to create full remote file path
remoteFilePath = remotePath

def customSize(img):
	w, h = img.size
	print('w: ' + str(w))
	print('h: '+ str(h))
	if w > 620:
		wsize = 620/float(w)
		print('wsize: '+str(wsize))
		hsize = int(float(h)*float(wsize))
		print('hsize: ' + str(hsize))
		
		img = img.resize((620, hsize), Image.ANTIALIAS)
	return img
	
image = customSize(image)
print(image.size)
image.show()

buffer = BytesIO()
image.save(buffer, 'PNG')
buffer.seek(0)

print(remoteFilePath)
print(fileName)

fileURL = urllib.quote(fileName)

ftp = ftplib.FTP(host, userName, userPass)
ftp.cwd(remoteFilePath)
ftp.storbinary('STOR '+fileName, buffer)
ftp.quit()
imageLink = urlBase+fileURL
print(imageLink)
clipboard.set(imageLink)

