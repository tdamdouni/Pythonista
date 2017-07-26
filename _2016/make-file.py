# https://forum.omz-software.com/topic/3776/making-files-with-python-script

from sys import argv

filename=input()
target=open(filename,'w') #open it for writing, as opposed to reading.
target.write('hello')
target.close()
