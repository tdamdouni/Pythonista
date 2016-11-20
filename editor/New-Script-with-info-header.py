#!/usr/bin/env python3
'''
Pythonista template to include some basic information in a header comment

You need to save this file to '~/Documents/Templates', so that Pythonista can find and list it in the "New File" dialog
'''

import dialogs
import editor
import datetime
import os
import string

__author__ = 'Lukas Kollmer'
__copyright__ = 'Copyright (c) 2016 Lukas Kollmer<lukas@kollmer.me>'

template_text = '''\'\'\'
${description}

${documentation}
\'\'\'

__author__ = '${author_name}'
__copyright__ = 'Copyright (c) ${year} ${author_name}'
'''

template = string.Template(template_text)

file_path = editor.get_path()
filename = os.path.basename(file_path)


# Get the information

fields = []

fields.append([  # Section 1 rows
        #{'type': 'text', 'title': 'File name', 'value': filename, 'key': 'filename'},
        {'type': 'text', 'title': 'Author', 'key': 'author_name'}
])

fields.append([  # Section 2 rows
        {'type': 'text', 'title': 'Description', 'key': 'description'},
        {'type': 'text', 'title': 'Documentation', 'key': 'documentation'}
])


form_sections = [
        ('About', fields[0], None),
        ('File info', fields[1], None)
]

data = dialogs.form_dialog('New File', sections=form_sections)

if not data:
	import sys
	sys.exit()
	
copyright_year = datetime.datetime.now().year
new_text = template.substitute(**data, year=copyright_year, filename=filename)

end = len(editor.get_text())
editor.replace_text(0, end, new_text)

