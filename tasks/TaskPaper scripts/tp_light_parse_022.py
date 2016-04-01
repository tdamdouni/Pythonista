#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""	Parse TaskPaper text to a list of dictionaries
	using the same property names as Jesse Grosjean's reference parser at
	https://www.npmjs.org/package/foldingtext.

	Parses FT/TaskPaper tags, node types, outline nesting levels
	and parent child relationships,
	but does not parse in-line Markdown formatting.

	Defines one main function:


	get_tp_parse(str_text)


	(parses the text as TaskPaper 3.0 format)


	Aims to produce the same output as the www.foldingtext.com
	reference parser, and later versions will be adjusted to match
	any further changes in that parser.

	Best practice is to use that parser directly
	(available in a draft command line form for TaskPaper 3.0 at
	https://www.npmjs.org/package/foldingtext)

	The reference parser (implemented in Javascript by Hog Bay Software
	and www.foldingtext.com, and copyright Jesse Grosjean)
	additionally provides a powerful query language
	http://www.foldingtext.com/sdk/nodepaths/

	whereas this parser has the following limitations:

	1. It is a provisional draft
	2. it does not directly provide any query language

	This parser is intended simply as a stop-gap for contexts in which
	the use of Javascript is not an option, or where there is a need for
	a simple light-weight parse which is compatible with the output
	of Jesse Grosjean, Hog Bay and www.foldingtext.com's reference parser.
"""

# Copyright Robin Trew 2014
# FoldingText and TaskPaper are copyright Jesse Grosjean and HogBay Software

AUTHOR = 'Rob Trew'
VER = '.022T TaskPaper Only'
LICENSE = """Copyright (c) 2014 Robin Trew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

# Version history
# 2014-03 11 ver 0.21 updated for compatibility with FT2 Dev772, TP Dev124
# 2014-03 12 ver 0.22 if .ft body paras have 2 trailling spaces for MD <br\>
#						the spaces are left in .line but now
#						stripped from .text (as in the reference parser)
# 2014-03 13 ver 0.22T Extracted this TaskPaper-only subset of the code

import re
import sys
import json
import codecs


# Node types in Jesse Grosjean's www.FoldingText.com and TaskPaer parser
TYP_ROOT = 'root'
TYP_EMPTY = 'empty'

# Node types in Jesse Grosjean's TaskPaper format
TYP_PROJ = 'project'
TYP_TASK = 'task'
TYP_NOTE = 'note'

# Node attributes, with corresponding elements in the reference parser's
# Javascript implementation.
# (www.foldingtext.com Jesse Grosjean & HogBay Software)

ATT_ID = 'id' # node.id
ATT_PARENT = 'parentID' # node.parent.id
ATT_LEVEL = 'nestedLevel' # nestedLevel(node)
ATT_CHILD_INDEX = 'childIndex' # node.indexToSelf()
ATT_INDENT = 'typeIndentLevel' # node.typeIndentLevel()
ATT_TYPE = 'type' # node.type()

ATT_LINE_INDEX = 'lineNumber' # node.lineNumber()
ATT_TEXT_INDEX = 'textIndex' # node.lineTextStart()
ATT_TEXT = 'text' # node.text()
ATT_LINE = 'line' # node.line()

ATT_TAG_NAMES = 'tagNames' # Object.keys(node.tags())
ATT_TAGS = 'tags' # node.tags()
# ATT_MODE = 'mode' # node.mode()
# ATT_CONTEXT = 'modeContext' # node.modeContext()

# additional outline node properties
# Ordered ids of all children, first & last members match
#  node.firstChild.id' and node.lastChild.id in the official FT/TP parser
ATT_CHILN = 'chiln'
# List of child indices from top level node down to this node
# [1,3,3] for the 3rd child of the 3rd of the 1st node
ATT_PATH = 'path'

RGX_TP_PRJ = r'^(\t*)([^-\s].*\:)$'

RGX_TP_KEY = r'\s{1}\@(\w+)'
RGX_TP_TAG = r'(^|\s+)@(\w+)(?:\(([^\)]*)\))?(?=\s|$)'


def main():
	""" Testing version: edit variable below for JSON output"""

	bln_json = False

	# Get file string from file specified in run-time argument
	str_text = ''
	lst_args = sys.argv
	if len(lst_args) > 1:
		str_path = lst_args[1]
		with codecs.open(str_path, "r", 'utf8') as myfile:
			str_text = myfile.read()

	if str_text == '':
		return 0

	# PARSE AS TASKPAPER OUTPUT (compatible with TP3.0 Dev (124))
	# A list starting with a virtual root node (id=0) followed by
	# one dictionary for each line of the text (Line 1 id=1, etc)
	# For keys of the dictionaries, and their mapping onto
	# attributes in Jesse Grosjean's Javascript parser,
	# see the ATT_ GLOBAL variables above
	lst = get_tp_parse(str_text)

	if bln_json:
		print json.dumps(lst).encode('utf-8')
	else:
		# FOR TESTING AGAINST THE REFERENCE PARSER - FEED FOR A DIFF

		print lst
		# OUTPUT FOR DIFF TESTING
		# for dct_line in lst[1:]:
		# 	print '\t'.join([str(dct_line[ATT_LEVEL]),
		# 			str(dct_line[ATT_LINE_INDEX]),
		# 			str(dct_line[ATT_TEXT_INDEX]), str(dct_line[ATT_ID]),
		# 			str(dct_line[ATT_PARENT]), str(dct_line[ATT_CHILD_INDEX]),
		# 			dct_line[ATT_TYPE],
		# 			_first_last_child(dct_line),
		# 			# json.dumps(dct_line[ATT_CHILN]),
		# 			json_keys(dct_line[ATT_TAG_NAMES], dct_line[ATT_TAGS]),
		# 			str(dct_line[ATT_INDENT]),
		# 			dct_line[ATT_TEXT], dct_line[ATT_LINE]]).encode('utf-8')

# DIFF FNS

def _first_last_child(dct_line):
	"""just a formatting function for testing """
	lst_chiln = dct_line[ATT_CHILN]
	if lst_chiln:
		if len(lst_chiln) > 1:
			str_chiln = '[' + str(lst_chiln[0]) + r' ' + \
				str(lst_chiln[-1]) + ']'
		else:
			str_chiln = '[' + str(lst_chiln[0]) + r' ' + \
				str(lst_chiln[0]) + ']'
	else:
		str_chiln = '[ ]'
	return str_chiln


def json_keys(lst, dct):
	"""generate ordered json sequence for testing"""
	if lst:
		_str = '{'
		for str_key in lst:
			_str += ''.join(['"', str_key, '":"', dct[str_key], '",'])
		str_json = _str[:-1] + "}"
	else:
		str_json = "{}"
	return str_json

def set_levels(lst_all, lst_chiln, lng_level):
	"""Top down recursive setting of nesting levels"""
	lng_next = lng_level + 1
	for id_child in lst_chiln:
		dct_child = lst_all[id_child]
		dct_child[ATT_LEVEL] = lng_level
		lst_next = dct_child[ATT_CHILN]
		if lst_next:
			set_levels(lst_all, lst_next, lng_next)

	return lst_all


# ******* TOP LEVEL PARSING FUNCTION HERE ********

def get_tp_parse(str_text):
	""" Parse as TaskPaper
		Return a list of dictionaries with key:values compatible
		with Jesse Grosjean's reference parser
	"""

	def _set_levels(lst_all, lst_chiln, lng_level):
		"""Top down recursive setting of nesting levels"""
		lng_next = lng_level + 1
		for id_child in lst_chiln:
			dct_child = lst_all[id_child]
			dct_child[ATT_LEVEL] = lng_level
			lst_next = dct_child[ATT_CHILN]
			if lst_next:
				_set_levels(lst_all, lst_next, lng_next)

		return lst_all

	# READ THE NODE TYPES, THEN DETERMINE THE PATTERN OF NESTING,
	# and return a list of dictionaries includinng id, ParentID, & child ids
	lst = add_parent_child(
		outline_nodes(
			str_text))
	return _set_levels(lst, lst[0][ATT_CHILN], 1)



def outline_nodes(str_in):
	""" Read a TaskPaper text outline to a list of attribute dicts
	"""

 # TASKPAPER REGEX REQUIREMENTS ARE SIMPLER THAN MARKDOWN
	rgx_body = re.compile(r'(\t*)([^\t]*.*)$')
	rgx_tp_tsk = re.compile(r'^(\t*)(\-\s.*)$')
	rgx_tp_prj = re.compile(r'^(\t*)(\s*)([^-\s].*\:)$')

	def _read_tags(dct_node):
		""" Store the key-value pairs and key list
			and return text leaving in-line tags in place
			but pruning off any tags at the end of the line
		"""
		str_text = dct_node[ATT_TEXT]

		bln_mode = False
		str_point = str_text

		# and then digest all tags, right to left, eating terminal tags.
		str_s_point = str_point.rstrip()
		i_end = len(str_s_point)
		lst_keys = []
		lst_not_duplicate = []
		rgx_tag = re.compile(RGX_TP_TAG)
		lst_matches = [_ for _ in rgx_tag.finditer(str_s_point)]
		for o_match in lst_matches:
			str_key = o_match.group(2)
			# Valid key assignment ? or a duplicate ?
			if str_key not in lst_keys:
				lst_keys.append(str_key)
				var_value = o_match.group(3)
				if var_value != None: #treat simple keys as boolean flags
					dct_node[ATT_TAGS][str_key] = var_value
				else:
					dct_node[ATT_TAGS][str_key] = ''
				lst_not_duplicate.append(True)
			else:
				lst_not_duplicate.append(False)

		# and now shed any string of non-duplicate tags from the end
		for i in reversed(range(len(lst_matches))):
			o_match = lst_matches[i]
			if lst_not_duplicate[i]:
				if i_end == o_match.end():
					i_end = o_match.start()
				else:
					break
			else:
				break


		# store any keys in textual order,
		lng_keys = len(lst_keys)
		if lng_keys:
			if lng_keys > 1:
				dct_node[ATT_TAG_NAMES] = lst_keys
			else:
				dct_node[ATT_TAG_NAMES] = lst_keys
			# and assign any remaining text
		if bln_mode or lng_keys:
			dct_node[ATT_TEXT] = str_s_point[0:i_end]


	def _set_tp_node(dct_node, var_type, o_match):
		"""set TP node properties by reference"""
		bln_empty = False
		if var_type != TYP_NOTE:
			dct_node[ATT_TYPE] = var_type
			if var_type != TYP_PROJ:  # strip prefix
				dct_node[ATT_TEXT] = o_match.group(2)[2:]
			else:	# or suffix
				dct_node[ATT_TEXT] = o_match.group(2) + o_match.group(3)[:-1]
		else:
			# str_text = dct_node[ATT_LINE].lstrip()
			dct_node[ATT_TEXT] = dct_node[ATT_TEXT].lstrip()
			if dct_node[ATT_LINE].lstrip() == '':
				dct_node[ATT_TYPE] = TYP_EMPTY
				bln_empty = True

		if not bln_empty:
			lng_indent = len(o_match.group(1))
			if lng_indent:
				dct_node[ATT_INDENT] = lng_indent

	str_vanilla = TYP_NOTE


	lst_nodes = [
		{ATT_ID:0, ATT_PARENT: None, ATT_LEVEL:0,
			ATT_CHILD_INDEX: None, ATT_INDENT:None, ATT_TYPE:TYP_ROOT,
			ATT_LINE_INDEX:None, ATT_TEXT_INDEX:None, ATT_TEXT:'',
			ATT_LINE:'', ATT_TAG_NAMES:[], ATT_TAGS:{},
			ATT_CHILN:[], ATT_PATH:[]}
	] + [
		{ATT_ID:i+1, ATT_TYPE:str_vanilla, ATT_LINE:str_line,
			ATT_LINE_INDEX:i, ATT_TEXT:str_line, ATT_INDENT:0, ATT_TAGS:{},
			ATT_LEVEL:0, ATT_TAG_NAMES:[], ATT_CHILN:[], ATT_PATH:[]}
		for i, str_line in
			enumerate(str_in.splitlines())
	]


	# MAIN PARSE LOOP TO DERIVE TYPE, AND OTHER ATTRIBUTES OF EACH NODE

	lng_txt = 0
	for dct_node in lst_nodes[1:]:
		# Maintain an index into the text
		# (Note that [ATT_ID] serves as a 1-based index to the lines)
		dct_node[ATT_TEXT_INDEX] = lng_txt

		str_point = dct_node[ATT_LINE]
		lng_chars = len(str_point)
		lng_txt += (lng_chars + 1) # splitlines is dropping \n

		# IDENTIFY THE INDENT COUNT & NESTING LEVEL
		# Assume Note text until there is counter-evidence
		if lng_chars < 1:
			dct_node[ATT_TYPE] = TYP_EMPTY
		else:
			_read_tags(dct_node)
			str_point = dct_node[ATT_TEXT]
			o_match = rgx_tp_prj.match(str_point)

			if o_match != None:
				_set_tp_node(dct_node, TYP_PROJ, o_match)
			else:
				o_match = rgx_tp_tsk.match(str_point)
				if o_match != None:
					_set_tp_node(dct_node, TYP_TASK, o_match)
				else:
					o_match = rgx_body.match(str_point)
					if o_match != None:
						_set_tp_node(dct_node, TYP_NOTE, o_match)
					else:
						print "Unexpected TP pattern:" + str_point


		# Now that we know the provisional type of each node,
		# digest any infixed or postfixed tags
		# DETECT ANY REMAINING EMPTIES BEFORE WE TAKE OUT MODES & TAGS
		if dct_node[ATT_TYPE] != TYP_EMPTY:
			str_line = dct_node[ATT_LINE]
			str_rs_line = str_line.rstrip()
			if str_rs_line == '':
				dct_node[ATT_TEXT] = ''
				if dct_node[ATT_TYPE] == TYP_NOTE:
					dct_node[ATT_TYPE] = TYP_EMPTY

	return lst_nodes

def add_parent_child(lst_lines):
	"""Add ParentID and ChildIDs to each node"""

	lst_tab_parents = [0]
	lst_blanks = []

	for dct_line in lst_lines[1:]:
		lng_id = dct_line[ATT_ID]
		var_type = dct_line[ATT_TYPE]

		if var_type != TYP_EMPTY:
			lng_indent = dct_line[ATT_INDENT]
			lng_next_level = lng_indent+1

			lng_over_indent = ((lng_next_level+1) - len(lst_tab_parents))
			if lng_over_indent > 0:
				id_parent = lst_tab_parents[-1]
				while lng_over_indent:
					lst_tab_parents.append(lng_id)
					lng_over_indent -= 1
			else:
				id_parent = lst_tab_parents[lng_indent]

			# This node becomes the parent for ALL deeper indented
			# nodes
			for i in range(lng_indent+1, len(lst_tab_parents)):
				lst_tab_parents[i] = lng_id


			# Record the parent/child relationships, and derive a path
			dct_line[ATT_PARENT] = id_parent
			dct_parent = lst_lines[id_parent]

			# FIRST MOP UP ANY PRECEDING BLANKS
			# MAKE THEM PEERS OF THIS NON-BLANK NODE
			if lst_blanks:
				for id_blank in lst_blanks:
					dct_parent[ATT_CHILN].append(id_blank)
					dct_blank = lst_lines[id_blank]
					dct_blank[ATT_PARENT] = id_parent
					dct_blank[ATT_INDENT] = dct_line[ATT_INDENT]
					dct_blank[ATT_CHILD_INDEX] = len(dct_parent[ATT_CHILN]) - 1
				lst_blanks = []

			# THEN LINK THIS NODE TO ITS PARENT
			# RECORD ITS CHILD INDEX
			# AND BUILD A UNIQUE PATH FOR IT
			dct_parent[ATT_CHILN].append(lng_id)
			i_index = len(dct_parent[ATT_CHILN]) - 1
			dct_line[ATT_CHILD_INDEX] = i_index
			dct_line[ATT_PATH] = dct_parent[ATT_PATH] + [i_index]


		else: # (blank line)
			# set TEMPORARY parent
			# and then push onto stack to wait for next non-empty node,
			# from which it will take its final level
			dct_line[ATT_PARENT] = lst_tab_parents[0]
			lst_blanks.append(lng_id)

	# Finalise the parenthood of any remaining blanks
	if lst_blanks:
		dct_parent = None
		for id_blank in lst_blanks:
			dct_blank = lst_lines[id_blank]
			if dct_parent == None:
				dct_parent = lst_lines[dct_blank[ATT_PARENT]]

			dct_parent[ATT_CHILN].append(id_blank)
			dct_blank[ATT_CHILD_INDEX] = len(dct_parent[ATT_CHILN]) - 1
		lst_blanks = []

	return lst_lines




main()
