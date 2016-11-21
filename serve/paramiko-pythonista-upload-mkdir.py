# https://gist.github.com/pattulus/bf20b63b457a259752ed

# http://stackoverflow.com/questions/18047808/sftp-upload-via-python-and-pythonista-with-paramiko-cant-create-directory-subd

# Set Variables
fileName = "temp.png"
remotePath = "/home/userZ/Dropbox/uploads/"
datePath = "year/month/"
remoteFilePath =  remotePath + datePath + fileName #

# Set Definition for "mkdir -p"
def mkdir_p(sftp,remote_directory):
	remote_dirname, basename = os.path.split(remote_directory)
	mkdir_p(os.path.dirname(remote_directory))
	try:
		sftp.chdir(name)
	except IOError:
		sftp.mkdir(name)
		sftp.chdir(name)
		
try:
	transport.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(transport)     # Start SFTP client
	
	# Try to make remote path - 3 Versions and all fail
	mkdir_p(sftp,remoteFilePath) # Version 1
	#mkdir_p(sftp, os.path.split(remoteFilePath)) # Version 2
	#sftp.mkdir(os.path.split(remoteFilePath)) # Version 3
	
	# Put file to remote
	sftp.put('temp.png', remoteFilePath)
	
	# Close connection
	#finally:
	transport.close()
	sftp.close()
