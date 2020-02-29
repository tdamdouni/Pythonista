# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/d43e11857a875d187a2a

from __future__ import print_function
import ftplib, os, shutil, tempfile, time

ftp=ftplib.FTP('ftp.deentaylor.com')
print(ftp.login('pythonista@deentaylor.com', 'FTPythonista'))

doc_path = os.path.expanduser('~/Documents/')
filename=time.strftime("%Y-%m-%d&%H:%M:%S")
backup_path = filename+'.zip'
if os.path.exists(backup_path):
	os.remove(backup_path)
	
print('Creating archive...', end=' ')
shutil.make_archive(os.path.join(tempfile.gettempdir(), filename), 'zip')
shutil.move(os.path.join(tempfile.gettempdir(), backup_path), backup_path)
print('Done!')

print('Uploading {} bytes to FTP server...'.format(str(os.path.getsize(backup_path))), end=' ')

def upload(ftp, file):
	ext= os.path.splitext(file)[1]
	if ext in (".txt", ".htm", ".html"):
		ftp.storlintes("STOR "+file, open(file))
	else:
		ftp.storbinary("STOR "+file, open(file,"rb"),1024)
try:
	upload(ftp,backup_path)
	print("Done!")
except:
	print("Upload failed")
os.remove(backup_path)

