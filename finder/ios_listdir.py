from __future__ import print_function
#		iOS listdir (Python)
			
#			I wrote this little Pythonista script to discover the iOS file structure, using a few Unix commands.
# 
#			Use 'cd' to change the directory, for example: 'cd Applications'
#			'cd /' to return to root
#			Type 'exit' to stop the script.

# 		Future updates: Using 'cd ..' to go back one level.


import os
import console

def main():
	
	console.clear()

	root = os.listdir('/')

	for i in root:
		print('/' + i)
		
	currentpath = ''
	newpath = '/'
	
	while True:	
		newcmd = raw_input('\niPhone:' + newpath + ' $ ')
		print('')
	
		if newcmd[0:2] == 'cd':
			newpath = newcmd[3:]
		elif newcmd == 'exit':
			console.clear()
			break
			
		if newpath == '/':
			currentpath = ''
			newpath = '/'
			
			for i in root:
				print('/' + i)
			
		else: 
			try: 	
				path = os.listdir(currentpath + '/' + newpath)
	
				for p in path:
					print(currentpath + '/' + newpath + '/' + p)
				
				currentpath = currentpath + '/' + newpath
					
			except OSError as xxx_todo_changeme:
				(errno, strerror) = xxx_todo_changeme.args
				print("{1} - (OSError {0})".format(errno, strerror))
		
if __name__ == '__main__':
	main()
