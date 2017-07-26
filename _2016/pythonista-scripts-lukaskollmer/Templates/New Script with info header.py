#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Pythonista template to include some basic information in a header comment

You need to save this file to '~/Documents/Templates', so that Pythonista
can find and list it in the "New File" dialog
'''

import datetime
import dialogs
import editor
import os

__author__ = 'Lukas Kollmer'
__copyright__ = 'Copyright © 2016 Lukas Kollmer <lukas@kollmer.me>'


def title_key_dict(title, key):
    return {'type': 'text', 'title': title, 'key': key}

fields = ([title_key_dict('Author', 'author_name'),       # section 1 rows
           title_key_dict('Email', 'email')],
          [title_key_dict('Description', 'description'),  # section 2 rows
           title_key_dict('Documentation', 'documentation')])

form_sections = (('About', fields[0], None),
                 ('File info', fields[1], None))

data = dialogs.form_dialog('New File', sections=form_sections)
assert data, 'No data entered.'
#data['filename'] = os.path.basename(editor.get_path())
data['copyright_year'] = datetime.datetime.now().year

fmt = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
{description}

{documentation}
'''

import sys

__author__ = '{author_name}'
__copyright__ = 'Copyright © {copyright_year}, {author_name} <{email}>'
__credits__ = ['{author_name}']
__email__ = '{email}'
__license__ = 'MIT'
__maintainer__ = '{author_name}'
__status__ = 'Pre-Alpha'
__version__ = '0.0.1'
"""

editor.replace_text(0, len(editor.get_text()), fmt.format(**data))
