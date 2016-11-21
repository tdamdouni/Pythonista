'''
Pythonista Find and Replace
===========================

Notices
-------

Copyright 2013 Harry Jubb.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

For a full copy of the GNU General Public License, see
<http://www.gnu.org/licenses/>.

Description
-----------

Implements a "Find and Replace" function for Ole Zorn's "Pythonista"
iPad app.

Installation
------------

- Add the script in Pythonista in the top level folder as "Find and Replace"
- Settings -> Actions Menu -> Checkmark the script

Usage
-----

- Tap the Action Menu
- Tap Find and Replace
- Enter the string to find
- Enter the replacement string
- Enjoy!
'''

import console
import editor

all_text = editor.get_text()

find = console.input_alert('Find', 'Please enter text to find.', '', 'Find')
replace = console.input_alert('Replace', 'Please enter replacement text.', find, 'Replace')

new_text = all_text.replace(find, replace)

editor.replace_text(0, len(all_text), new_text)

