# coding: utf-8

# https://github.com/psidnell/Pythonista/blob/master/Import.py

'''
Copyright 2015 Paul Sidnell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
The backend saving component of a WorkFlow app to allow easy importing of source
files from DropBox to Pythonista.

The Workflow app is:

Get Files from Dropbox
  Show Picker: yes
Copy to Clipboard
Get Name
Text:
        pythonista://Import?action=run&args=(Input)
Open URLs
'''
from __future__ import print_function

import sys
import clipboard
import editor
import webbrowser
import urllib
import console

name = "IMPORTED_" + sys.argv[1] + ".py";
content = clipboard.get();
f = open(name, "w");
f.write(content);
f.close();

console.clear();
print("Created " + name);

