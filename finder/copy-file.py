#!python2

# coding: utf-8

# https://forum.omz-software.com/topic/2973/file-manager-rename-and-copy-functions/2

import console
import editor
import os
import shutil

DOCUMENTS = os.path.expanduser("~/Documents")

old_name = editor.get_path()
new_name = os.path.join(DOCUMENTS, console.input_alert("Duplicate File", "Enter new name", os.path.relpath(old_name, DOCUMENTS)))

if os.path.exists(new_name):
	console.hud_alert("Destination already exists", "error")
else:
	shutil.copy(old_name, new_name)
	
	##editor.open_file(os.path.relpath(new_name, DOCUMENTS)) # For old Pythonistas
	editor.open_file(new_name)

