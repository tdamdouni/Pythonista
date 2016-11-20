# https://forum.omz-software.com/topic/3499/simple-file-download/6

import console
import dialogs
import appex
import os.path
import urllib.request, urllib

#Make a downloads directory
os.chdir(os.path.expanduser('~'))
os.chdir(os.path.join(os.getcwd(),'Documents'))

test = os.path.isdir('Downloads')
print(test)

if test == False:
	print('Downloads created')
	os.makedirs('Downloads')
else:
		print('Downloads exists')

print('Change dir to Downloads')

os.chdir(os.path.join(os.getcwd(),'Downloads'))

#Test if running as extenstion
test = appex.is_running_extension()

if test == True:
	filein = appex.get_url()
else:
	myrun = dialogs.alert('Manual entry?', '','Enter manual URL',"Dummy")

if myrun == 1:
	filein = input("Enter the URL address of file to get:")

else:
	filein = "https://raw.githubusercontent.com/grrrr/py/741ba0500bc49e8f6268f02d23e461649e8d457b/scripts/buffer.py"

fileparse = urllib.parse.urlparse(filein)
filepath,filename = os.path.split(fileparse.path)

fin = urllib.request.urlopen(filein)

fout = open(filename,'w')

fout.truncate()

bytemyfile = fin.read()
myfile = bytemyfile.decode("utf-8")
fout.write(myfile)
print (myfile)

fin.close()
fout.close()
