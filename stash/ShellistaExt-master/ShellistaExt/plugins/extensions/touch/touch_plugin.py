
from ...tools.toolbox import bash

def main(self, line):
    do_touch(line)

def do_touch(line):
    """touch a file, either creating it or modifying the modified date"""
    files = bash(line)
    for file in files:
        try:
            with open(file,'ab') as f:
                pass
        except Exception as e:
            print "Couldn't touch {0}".format(file)
