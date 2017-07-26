# https://forum.omz-software.com/topic/4034/simple-ui-to-run-script2-args/8

import sys
import runpy

try:  # https://docs.python.org/3/whatsnew/3.0.html#builtins
	raw_input          # Python 2
except NameError:
	raw_input = input  # Python 3
	
script2 = sys.argv[1] if sys.argv[1:] else 'script2.py'
first_name = raw_input("What is your first name? ").strip() or 'Donald'
middle_name = raw_input("What is your middle name? ").strip() or 'J.'
last_name = raw_input("What is your last name? ").strip() or 'Trump'
fmt = "%s: Your full name is %s %s %s."
print(fmt % (sys.argv[0].split('/')[-1], first_name, middle_name, last_name))
runpy.run_path(script2, init_globals={'first_name': first_name,
                                      'middle_name': middle_name,
                                      'last_name': last_name})


"""script2.py
import sys
fmt = "{}: Your full name is {first_name} {middle_name} {last_name}."
print(fmt.format(sys.argv[0], **globals()))
"""

