# coding: utf-8

# [pythonistabackup]: https://github.com/lukaskollmer/pythonista-scripts/blob/master/pythonista_backup/PythonistaBackup.py

'''Creates a zip archive of your Pythonista files and uploads it to S3.'''

from __future__ import print_function

import boto
from boto.s3.key import Key
import console
import keychain
from objc_util import NSBundle
import os
import requests
import shutil
import sys
import tempfile
import time
import ui

try:
	from reprint_line import reprint
except ImportError:
	reprint = print

console.clear()


@ui.in_background
def perform_backup(quiet=True):
	try:
		is_amazon_up = requests.get('http://s3.amazonaws.com').status_code == 200
	except requests.exceptions.ConnectionError:
		is_amazon_up = False
	if not is_amazon_up:
		if quiet:
			return
		else:
			sys.exit('ERROR: Unable to connect to s3.amazonaws.com')
	doc_path = os.path.expanduser('~/Documents')
	os.chdir(doc_path)
	backup_path = os.path.join(doc_path, 'Backup.zip')
	if os.path.exists(backup_path):
		os.remove(backup_path)
	print('Creating backup archive...')
	shutil.make_archive(os.path.join(tempfile.gettempdir(), 'Backup'), 'zip')
	shutil.move(os.path.join(tempfile.gettempdir(), 'Backup.zip'), backup_path)
	print('Backup archive created, uploading to S3 ...')
	
	date_text = time.strftime('%Y-%b-%d')
	time_text = time.strftime('%I-%M-%S-%p')
	info_dict_version_key = 'CFBundleShortVersionString'
	main_bundle = NSBundle.mainBundle()
	app_version = str(main_bundle.objectForInfoDictionaryKey_(info_dict_version_key))[0]
	
	AWS_ACCESS_KEY_ID = keychain.get_password('aws', 'AWS_ACCESS_KEY_ID')
	AWS_SECRET_ACCESS_KEY = keychain.get_password('aws', 'AWS_SECRET_ACCESS_KEY')
	
	bucket_name = 'lukaskollmer'
	
	def percent_cb(complete, total):
		reprint('{}'.format(round(float(complete) / float(total) * 100, 2)))
	
	s3 = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = s3.get_bucket(bucket_name)
	
	filename = 'Backup-{}.zip'.format(time_text)
	k = Key(bucket)
	k.storage_class = 'REDUCED_REDUNDANCY'
	k.key = '/Backup/Pythonista{}/{}/{}'.format(app_version, date_text, filename)
	print('0.0 %')
	k.set_contents_from_filename('Backup.zip', cb=percent_cb, num_cb=10)
	print('Successfully uploaded')
	os.remove(backup_path)

if __name__ == '__main__':
	perform_backup(quiet=False)
