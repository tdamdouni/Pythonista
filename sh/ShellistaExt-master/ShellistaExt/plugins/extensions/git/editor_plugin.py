'''Open a file in the Pythonista text editor, or vi
if not on iPad
'''

HAS_EDITOR = False

try:
    import editor
    HAS_EDITOR = True
except:
    import os

from ... tools.toolbox import bash

def main(self, line):
    print line
    args = bash(line)

    if len(args) == 1:
        if HAS_EDITOR:
            editor.open_file(args[0])
        else:
            import platform
            if platform.system() == 'Linux':
                os.system('vi {0}'.format(args[0]))
            else:
                print 'Unsupported platform'
    else:
        print 'Usage: editor <filename>'
