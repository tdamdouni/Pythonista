import os
import urllib2
import tarfile
import shutil

workingPath = os.getcwd()
tempPath = os.path.join(workingPath, 'temp')
dateutilArchiveDir = 'python-dateutil-1.5'
dateutilArchive = dateutilArchiveDir + '.tar.gz'
dateutilArchivePath = os.path.join(tempPath, dateutilArchive)

try:
	os.mkdir(tempPath)
except OSError:
	pass

dateutilArchiveUrl = urllib2.urlopen('http://labix.org/download/python-dateutil/' + dateutilArchive)
localArchive = open(dateutilArchivePath, 'w')
localArchive.write(dateutilArchiveUrl.read())
localArchive.close()
dateutilArchiveUrl.close()
archive = tarfile.open(dateutilArchivePath, 'r:gz')

try:
	os.chdir(tempPath)
	archive.extractall()
finally:
	archive.close()
	os.chdir(workingPath)


dateutilDir = 'dateutil'
tempDateutilPath = os.path.join(os.path.join(tempPath, dateutilArchiveDir), dateutilDir)
dateutilPath = os.path.join(workingPath, dateutilDir)

shutil.rmtree(dateutilPath, True)
shutil.copytree(tempDateutilPath, dateutilPath)
shutil.rmtree(tempPath)
