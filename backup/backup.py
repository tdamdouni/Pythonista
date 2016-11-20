# Provides an easy way to backup all your scripts by creating
# a zip archive of everything in your Pythonista library
#
# Note: This app only creates a backup -- it does not restore/extract zip files.
# For extracting .zip files, try 'shellista' https://github.com/transistor1/shellista

import os, sys, zipfile, datetime, console, time
from dropbox import client, rest, session
from webbrowser import open

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
	open(url, modal=True)
	raw_input('Please press enter to continue')
	
	# This will fail if the user didn't visit the above URL and hit 'Allow'
	access_token = sess.obtain_access_token(request_token)
	client = client.DropboxClient(sess)
	response = client.put_file('Script Backups' + upload_file, upload_file)
	
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
	dropbox('qnlzpc6u8oun74e','edoeh1udb2bgsxn', 'app_folder', zip_file)
	console.clear()
	console.hud_alert('Uploaded to Dropbox!', 'success', 1.5)
	
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
	main()

