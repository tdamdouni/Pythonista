# coding: utf-8

# https://forum.omz-software.com/topic/3883/upload-any-files-from-any-app-via-pythonista-script-to-my-raspberry-pi-connected-harddisk/2

import appex
import console
import os
import ui
from ftplib import FTP

def main():

	# Sharing: receive file
	fil = appex.get_file_path()
	if fil == None:
		print('no file passed')
		return
		
	server = 'Your ip'
	user = 'Your user'
	pwd = 'your password'
	server_file = os.path.basename(fil)
	
	try:
		ftp = FTP(server) #connect
		ftp.encoding = 'utf-8'
		ftp.login(user,pwd)
		ipad_file = open(fil,'rb')
		ftp.storbinary('STOR '+server_file,ipad_file,blocksize=8192)
		ipad_file.close()
		ftp.close()
	except Exception as e:
		print(str(e))
		
	appex.finish()
	
if __name__ == '__main__':
	main()
