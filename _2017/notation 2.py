# https://gist.github.com/Phuket2/29c4dcf2216c72d2cf4d87638192a1e3

# https://forum.omz-software.com/topic/4218/source-file-notation-script-share

'''
	****** WRENCH ITEM ******
	create notes for the current source file in the Pythonisita Editor
	This file should be added to the wrench menu, and will be run on the active editor tab
	
	The idea is simple. just sometimes you want to make notes as you working on a file. This
	script just automates creating a sub dir to save a notes file as well as file by the
	same name, but different ext.  The ext can be changed below.
	 
	A dir will be created in the directory of the source file if one does not exit,
	a file by the same base name will created in the new dir if it does not exist.
	Finally the file will open in a new tab in the editor.  
	
	
	The file is created with a header, which you can alter below. Currently, it has the date the
	notes file was created and the full path of the file. The full path ugly, but it could be 
	useful at some point.
	
	** Note **
	There is a var called _copy_to_clip. If this is True, and you have selected text in your
	file, the selected text will copied to the clipboard in anticipation you want to paste it
	into the notes file. 
	I have set _copy_to_clip = False, so it does not hammer your clipboard. Just change it to
	True if you think its a good idea.
	
	I realise more could be done, like a timestamp entry template for entering a note into 
	for example. Just to begin with, this suits my needs.
	Not sure people will like a sub dir being created in there source code folder??
	Because i just tinker, it does not bother me.
	I did look at other ways of having a single folder for all notes, hashing path + file names,
	or recreating the directory structure from the root of the single dir to keep in contact
	with the file, but it seemed like over kill to me.
	
	Not sure anyone other than me will find it useful. Personally, i would love to see this built
	into Pythonista.  i mean, a strong connection to any number of files from any given source
	file.  i dont mean project dependent files (for execution), but notes, maybe images that you have created that sketches out your initial thoughts etc.
	I think this idea will be frowned upon, connecting files to a source file rather than the
	traditional approach of a project list of files and resources.  hmmm, maybe some editors do
	this already, i am not sure.
	
	@Phuket2, Pythonista Forum
	
'''
import datetime
import os
import editor
import clipboard

_notes_suffix = 'md'			# the ext for the created note file.
_notes_sub_dir = 'notations'	# the sub dir the notes will be saved in
_copy_to_clip = False

_creation_date_str = '%I:%M%p on %B %d, %Y'
_file_header_text =\
'''{sep}
#Notation File for Source file {src_name}
source path:{src_path}
This File created : {creation_date}	
{sep}

'''
	
file_path = editor.get_path()
file_name = os.path.basename(file_path)
file_dir = os.path.dirname(file_path)
name, suffix = os.path.splitext(file_name)

target_dir = os.path.join(file_dir, _notes_sub_dir)
target_file = os.path.join(target_dir, '{}.{}'.format(name, _notes_suffix))

if _copy_to_clip:
	# get the selected text in the file, if any
	sel = editor.get_selection()
	selection_text = editor.get_text()[sel[0]:sel[1]]
	if selection_text:
		clipboard.set(selection_text)
		
if not os.path.exists(target_dir):
	os.mkdir(target_dir)
	
if not os.path.exists(target_file):
	'''
		not using editor.make_new_file() here as far as i know you cant control how it opens.
		it opens replacing the current tab, instead of opening in a new tab
		
	'''
	creation_date_str = datetime.datetime.now().strftime(_creation_date_str)
	with open(target_file, 'w') as f:
		f.writelines(_file_header_text.format(src_name=file_name,
												 src_path=file_path,
												 creation_date=creation_date_str,
												 sep='*' * 60))
	
# open the file in the editor
editor.open_file(target_file, True)

# position the cursor at the end of the file
editor.set_selection(len(editor.get_text()))




