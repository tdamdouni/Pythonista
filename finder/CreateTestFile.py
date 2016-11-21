# coding: utf-8

# https://forum.omz-software.com/topic/2427/share-code-create-a-py-file-in-a-dir-from-tools-menu

# Ok, some more trivial code to share. This is for the tools menu. All it does is create a temp file in a directory , if you want with some text inserted in the file, you can also do. Then it opens up the newly created file in the editor (sorry, it replaces the active tab, I looked, but I don't think I can change that). While its a temp file, it does not get deleted (using NamedTemporaryFile with delete = False). I often want to try new things and need a type of scratch pad. This script basically gives you this functionality. It's important to me, because so often I just create a file in the dir I am in and call it test.py or crap.py etc.. I just screw up my project directory with lots of crap files for testing something.
# I tried to write this with some care to errors.
# Personally, I would love to see a framework you have to write to when publishing scripts for the tools menu. Whilst I can grasp and understand the concepts of these type of frameworks, it's beyond me to write one.
# But I think the tools menu is trivialised because of this. Again, I could be wrong as I often am 😁

# https://gist.github.com/Phuket2/89535a038f5d954d5c6a

# *** DISCLAIMER PLEASE READ ***
# please understand, i am a newbie. being a newbie,
# my code may be crap or worse buggy
# i still like to share. it could be useful code.
# or parts of could be useful
# but i like the feedback


'''
        NOTES:
        meant to be run from the tools menu....
        the idea is to create a .py file
        fast in a known location.

        You can use **my_std_script** var to write some code to the
        file if you like.
        LOL , it would be so nice if markdown worked
        inside python comments :)

        REASON:
        So often i want to test something in a new .py,
        i often create a new file in the project dir i am
        wirking on, called crap.py or test.py or something.
        Pollutes my project directory.

        This is only for those .py files you want to create,
        use and forget.

        Some point you should go back into the target directory all delete
        its contents. the temp file created will not be automactially
        deleted!

'''

import os, sys
import tempfile
import editor, console


# assumes this directory will reside in
# the site_packages directory.
_temp_dir_name = 'TestFiles'

# the base dir where the temp_dir_name is
# created if it does exist...
# you will be prompted, before a dir is created
_base_dir = '{}/Documents/{}'.format(os.path.expanduser('~'),
                                        'site-packages')

# my_std_script, is written to the new file
# can also set my_std_script = '', nothing will be
# written to the file

my_std_script ='''
# coding: utf-8

import ui


class MyClass(object):
        def __init__(self):
                pass



if __name__ == '__main__':
        print 'in main...'

'''

# uncomment the line below, if you want nothing written
# to the temp file...
#my_std_script = ''

_target_dir = '''{0}/{1}/'''.format(_base_dir, _temp_dir_name)


# make sure the target dir exists
if not os.path.isdir(_target_dir):
	result = console.alert(title = 'Directory Does Not Exist',
	message = 'the target_dir, does not exist!',
	button1 = 'Make Dir')
	
	# Cancel button exits, so no check required.
	try:
		os.mkdir(_target_dir)
	except OSError as err:
		raise OSError(err.message, err.args, err.filename)
		
		
try:
	with tempfile.NamedTemporaryFile(mode = 'w',
	dir = _target_dir,
	suffix = '.py',
	delete = False) as f:
		f.write(my_std_script)
		name = f.name
		
except Exception as err:
	raise Exception(err.message, err.args)
	
	
editor.open_file(name)

