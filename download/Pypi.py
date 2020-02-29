from __future__ import print_function
import urllib
import tarfile
import shutil
import console
import os

class Installer(object):
	name = None
	version = None
	firstLetter = None
	lowerName = None
	tarfolder = None
	tarname = None
	
	def __init__(self, name, version):
		self.name = name
		self.version = version
		self.firstLetter = name[0]
		self.lowerName = name.lower()
		self.tarfolder = self.name + '-' + self.version
		self.tarname = self.tarfolder + '.tar.gz'

	def install(self):
		try:
			self.download()
			self.extract()
			self.copy()
		except Exception as e:
			print(str(e))
		finally:
			self.clean()
		
	def download(self):
		print('Downloading ' + self.name + ' v' + self.version + '...')
		url = 'http://pypi.python.org/packages/source/' + self.firstLetter + '/' + self.name + '/' + self.tarname
		urllib.urlretrieve(url, self.tarname)
		print('Download Complete')

	def extract(self):
		print('Extracting...')
		t = tarfile.open(self.tarname)
		t.extractall()
		print('Package extracted')
			
	def copy(self):
		# If source is a folder
		if os.path.isdir(self.tarfolder + '/' + self.lowerName):
			if os.path.isdir(self.lowerName):
				print('Removing old package directory...')
				shutil.rmtree(self.lowerName)
			print('Installing package directory...')
			shutil.move(self.tarfolder + '/' + self.lowerName, './' + self.lowerName)
			
		# if source is a file
		file = self.lowerName + '.py'
		if os.path.isfile(self.tarfolder + '/' + file):
			if os.path.isfile(file):
				print('Removing old package file...')
				os.remove(file)
			print('Installing package file...')
			shutil.move(self.tarfolder + '/' + file, './' + file)
			
	def clean(self):
		print('Cleaning up...')
		if os.path.isdir(self.tarfolder):
			print('Removing source directory...')
			shutil.rmtree(self.tarfolder)
		if os.path.isfile(self.tarname):
			print('Removing source tarball...')
			os.remove(self.tarname)
		print('Done.')
