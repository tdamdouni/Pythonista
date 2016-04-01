"""change the current directory to DIR"""

from .. tools.toolbox import bash
import os

def main(self, line):
        
    args = bash(line)
    if args is None:
        return
    elif args and len(args) == 1:
        try:
            os.chdir(args[0])
        except Exception:
            print "cd: %s: No such directory" % line
    elif len(args) > 1:
        print "cd: Too many arguments"
    else:
        os.chdir(os.path.expanduser('~/Documents'))

