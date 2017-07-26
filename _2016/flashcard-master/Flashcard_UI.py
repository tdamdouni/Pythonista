# coding: utf-8

# https://github.com/polymerchm/flashcard

""" Flashcard Program

written by Steven K. Pollack
           July 18, 2014
           modified August 15, 2014

This script is designed to display a set of image and/or their descriptions from files organized
in a set of folders (chapters)

The program will display a set of selectors for the chapters (picture directories)
The program allows either the descriptor, derived form the name of the file, the image, image or
text randomly, or both to be displayed randomly for study purposes.  The associated chapter will be
highlighted during display.

Alternatively, the entire picture collection can be displayed in alphabetical order as a visual
dictionary.  A picture can have multiple desciptors.  To accomplish this, the file name should be
the descriptors separated by commas.  For example:

        motor, engine.jpg
        to run, to jog.png

The folders and their files are imported into the pythonista "file structure" under a single folder


View Components

Flash_Dict.pyui

        dict_list_window
        button_dict_back
        dict_flashcard
        button_a, button_b,....... added programmatically

Flashcard_UI.pyui

        chapter_list
        Image (label)
        text(label)
        both(label)
        random(label)
        sw_image, sw_text, sw_bpth, sw_random (acting as a radio button group)
        button_next
        button_answer
        button_dict
        text_field
        flashcard

"""

import os, os.path, sys, Image, random, ui, re, math



#####################################
# all alphabetical sorts of the descriptors of images have "noise words" removed before sorting

noise=["to be ", "to ", "the ", "a ", "an "]

def de_noise(descriptor): # string or list.  if a list, assumes the first entry is a descriptor string.
	if isinstance(descriptor,basestring):
		sortitem  = descriptor.lower()
	else:
		sortitem = descriptor[0].lower()
	for item in noise:
		res =  re.split("^%s" % item,sortitem) # search for noise strings (anchored at start)
		if len(res) == 2:
			return res[1]
# if no matches, return original
	return sortitem
	
	
###############################
#  View Mode Radio Button Group

def on_mode_switch(switch): # choose display mode.  Force group of buttons to act as a radio button
	global current_mode, flashView
	
	for sw in switch_array_index:
		flashView[sw].value = False
	switch.value = True
	current_mode = switch.name
	
	
	
############################################################################################
# Next Button: the heart of the program, picks next image according to the radion button and
# chapter selections then displays accordingly

def on_next(button):
	global fullname, basename, current_mode, now_mode, answered, selected, chapter_dir_dict
	global flashView, highlight, prev_highlight
	
	if selected and answered: # don't advance if answer wasn't displayed or no chapters selected
		dir_index =  random.randint(0,len(selected)-1) # random chapter index from selected list
		dirname = chapter_names_list[selected[dir_index]]
		highlight = selected[dir_index]  # set chapter to hightlight
		if highlight != prev_highlight: # don't bother if its the same chapter'
			flashView['chapter_list'].reload_data()
		prev_highlight = highlight
		(path, image_list, image_pointer_list, image_pointer_index) = chapter_dir_dict[dirname]
		try:
			imagename = image_list[image_pointer_list[image_pointer_index]]
		except:
			image_pointer_index = 0 # finished current list resort arnd restart
			random.shuffle(image_pointer_list)
			imagename = image_list[image_pointer_list[0]]
			
		image_pointer_index += 1
		chapter_dir_dict[dirname] = (path, image_list, image_pointer_list, image_pointer_index)
		fullname = os.path.join(path,imagename)
		(basename,ext) = os.path.splitext(imagename)
		now_mode = current_mode
		text_field = flashView['text_field']
		image = flashView['flashcard']
		if (now_mode == "sw_random"):
			now_mode = random.choice(["sw_image","sw_text"])
		if now_mode in ["sw_text","sw_both"]:
			text_field.text = basename
		else:
			text_field.text = "  "
		if now_mode in ["sw_image", "sw_both"]:
			image.image = ui.Image.named(fullname)
		else:
			image.image = ui.Image.named('blank.jpg')
		if now_current == "sw_both":
			answered = True
			flashView['button_answer'].enabled = False
		else:
			answered = False
			flashView['button_answer'].enabled = True
			flashView['button_next'].enabled = False
			
##############################
# Answer Button

def on_answer(button): # displays the text or image (unless in both mode, then disbled)
	global flashView, answered, now_mode
	
	try:
		if (now_mode == "sw_image"):
			flashView['text_field'].text = basename
		elif (now_mode == 'sw_text'):
			flashView['flashcard'].image = ui.Image.named(fullname)
		answered = True
		flashView['button_next'].enabled = True
		flashView['button_answer'].enabled = False
	except:
		pass
		
		
########################
# Action on Dictionary Button
def on_dictionary(button):
	global navView, dictView
	
	navView.push_view(dictView)
	
	
#######################################################
#######################################################
# dictionary view mode call back routines

########################
# Action on dictionary back button
def on_dict_back(button):
	global navView
	
	navView.pop_view()
	
	
##############################
# Action for word list

def on_word_select(wordtable):
	global dictView
	
	row = wordtable.selected_row
	file = dictItems_list[row]['fname']
	chapter = dictItems_list[row]['chapter']
	filePath = os.path.join(root_dir_path,chapter,file)
	dictView['dict_flashcard'].image = ui.Image.named(filePath)
	
###############################
# word list section jump  button

def on_word_jump(button):
	global dictItems_list_alpha, dictTableView
	
	offset = dictItems_list_alpha[button.title]
	dictTableView.content_offset = (0,dictTableView.row_height*offset)
	dictTableView.reload()
	
	
#################################
### Turn on/off all chapters

def     on_select_all_none(button):
	global flashView,selected
	
	tableView = flashView['chapter_list']
	if button.title == 'Select All':
		next_button_name = 'Select None'
		selected = range(len(tableView.data_source.items))
		state = 'checkmark'
	elif button.title == 'Select None':
		next_button_name ='Select All'
		state = 'none'
		selected = []
		
	for index in range(len(tableView.data_source.items)):
		tableView.data_source.items[index]['accessory_type'] = state
	tableView.reload_data()
	button.title = next_button_name
	
	
	
##########################################
##### Chapter list object, data_source and delegate routines
class FlashcardDataSource(object):
	global highlight
	
	def __init__(self,items):
		self.items = items
		
##############################
# Chapter ListView Select

	def isChecked(self,row): # is a checkbox set in a tableview items attribute
		return self.items[row]['accessory_type'] == 'checkmark'
		
#####################################################################
# Support routine to switch checkmark on and off in table view entry

	def toggleChecked(self,row):
		if self.isChecked(row):
			self.items[row]['accessory_type'] = 'none'
		else:
			self.items[row]['accessory_type'] = 'checkmark'
			
##############################################
# action for chapter select in flashcard mode

	def tableview_did_select(self,tableView,section,row):
		global selected
		
		self.toggleChecked(row)
		tableView.reload_data()
# rebuild selected list based on changes to tableview
		selected = [index for index in range(len(self.items)) if self.isChecked(index)]
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]['title']
		if row == highlight:
			cell.text_label.text_color = 'red'
		cell.accessory_type = self.items[row]['accessory_type']
		return cell
		
#########################################################
#########################################################
#
# Main program


# changed to be same folder as the program

root_dir_path = 'ASL'       # the root directory for the "chapter folders"

chapter_dir_dict = {}
basename = fullname = ''
image_type = ('.png', '.jpg') #forces image files only.  add other extensions you might use

try:
	chapter_dirList=os.listdir(root_dir_path) # directory names for set of flashcards
except OSError as e:
	print('ERROR: No ASL directory of flashcards found.\n\n{}'.format(e))
	sys.exit()
	
chapter_dirs = [fname for fname in chapter_dirList if ((fname[0] != '.') and
                (os.path.isdir(os.path.join(root_dir_path,fname))))] # filter out non-valid directories


picture_chap_list = []
for chapter_dirname in chapter_dirs: # walk through chapter folders
	fullpath = os.path.join(root_dir_path,chapter_dirname)
	filelist = os.listdir(fullpath)             # file names in curent chapter
	
	picture_files = [fname for fname in filelist if os.path.splitext(fname)[1] in image_type]
	for picture in picture_files:
		descrip = os.path.splitext(picture)[0]
		terms = re.split(",",descrip) # split the descptor into multiple terms if comma separatated
		for term in terms:
			picture_chap_list.append((term.lstrip(),picture,chapter_dirname)) # make an entry for each term
			
# have name of all valid picture files
#
# instead of a random pick from the names, we force all pctures to be viewed only once using a randomized
# index list

	if picture_files:
		picture_index = range(len(picture_files))  # indexes into the picture list
		random.shuffle(picture_index)              # randomized
		chapter_pointer = 0                        # pointer to the randomized index
		chapter_dir_dict[chapter_dirname] = (fullpath, picture_files, picture_index, chapter_pointer)
		
# Now have the directories and picture names in the hash

picture_chap_list =  sorted(picture_chap_list, key=de_noise) # also all pictures in alphabetical order

chapter_names_list = sorted(chapter_dir_dict.keys())


blank_image = Image.new("RGBA", (500, 500), "white").save('blank.jpg')

rootView = ui.View()
rootView.background_color = 'white'
navView = ui.NavigationView(rootView) # stack of views
navView.navigation_bar_hidden = True
flashView = ui.load_view('Flashcard_UI.pyui')
flashView['button_answer'].enabled = True

# set up subviews for flashview

switch_array_index = ['sw_image', 'sw_text', 'sw_both', 'sw_random']
for index in switch_array_index:
	flashView[index].action = on_mode_switch
	flashView[index].value = False
flashView['sw_image'].value = True # default

flashView['button_next'].action = on_next
flashView['button_answer'].action = on_answer

tableView = flashView['chapter_list']
items_list = [{'title':chapter,'accessory_type':'none' } for chapter in chapter_names_list]
flashDataSource = FlashcardDataSource(items_list)
tableView.data_source = tableView.delegate = flashDataSource
flashView['button_select_all'].enabled = True
flashView['button_select_all'].action = on_select_all_none
flashView['button_select_all'].title = 'Select All'
flashView['button_answer'].enabled = False
flashView['button_next'].enabled =True
flashView['button_dict'].enabled = True
flashView['button_dict'].action = on_dictionary

Vimage = flashView['flashcard']
Vimage.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
Vimage.image = ui.Image.named('blank.jpg')


###############################
# set up dictView

dictView = ui.load_view('Flash_Dict.pyui')
dictTableView = dictView['dict_list']

dictItems_list = [{'title':word, 'fname': fname, 'chapter': chapter} for
              word, fname, chapter in picture_chap_list]

################################
# This section creates a set of buttons and links them to a pointer to the first instance of a descriptor
# starting with the next letter in the alphabet.  It work like the section index in iOS

dictItems_list_alpha = {}
current_letter = None
numbers_flag = False
for count,item in enumerate(dictItems_list):
	title = de_noise(item['title'].lower())
	if title[0] != current_letter:
		if re.match('\d',title[0]): # special case for any digit
			if not numbers_flag:
				dictItems_list_alpha['#'] = count
				numbers_flag = True
		else:
			current_letter = title[0]
			dictItems_list_alpha[current_letter] = count
			
num_keys = len(dictItems_list_alpha)
key_height = int(math.floor(dictTableView.height/(num_keys-1)))
button_offset = dictTableView.width + 100


for count,letter in enumerate(sorted(dictItems_list_alpha.keys())):
	button = ui.Button()
	dictView.add_subview(button)
	button.name = "button_%s" % letter
	button.title = letter
	button.frame = (button_offset, key_height*(count+1),24,24)
	button.action = on_word_jump
	
	
	
dictTableView.data_source.items = dictItems_list
dictTableView.data_source.action = on_word_select

dictView['dict_flashcard'].content_mode = ui.CONTENT_SCALE_ASPECT_FIT

dictView['button_dict_back'].enabled = True
dictView['button_dict_back'].action = on_dict_back

answered = True
current_mode = 'sw_image'
now_current = current_mode
selected = [] # a list containing the index of each selected chapter (folder)
highlight = prev_highlight = -1

navView.push_view(flashView)
navView.present('full_screen')

