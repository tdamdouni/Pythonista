# coding: utf-8

# [Capitalize Workflow - Run Python Code](https://forum.omz-software.com/topic/2421/return-ticket-from-editorial-to-texttool-back-to-editorial)

from __future__ import print_function
import workflow
import editor
import os

action_in = workflow.get_input()

#TODO: Generate the output...
action_out = action_in

path = editor.get_path()
p, file_name = os.path.split(path)
doc_drop = os.path.split(p)[1]
data = editor.get_file_contents(file_name, doc_drop).split(". ")
print(data)
print([x.capitalize() for x in data])
editor.set_file_contents(file_name, ". ".join([x.capitalize() for x in data]), doc_drop)
editor.reload_files()

workflow.set_output(action_out)
