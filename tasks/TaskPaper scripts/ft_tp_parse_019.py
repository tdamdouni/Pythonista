#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Parse TaskPaper or www.FoldingText.com text to a list of dictionaries
	using the same property names as Jesse Grosjean's reference parser at
	https://www.npmjs.org/package/foldingtext.

	Parses FT/TaskPaper tags, node types, outline nesting levels
	and parent child relationships,
	but does not parse in-line Markdown formatting.

	Defines two functions:

	1. is_tp(str_text)

		Returns True if the text appears to be in TaskPaper format.
		(Otherwise, the www.FoldingText.com FoldingText MD format is assumed)

	2. get_ft_tp_parse(str_text, bln_is_tp)

		Depending on the boolean value of bln_is_tp,
		parses the text either as TaskPaper 3.0 format
		or as FoldingText 2.0 format

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
	2. it does not support any query language
	3. it only parses node types, tags, nesting, and ft mode flags.
		(it attempts no parsing of inline Markdown formatting)

	This parser is intended simply as a stop-gap for contexts in which
	the use of Javascript is not an option, or where there is a need for
	a simple light-weight parse which is compatible with the output
	of Jesse Grosjean, Hog Bay and www.foldingtext.com's reference parser.


"""

# Copyright Robin Trew 2014
# FoldingText and TaskPaper are copyright Jesse Grosjean and HogBay Software

AUTHOR = 'Rob Trew'
VER = '.019'
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


import re
import sys
import json
import codecs


# Node types in Jesse Grosjean's www.FoldingText.com dialect of Markdown
TYP_ROOT = 'root'
TYP_HEAD = 'heading'
TYP_UNORD = 'unordered'
TYP_ORD = 'ordered'
TYP_BODY = 'item'
TYP_QUOTE = 'blockquote'
TYP_CODE = 'codeblock'
TYP_LINK = 'linkdef'
TYP_PROP = 'property'
TYP_TERM = 'term'
TYP_DEFN = 'definition'
TYP_RULE = 'horizontalrule'
TYP_EMPTY = 'empty'

# Node types in Jesse Grosjean's TaskPaper format
TYP_PROJ = 'project'
TYP_TASK = 'task'
TYP_NOTE = 'note' # temporarily 'comment' in current build of TaskPaper 3.0

SET_MODE_TYPES = set([TYP_HEAD, TYP_EMPTY, TYP_UNORD, TYP_ORD, TYP_BODY])
SET_BLANK_TYPES = set([TYP_EMPTY, TYP_RULE])
SET_TAGLESS = set([TYP_EMPTY, TYP_CODE])

# Node attributes, with corresponding elements in the reference parser's
# Javascript implementation.
# (www.foldingtext.com Jesse Grosjean & HogBay Software)

ATT_ID = 'id' # node.id
ATT_PARENT = 'parentID' # node.parent.id
ATT_TEXT = 'text' # node.text()
ATT_LINE = 'line' # node.line()
ATT_LINE_INDEX = 'lineNumber' # node.lineNumber()
ATT_LEVEL = 'nestedLevel' # nestedLevel(node)
ATT_TAG_NAMES = 'tagNames' # Object.keys(node.tags())
ATT_TAGS = 'tags' # node.tags()
ATT_TEXT_INDEX = 'textIndex' # node.lineTextStart()
ATT_TYPE = 'type' # node.type()
ATT_INDENT = 'typeIndentLevel' # node.typeIndentLevel()
ATT_CHILD_INDEX = 'childIndex' # node.indexToSelf()
ATT_MODE = 'mode' # node.mode()
ATT_CONTEXT = 'modeContext' # node.modeContext()

# additional outline node properties
# Ordered ids of all children, first & last members match
#  node.firstChild.id' and node.lastChild.id in the official FT/TP parser
ATT_CHILN = 'chiln'
# List of child indices from top level node down to this node
# [1,3,3] for the 3rd child of the 3rd of the 1st node
ATT_PATH = 'path'

RGX_MD_HDR = r'^(\#+)\ ?(.*)[\#\s]*$'
RGX_TP_PRJ = r'^(\t*)([^-\s].*\:)$'

RGX_MODE_END = r'\.(\w+)$'
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

	# TEST WHETHER THE INPUT STRING IS TASKPAPER,
	# ASSUME FOLDINGTEXT OTHERWISE, AND ATTEMPT A STANDARD PARSE
	# TO A LIST OF DICTIONARIES USING JESSE GROSJEANS ATTRIBUTE NAMES

	# NB THE CURRENT TASKPAPER 3.0 FLAGS NOTES AS TYPE 'comment'
	# BUT THIS IS CHANGING TO TYPE 'note' IN THE NEXT BUILD

	bln_is_tp = is_tp(str_text)

	lst = get_ft_tp_parse(str_text, bln_is_tp)

	if bln_json:
		print json.dumps(lst).encode('utf-8')
	else:
		# FOR TESTING AGAINST THE REFERENCE PARSER - FEED FOR A DIFF

		print lst

		# OUPUT FOR DIFF TESTING
		# for dct_line in lst[1:]:
		# 	print '\t'.join([str(dct_line[ATT_LEVEL]),
		# 			str(dct_line[ATT_LINE_INDEX]),
		# 			str(dct_line[ATT_TEXT_INDEX]), str(dct_line[ATT_ID]),
		# 			str(dct_line[ATT_PARENT]), str(dct_line[ATT_CHILD_INDEX]),
		# 			dct_line[ATT_MODE],
		# 			dct_line[ATT_TYPE],
		# 			_first_last_child(dct_line),
		# 			dct_line[ATT_CONTEXT],
		# 			# json.dumps(dct_line[ATT_CHILN]),
		# 			json_keys(dct_line[ATT_TAG_NAMES], dct_line[ATT_TAGS]),
		# 			str(dct_line[ATT_INDENT]),
		# 			dct_line[ATT_TEXT], dct_line[ATT_LINE]]).encode('utf-8')

# # DIFF FNS

# def _first_last_child(dct_line):
# 	"""just a formatting function for testing """
# 	lst_chiln = dct_line[ATT_CHILN]
# 	if lst_chiln:
# 		if len(lst_chiln) > 1:
# 			str_chiln = '[' + str(lst_chiln[0]) + r' ' + \
# 				str(lst_chiln[-1]) + ']'
# 		else:
# 			str_chiln = '[' + str(lst_chiln[0]) + r' ' + \
# 				str(lst_chiln[0]) + ']'
# 	else:
# 		str_chiln = '[ ]'
# 	return str_chiln


# def json_keys(lst, dct):
# 	"""generate ordered json sequence for testing"""
# 	if lst:
# 		_str = '{'
# 		for str_key in lst:
# 			_str += ''.join(['"', str_key, '":"', dct[str_key], '",'])
# 		str_json = _str[:-1] + "}"
# 	else:
# 		str_json = "{}"
# 	return str_json

# def set_levels(lst_all, lst_chiln, lng_level):
# 	"""Top down recursive setting of nesting levels"""
# 	lng_next = lng_level + 1
# 	for id_child in lst_chiln:
# 		dct_child = lst_all[id_child]
# 		dct_child[ATT_LEVEL] = lng_level
# 		lst_next = dct_child[ATT_CHILN]
# 		if lst_next:
# 			set_levels(lst_all, lst_next, lng_next)

# 	return lst_all




# ******* TOP LEVEL PARSING FUNCTION HERE ********

def get_ft_tp_parse(str_text, bln_tp):
	""" Parse either at FoldingText or TaskPaper
		Return a list of dictionaries with key:values compatible
		with Jesse Grosjean's reference parser

		[ use is_tp(str_text) to detect the format of unknown source ]
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
			str_text, bln_tp), bln_tp)
	return _set_levels(lst, lst[0][ATT_CHILN], 1)



def outline_nodes(str_in, bln_tp):
	""" Read an MD or TP text outline to a list of attribute dicts
	"""

 # TASKPAPER REGEX REQUIREMENTS ARE SIMPLER THAN MARKDOWN
	rgx_body = re.compile(r'(\t*)([^\t]*.*)$')
	if bln_tp:
		rgx_tp_tsk = re.compile(r'^(\t*)(\-\s.*)$')
		rgx_tp_prj = re.compile(r'^(\t*)(\s*)([^-\s].*\:)$')
	else:
		rgx_md_hdr = re.compile(RGX_MD_HDR)
		rgx_list = re.compile(r'(\t*)([\-\*\+]|\d{1,}\.)\ ')
		rgx_ord_list = re.compile(r'(\d+\.\ )')
		rgx_code_block = re.compile(r'(\t*)\ {4}')

		rgx_quote = re.compile(r'(\t*)>+\ *')
		rgx_rule = re.compile(r'[\-\*\_]\ {0,2}[\-\*\_]\ {0,2}[\-\*\_]\ *$')
		rgx_prop = re.compile(r'^(\t*)\ *((\w+|)\ :\ (.*))$')
		rgx_link_def = re.compile(r'\ {0,3}\[(.*)\]\:\ +(\S*)(\ *.*)$')


	set_bullets = set(['-', '*', '_'])

	def _read_mode_and_tags(dct_node, bln_tp):
		""" Store the key-value pairs and key list
			and return text leaving in-line tags in place
			but pruning off any tags at the end of the line
		"""
		str_text = dct_node[ATT_TEXT]
		# print "ATT_TEXT", str_text

		# first eat any terminating .mode
		if not bln_tp:
			rgx_mode = re.compile(r'\.(\w+)$')
			o_match = rgx_mode.search(str_text)
			bln_mode = (o_match != None)
			if bln_mode:
				i_start = o_match.start()
				str_point = str_text[0:i_start].rstrip()
				str_mode = str_text[i_start+1:]
				dct_node[ATT_MODE] = str_mode
				dct_node[ATT_CONTEXT] = str_mode
			else:
				str_point = str_text
		else:
			bln_mode = False
			str_point = str_text

		# and then digest all tags, right to left, eating terminal tags.
		i_end = len(str_point)
		lst_keys = []
		lst_not_duplicate = []
		rgx_tag = re.compile(RGX_TP_TAG)
		lst_matches = [_ for _ in rgx_tag.finditer(str_point)]
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
			dct_node[ATT_TEXT] = str_point[0:i_end]


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


	def _set_ft_tabbed_node(dct_node, str_text, var_type, o_match, lng_extra):
		"""set FT node properties by reference"""
		lng_indent = len(o_match.group(1)) + lng_extra
		if lng_indent:
			dct_node[ATT_INDENT] = lng_indent
		if var_type != TYP_BODY:
			dct_node[ATT_TYPE] = var_type
		dct_node[ATT_TEXT] = str_text

	def _set_prop_node(dct_node, o_match):
		""" Read as FT property node
			adding 'name' 'value' to the tagNames list
			and adding teh name:value pair to the tags dict
		"""
		dct_node[ATT_TYPE] = TYP_PROP
		dct_node[ATT_TEXT] = o_match.group(2)
		dct_node[ATT_TAG_NAMES] += ['name', 'value']
		dct_tags = dct_node[ATT_TAGS]
		dct_tags['name'] = o_match.group(3)
		dct_tags['value'] = o_match.group(4)
		lng_indent = len(o_match.group(1))
		if lng_indent > 0:
			dct_node[ATT_INDENT] = lng_indent

	def _read_as_linkdef(dct_node, rgx_link_def, str_point):
		""" Try to read str_point as a linkdef
			if no match, leave as body line
		"""
		o_match = rgx_link_def.match(str_point)
		if o_match != None:
			dct_node[ATT_TYPE] = TYP_LINK
			str_link = o_match.group(2)
			dct_node[ATT_TEXT] = str_link + o_match.group(3)
			dct_node[ATT_TAGS]['label'] = o_match.group(1)
			dct_node[ATT_TAGS]['link'] = str_link
			dct_node[ATT_TAG_NAMES] += ['label', 'link']
			return True
		else:
			return False

	if bln_tp:
		str_vanilla = TYP_NOTE
	else:
		str_vanilla = TYP_BODY

	# WE NEED A ROOT NODE, PLUS A NODE FOR EACH LINE OF TEXT
	lst_nodes = [
		{ATT_ID:0, ATT_TYPE:TYP_ROOT, ATT_TEXT:'', ATT_LEVEL:0, ATT_INDENT:0,
		ATT_MODE:[], ATT_CHILN:[], ATT_PATH:[]}
	] + [
		{ATT_ID:i+1, ATT_TYPE:str_vanilla, ATT_LINE:str_line,
			ATT_LINE_INDEX:i, ATT_TEXT:str_line, ATT_INDENT:0, ATT_TAGS:{},
			ATT_LEVEL:0, ATT_TAG_NAMES:[], ATT_MODE:'', ATT_CONTEXT:'',
			ATT_CHILN:[], ATT_PATH:[]}
		for i, str_line in
			enumerate(str_in.splitlines())
	]

	# MAIN PARSE LOOP TO DERIVE TYPE, AND OTHER ATTRIBUTES OF EACH NODE

	# lng_hash_level = 0
	# lng_hash_len = 0
	# lng_level = 0
	# lng_min_hash = -1 # does the doc start with multiple hashes ?
	lng_txt = 0
	for dct_node in lst_nodes[1:]:
		# Maintain an index into the text
		# (Note that [ATT_ID] serves as a 1-based index to the lines)
		dct_node[ATT_TEXT_INDEX] = lng_txt

		str_point = dct_node[ATT_LINE]
		lng_chars = len(str_point)
		lng_txt += (lng_chars + 1) # splitlines is dropping \n

		# IDENTIFY THE INDENT COUNT & NESTING LEVEL
		# AS WELL AS THE NODE TYPE (hash or bullet start, colon end)
		# EXTRACTING THE PLAIN TEXT

		# REGEXES ARE EXPENSIVE, SO WE'LL START WITH SOME SIMPLE TRIAGE
		# BASED ON THE FIRST CHARACTERS OF THE STRING

		# Assume Body text until there is counter-evidence
		if lng_chars < 1:
			dct_node[ATT_TYPE] = TYP_EMPTY
		else:
			# TaskPaper project ?
			if bln_tp:
				_read_mode_and_tags(dct_node, True)
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
			else:
				str_char = str_point[0]
				if str_char == '\t':
					# LIST ITEMS ?
					o_match = rgx_list.match(str_point)
					if o_match != None:
						# ORDERED (give 1 free indent)
						if len(o_match.group(2)) > 1:
							_set_ft_tabbed_node(dct_node,
								str_point[o_match.end():],
									TYP_ORD, o_match, 1)
						else:
							# UNORDERED (give 1 free indent))
							_set_ft_tabbed_node(dct_node,
								str_point[o_match.end():],
									TYP_UNORD, o_match, 1)
					else:
						o_match = rgx_code_block.match(str_point)

						# CODE BLOCK ?
						if o_match != None:
							dct_node[ATT_TYPE] = TYP_CODE
							dct_node[ATT_INDENT] = len(o_match.group(1))
							dct_node[ATT_TEXT] = str_point[o_match.end():]
						else:
							# BLOCK QUOTE ?
							o_match = rgx_quote.match(str_point)
							if o_match != None:
								_set_ft_tabbed_node(dct_node,
									str_point[o_match.end():],
										TYP_QUOTE, o_match, 0)
							else:
								# FT PROPERTY ?
								o_match = rgx_prop.match(str_point)
								if o_match != None:
									_set_prop_node(dct_node, o_match)

								else:
									# BODY ...
									o_match = rgx_body.match(str_point)
									if o_match != None:
										_set_ft_tabbed_node(dct_node,
											o_match.group(2),
												TYP_BODY, o_match, 0)
									else:
										print "Unexpected result - \
											body parsing"
				elif (not bln_tp) and (str_char == '#'):

					# HEADING ?
					o_match = rgx_md_hdr.match(str_point)
					if o_match != None:
						dct_node[ATT_TYPE] = TYP_HEAD
						dct_node[ATT_TEXT] = o_match.group(2).rstrip()

						dct_node[ATT_INDENT] = len(o_match.group(1))

				elif str_char == ' ':
					o_match = rgx_code_block.match(str_point)

					# CODE BLOCK
					if o_match != None:
						dct_node[ATT_TYPE] = TYP_CODE
						dct_node[ATT_TEXT] = str_point[4:]

					else:
						# LINK DEF ?
						_read_as_linkdef(dct_node, rgx_link_def, str_point)


				elif str_char in set_bullets:
					# EITHER HORIZONTAL RULE OR UNORDERED LIST ITEM
					o_match = rgx_rule.match(str_point)
					if o_match != None:
						dct_node[ATT_TYPE] = TYP_RULE
						dct_node[ATT_TEXT] = ''
					else:
						o_match = rgx_list.match(str_point)
						if o_match != None:
							dct_node[ATT_TYPE] = TYP_UNORD
							# list items are indented an extra level
							# dct_node[ATT_LEVEL] = lng_hash_level + 2
							dct_node[ATT_INDENT] = 1
							dct_node[ATT_TEXT] = str_point[o_match.end():]

				elif str_char == '[':
					# LINK DEF ?
					_read_as_linkdef(dct_node, rgx_link_def, str_point)


				elif str_char == ':':
					#print "found it", dct_node[ATT_LINE]
					#DEFINITION
					dct_node[ATT_TYPE] = TYP_DEFN
					dct_node[ATT_INDENT] = 1
					dct_node[ATT_TEXT] = str_point[1:].lstrip()

				else:
					# ORDERED LIST ?
					o_match = rgx_ord_list.match(str_point)
					if o_match != None:
						dct_node[ATT_TYPE] = TYP_ORD
						# list items are indented an extra level
						dct_node[ATT_INDENT] = 1
						dct_node[ATT_TEXT] = str_point[o_match.end():]
					else:
						# FT PROPERTY (FULL LEFT - NO TABS)
						o_match = rgx_prop.match(str_point)
						if o_match != None:
							_set_prop_node(dct_node, o_match)

		# Now that we know the provisional type of each node,
		# digest any terminal mode, and tags in any position
		# skipping codeblocks, finalising empties
		# and recording modes and modeContexts if type is relevant
		# [heading, empty, body, ordered, unordered]

		# DETECT ANY REMAINING EMPTIES BEFORE WE TAKE OUT MODES & TAGS
		if dct_node[ATT_TYPE] not in SET_BLANK_TYPES:
			if dct_node[ATT_TEXT].rstrip() == '':
				dct_node[ATT_TEXT] = ''
				if dct_node[ATT_TYPE] == TYP_BODY:
					dct_node[ATT_TYPE] = TYP_EMPTY

		if not bln_tp:
			if dct_node[ATT_TYPE] not in SET_TAGLESS:
				_read_mode_and_tags(dct_node, False)


	return lst_nodes

def add_parent_child(lst_lines, bln_tp):
	"""Add ParentID and ChildIDs to each node"""
	# The parent of top levels headers (and other lines before any header)
	# is the virtual root.

	def _set_mode_contexts(lst_nodes, dct_node, str_mode):
		"""copy a mode context to the subtree of a node"""
		dct_node[ATT_CONTEXT] = str_mode
		for id_child in dct_node[ATT_CHILN]:
			dct_child = lst_nodes[id_child]
			dct_child[ATT_CONTEXT] = str_mode
			# and recurse through any subtree
			_set_mode_contexts(lst_nodes, dct_child, str_mode)

	# As we work down the text, maintain lists of the current parent nodes
	# Current hash header parent at each level
	# and any current parents at levels below the hash
	# (e.g. nested list items)
	lst_hash_parents = [0]
	lst_tab_parents = [0]
	lst_blanks = []

	bln_in_defn = False # flips at the borders of definition streams
						# to facilitate backtracking for term flagging
	for dct_line in lst_lines[1:]:
		lng_id = dct_line[ATT_ID]
		var_type = dct_line[ATT_TYPE]

		if var_type != TYP_EMPTY:
			lng_indent = dct_line[ATT_INDENT]
			lng_next_level = lng_indent+1
			if var_type != TYP_HEAD:
				# tabbed types
				# parents in zero-based cell position matching indent length
				# (zero-indented body para has its parent in cell[0])
				# (because minimum indent is ZERO)
				# parent list must be 1 LONGER THAN level of indent
				# zero indent needs parent list of length 1
				# one tab indent nees parent list of length 2

				lng_over_indent = ((lng_next_level+1) - len(lst_tab_parents))
				if lng_over_indent > 0:
					id_parent = lst_tab_parents[-1]
					while lng_over_indent:
						lst_tab_parents.append(lng_id)
						lng_over_indent -= 1
				else:
					id_parent = lst_tab_parents[lng_indent]

				# This node becomes the parent for ALL deeper indented
				# non header nodes
				for i in range(lng_indent+1, len(lst_tab_parents)):
					lst_tab_parents[i] = lng_id

				# print lng_id, dct_line[ATT_TYPE], lst_tab_parents


			else: # hash headers
				# parents in ONE-based cell position matching indent length
				# 1-hash header finds its parent in cell[0]
				# (because minimum indent is ONE)
				# parent list must be AS LONG AS level of indent
				# one hash needs parent list of length 1
				# two hashes needs parent list of length 2
				lng_over_indent = (lng_next_level - len(lst_hash_parents))
				if lng_over_indent > 0:
					id_parent = lst_hash_parents[-1]
					while lng_over_indent:
						lst_hash_parents.append(lng_id)
						lng_over_indent -= 1
				else:
					id_parent = lst_hash_parents[lng_indent-1]


				# This header becomes the parent for ALL more indented headers
				for i in range(lng_indent, len(lst_hash_parents)):
					lst_hash_parents[i] = lng_id
				# and for all other node types
				for i in range(0, len(lst_tab_parents)):
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
			# set TEMPORARY parent (previous hash or virtual root)
			# and then push onto stack to wait for next non-empty node,
			# from which it will take its final level
			dct_line[ATT_PARENT] = lst_tab_parents[0]
			lst_blanks.append(lng_id)

		# IF WE HAVE JUST ENTERED A DEFINITION STREAM,
		# AND THE PARENT IS CURRENTLY FLAGGED 'BODY'
		# THEN SET THE PARENT TYPE TO 'TERM'
		if dct_line[ATT_TYPE] == TYP_DEFN:
			if not bln_in_defn:
				if dct_parent[ATT_TYPE] == TYP_BODY:
					dct_parent[ATT_TYPE] = TYP_TERM
				dct_line[ATT_INDENT] = 0 # reduce for FT compatibility
				bln_in_defn = True
		else:
			bln_in_defn = False

	# Finalise the parenthood of any remaining blanks
	if lst_blanks:
		dct_parent = None
		for id_blank in lst_blanks:
			dct_blank = lst_lines[id_blank]
			if dct_parent == None:
				dct_parent = lst_lines[dct_blank[ATT_PARENT]]
			if not bln_tp:
				dct_blank[ATT_INDENT] = dct_parent[ATT_INDENT] + 1
			dct_parent[ATT_CHILN].append(id_blank)
			dct_blank[ATT_CHILD_INDEX] = len(dct_parent[ATT_CHILN]) - 1
		lst_blanks = []

	# propagate any mode Contexts down through sub-trees
	for dct_node in lst_lines:
		if dct_node[ATT_CHILN]:
			str_mode = dct_node[ATT_MODE]
			if str_mode:
				_set_mode_contexts(lst_lines, dct_node, str_mode)

	return lst_lines


def is_tp(str_text):
	"""True if there are more TP projects than MD hash headers"""
	rgx_md_hdr = re.compile(RGX_MD_HDR, re.M)
	rgx_tp_prj = re.compile(RGX_TP_PRJ, re.M)
	lst_md = rgx_md_hdr.findall(str_text)
	lst_tp = rgx_tp_prj.findall(str_text)
	return len(lst_tp) > len(lst_md)


main()
