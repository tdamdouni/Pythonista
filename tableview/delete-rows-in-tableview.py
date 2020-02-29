# coding: utf-8

# https://forum.omz-software.com/topic/2733/delete-rows-in-tableview/2

from __future__ import print_function
import ui

def tableview_delete(tableview, section, row):
	# Called when the user confirms deletion of the given row.
	print('in delete', tableview, section, row)
# load
v = ui.load_view('Table.pyui')
tbl = v['tbl']          # get a ref to the table in the form

# replace the tableview_delete function
tbl.data_source.tableview_delete = tableview_delete
v.present('sheet')

