# coding: utf-8

# https://forum.omz-software.com/topic/3606/script-to-import-any-file-in-pythonista-from-any-app

import appex
import clipboard
import console
import shutil
import os

import File_Picker # from @omz
dest_dir = File_Picker.file_picker_dialog('Select the folder where you want to save the file', multiple=False, select_dirs=True, file_pattern=r'^.*\.py$')

def getuniquename(filename, ext):
	root, extension = os.path.splitext(filename)
	if ext!='':
		extension = ext
	filename = root + extension
	filenum = 1
	while os.path.isfile(filename):
		filename = '{} {}{}'.format(root, filenum, extension)
		filenum += 1
	return filename
	
def main():
	console.clear()
	dest_path_short = '~/Documents/inbox'
	dest_path = os.path.expanduser(dest_path_short)
	if not os.path.isdir(dest_path):
		print('Create ' + dest_path_short)
		os.mkdir(dest_path)
	if not appex.is_running_extension():
		print('Using clipboard content...')
		text = clipboard.get()
		assert text, 'No text on the clipboard!'
		resp = console.alert('Alert!', 'Choose File Extension', '.py', '.pyui', hide_cancel_button=False)
		if resp==1:
			ext = '.py'
		elif resp==2:
			ext = '.pyui'
		filename=os.path.join(dest_path,'clipboard')
		filename=getuniquename(filename,ext)
		while os.path.isfile(filename):
			filename = '{} {}{}'.format(root, filenum, extension)
			#filenum += 1
		#with open(filename,'w') as f:
			#f.write(text)
		#print('Done!')
			filenum += 1
		with open(filename,'w', encoding='utf-8') as f:
			f.write(text)
		print('Done!')
	else:
		file = appex.get_file_path()
		print('Input path: %s' % file)
		filename=os.path.join(dest_path, os.path.basename(file))
		filename=getuniquename(filename,'')
		shutil.copy(file,filename)
	print('Saved in %s' % dest_path_short)
	if not os.path.exists(filename):
		print(' > Error file %s not found !' % os.path.basename(filename))
	else:
		print(' > as %s' % os.path.basename(filename))
		
if __name__ == '__main__':
	main()

