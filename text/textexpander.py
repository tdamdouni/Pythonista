# coding: utf-8

# https://gist.github.com/SFurnace/2baa00e86fd1005df49d

'''A snippet-expander in pythonista, you can add your own snippets easily. '|' is where the cursor will be after expansion.'''

import re
import editor

# variables which are used to get text from the editor.
_text = editor.get_text()
_cursor = editor.get_selection()
_line = editor.get_line_selection()

# some `re` patterns.
_indent = re.compile(r'^ *')

# get indent.
line = _text[_line[0]:_line[1]]
indent = re.match(_indent, line).group(0)

# get the trigger_text
if _cursor[0] != _cursor[1]:
	object = _text[_cursor[0]:_cursor[1]]
	place = (_cursor[0], _cursor[1])
else:
	object = line[0:_cursor[0]-_line[0]].split(' ')[-1]
	place = (_cursor[0]-len(object), _cursor[0])
	
# snippets
storage = {
    'f': '''
def |():
    pass
''',

    'm': '''
def |(self, ):
    pass
''',

    'ifm': '''
if __name__ == '__main__':
    |
''',

    'for': '''
for | in :
''',

    'te': '''
try:
    |
except:
    pass
''',

    'tee': '''
try:
    |
except:
    pass
else:
    pass
''',

    'cls': '''
class |:
    pass
''',
    'init': '''
def __init__(|):
    pass
'''
}


def replace_with_cursor(replacement, cursor):
	if indent != '':
		lines = replacement.splitlines()
		replacement = ('\n'+indent).join(lines)
		cursor = replacement.find('|')
	replacement = replacement[:cursor]+replacement[cursor+1:]
	editor.replace_text(place[0], place[1], replacement)
	editor.replace_text(place[0]+cursor, place[0]+cursor, '')
	
	
def replace_without_cursor(replacement):
	if indent != '':
		lines = replacement.splitlines()
		replacement = ('\n'+indent).join(lines)
	editor.replace_text(place[0], place[1], replacement)
	
	
if __name__ == '__main__':
	replacement = storage.get(object, object).strip()
	cursor = replacement.find('|')
	first_line_length = replacement.find('\n')
	
	if cursor == -1:
		replace_without_cursor(replacement)
	else:
		replace_with_cursor(replacement, cursor)

