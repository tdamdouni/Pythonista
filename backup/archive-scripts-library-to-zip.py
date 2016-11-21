# https://forum.omz-software.com/topic/1391/archive-scripts-library-to-zip

# Provides an easy way to backup all your scripts by creating
# a zip archive of everything in your Pythonista library
#
# - Run this script
#
# - Look in the 'tmp' folder (default) for a zip file with a
#           timestamped-filename. (e.g. scripts-20141103T0700.zip)
#
# - Tap on the zip file to open it in the native Pythonista viewer
#       Although you won't see anything (as of Pythinista 1.5)
#           you can still tap on the sharing icon in the upper right corner
#           to email or Open the archive in another app for safekeeping.
#
#  Note: This app only creates a backup -- it does not restore/extract zip files.
#  For extracting .zip files, you might try the excellent 'shellista' tool by
#  pudquick/Transistor1 [ https://github.com/transistor1/shellista ]
#
# pacco - lastmod:20141112T2121
#
# 20141103 : initial
# 20141112 : added option to open zip in Pythonista quicklook afterwards
#            [suggested by 'techteej' on OMZ:Pythonista forum]

# First posted on Pythonista forum 20141103
# https://omz-forums.appspot.com/pythonista/post/5306403304505344

import os,sys,zipfile,datetime,console

EXCLUDES=['local-packages'] # any folders you want to exclude from backup

ZIP_DIR='tmp'                   # default folder where the finished .zip file will reside.
                                # Folder will be created if doesn't exist and is automatically
                                # excluded from the backup.

def main():
	zip_dir=ZIP_DIR
	excludelist=EXCLUDES
	open_in_quicklook=False # set True to have Pythonista automatically open completed zip
																																																																																																																																																								# (nice if you're always exporting zip immediately afterwards)
	excludelist.append(zip_dir)
	source_dir=os.path.join(os.path.expanduser("~"),"Documents")
	zip_dir_full=os.path.join(source_dir,zip_dir)
	fname=datetime.datetime.now().strftime("scripts-%Y%m%dT%H%M%S.zip")
	zip_file=os.path.join(zip_dir_full,fname)
	
	try:
		os.stat(zip_dir_full)
	except:
		os.mkdir(zip_dir_full)
	if not os.path.isdir(zip_dir_full):
		print "could not create zip dest dir {zdf}".format(zdf=zip_dir_full)
		sys.exit()
		
	make_zipfile(zip_file,source_dir,excludelist)
	print
	print "{fs} bytes written".format(fs=os.path.getsize(zip_file))
	print "Done."
	
	if open_in_quicklook:
		console.quicklook(zip_file)
		
		
# borrowed and butchered from
# http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory

def make_zipfile(output_filename, source_dir, excludelist):
	relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
	with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
		for root, dirs, files in os.walk(source_dir,topdown=True):
			path_element=os.path.relpath(root,source_dir)
			# incredibly hacky and non-optimal way to implement an exclude list
			nextiter=False
			for path_ex in excludelist:
				if os.path.commonprefix([path_ex,path_element])==path_ex:
					nextiter=True
					break
			if nextiter==True:
				continue
			print "Adding {pe}".format(pe=path_element)
			zip.write(root, os.path.relpath(root, relroot))
			for file in files:
				filename = os.path.join(root, file)
				if os.path.isfile(filename): # regular files only
					arcname = os.path.join(os.path.relpath(root, relroot), file)
					zip.write(filename, arcname)
					
if __name__ == "__main__":
	main()
	
# --------------------

def main():# --------------------
excludelist.append(zip_dir)
source_dir=os.path.join(os.path.expanduser("~"),"Documents")
zip_dir_full=os.path.join(source_dir,zip_dir)
fname=datetime.datetime.now().strftime("scripts-%Y%m%dT%H%M%S.zip")
zip_file=os.path.join(zip_dir_full,fname)

try:
	os.stat(zip_dir_full)
except:
	os.mkdir(zip_dir_full)
if not os.path.isdir(zip_dir_full):
	print "could not create zip dest dir {zdf}".format(zdf=zip_dir_full)
	sys.exit()
	
make_zipfile(zip_file,source_dir,excludelist)
print
print "{fs} bytes written".format(fs=os.path.getsize(zip_file))
print "Done."

if open_in_quicklook:
	console.quicklook(zip_file)
	
if open_in_other_app:
	console.open_in(zip_file)
	
# --------------------

import os, sys, zipfile, datetime, console, time
from dropbox import client, rest, session
import webbrowser

EXCLUDES=['local-packages', 'Backups', '.Trash'] # any folders you want to exclude from backup

ZIP_DIR = 'Backups'             # default folder where the finished .zip file will reside.
				# Folder will be created if doesn't exist and is automatically
				# excluded from the backup.
				
				
def dropbox(APP_KEY, APP_SECRET, ACCESS_TYPE, upload_file):
	global client
	sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	
	# Make the user sign in and authorize this token
	webbrowser.open(url, modal=False, stop_when_done=False)
	raw_input()
	
	# This will fail if the user didn't visit the above URL and hit 'Allow'
	access_token = sess.obtain_access_token(request_token)
	client = client.DropboxClient(sess)
	response = client.put_file(upload_file, upload_file)
	
def main():
	zip_dir=ZIP_DIR
	excludelist=EXCLUDES
	
	excludelist.append(zip_dir)
	source_dir=os.path.join(os.path.expanduser("~"),"Documents")
	zip_dir_full=os.path.join(source_dir,zip_dir)
	fname=datetime.datetime.now().strftime("Scripts Backup - %m%d%Y - %I:%M %p.zip")
	zip_file=os.path.join(zip_dir_full,fname)
	
	try:
		os.stat(zip_dir_full)
	except:
		os.mkdir(zip_dir_full)
	if not os.path.isdir(zip_dir_full):
		console.hud_alert("Could not create zip dest dir {zdf}".format(zdf=zip_dir_full), 'error', 1.5)
		sys.exit()
		
	make_zipfile(zip_file,source_dir,excludelist)
	bytes = "Backup Successfully Created - {fs} bytes written".format(fs=os.path.getsize(zip_file))
	console.hud_alert(bytes, 'success', 1.5)
	dropbox('rso5vcsund16lw9','wqivu6pzm3ef93s', 'dropbox', zip_file)
	
# http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory

def make_zipfile(output_filename, source_dir, excludelist):
	relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
	with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
		for root, dirs, files in os.walk(source_dir,topdown=True):
			path_element=os.path.relpath(root,source_dir)
			# incredibly hacky and non-optimal way to implement an exclude list
			nextiter=False
			for path_ex in excludelist:
				if os.path.commonprefix([path_ex,path_element])==path_ex:
					nextiter=True
					break
			if nextiter==True:
				continue
			str = ("Adding {pe}").format(pe=path_element)
			console.show_activity(str)
			time.sleep(1)
			zip.write(root, os.path.relpath(root, relroot))
			for file in files:
				filename = os.path.join(root, file)
				if os.path.isfile(filename): # regular files only
					arcname = os.path.join(os.path.relpath(root, relroot), file)
					zip.write(filename, arcname)
			console.hide_activity()
			
if __name__ == "__main__":
	main()# --------------------

