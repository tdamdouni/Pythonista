# https://forum.omz-software.com/topic/4034/simple-ui-to-run-script2-args/9

import sys
import runpy

try:  # https://docs.python.org/3/whatsnew/3.0.html#builtins
	raw_input          # Python 2
except NameError:
	raw_input = input  # Python 3
	

import dialogs
fields=[{'title':'First Name','type':'text'},
         {'title':'Last Name','type':'text'},
         {'title':'Age','type':'number'}]
response=dialogs.form_dialog('What is your info?',fields)
	
script2 = sys.argv[1] if sys.argv[1:] else 'script2.py'
first_name = raw_input("What is your first name? ").strip() or 'Donald'
middle_name = raw_input("What is your middle name? ").strip() or 'J.'
last_name = raw_input("What is your last name? ").strip() or 'Trump'
fmt = "%s: Your full name is %s %s %s."
print(fmt % (sys.argv[0].split('/')[-1], first_name, middle_name, last_name))
sys.argv = ('script2.py', first_name, middle_name, last_name)
with open(sys.argv[0]) as in_file:
	exec(in_file.read())  # exec() is a security hole a mile wide and 10 miles deep!!
	
"""script2.py
import sys
print("{}: Your full name is {} {} {}.".format(*sys.argv))
"""

