# coding: utf-8

# https://forum.omz-software.com/topic/3883/upload-any-files-from-any-app-via-pythonista-script-to-my-raspberry-pi-connected-harddisk/5

import appex
import console
import os
import ui
import paramiko
from io import BytesIO


def UploadCallBack(tran_bytes,  total_bytes):
	print("Bytes Transferred:" +tran_bytes + "\nTotal Bytes:" + total_bytes)
	
def main():

	# Sharing: receive file
	input_file = appex.get_file_path()
	if input_file == None:
		print('no file passed')
		return
		
		
	# SFTP Configuration
	
	host = '192.168.1.x'
	port = 22
	password = 'password'
	username = 'Username'
	remoteFilePath = '/media/sda/'
	
	server_file = os.path.basename(input_file)
	filesize = os.path.getsize(input_file)
#   print("server_file:" + server_file)
	print("Starting to upload the file:" + input_file + "(Size: ", end='')
	print(filesize, end='')
	print(")... ")
	
	try:
		transport = paramiko.Transport((host, port))
		
		transport.connect(username = username, password = password)
		
		sftp = paramiko.SFTPClient.from_transport(transport,max_packet_size=8*1024*1024)
		
		''' sftp.open()
		
		while with open(input_file, 'rb') as ipad_file:
		
		read(ipad_file,  )
		'''
		#sftp.putfo(ipad_file, remoteFilePath + server_file, callback=UploadCallBack(int, int ))
		ipad_file = open(input_file, 'rb')
		
		sftp.putfo(ipad_file, remoteFilePath + server_file)
		
		ipad_file.close()
		sftp.close()
		
		transport.close()
		print('Upload done!')
		
	except Exception as e:
		print(str(e))
		
	appex.finish()
	
if __name__ == '__main__':
	main()

