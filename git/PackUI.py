# -*- coding: utf-8 -*-
# https://github.com/dgelessus/pythonista-scripts/blob/master/PackUI.py
################################################################################
# PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
################################################################################
# Package a UI script and its corresponding .pyui file into a single,
# self-extracting file. When run, the generated script will unpack both files,
# allowing both running and further editing without limitations.
# 
# The PackUI script itself can be given a py/pyui pair to package either using
# the (very basic) UI by running it directly, via sys.argv, or by importing it
# and using the PackUI.pack() function. All paths are considered relative to
# the current working directory.
################################################################################

import os.path

def script_text(name, pyfile, pyuifile):
    return '''# -*- coding: utf-8 -*-
###############################################################################
# This is a self-extracting UI application package for {name}.
# Run this script once to extract the packaged application.
# The files will be extracted to {name}.py and {name}.pyui.
# Make sure that these files do not exist yet.
# To update from an older version, move or delete the old files first.
# After extracting, the application can be found at {name}.py.
# This bundle can be deleted after extraction.
###############################################################################
# Packaged using PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
###############################################################################

import console, os.path

NAME     = "{name}"
PYFILE   = """{pyfile}"""
PYUIFILE = """{pyuifile}"""

def fix_quotes_out(s):
    return s.replace("\\\\\\"\\\\\\"\\\\\\"", "\\"\\"\\"").replace("\\\\\\\\", "\\\\")

def main():
    if os.path.exists(NAME + ".py"):
        console.alert("Failed to Extract", NAME + ".py already exists.")
        return
    
    if os.path.exists(NAME + ".pyui"):
        console.alert("Failed to Extract", NAME + ".pyui already exists.")
        return
    
    with open(NAME + ".py", "w") as f:
        f.write(fix_quotes_out(PYFILE))
    
    with open(NAME + ".pyui", "w") as f:
        f.write(fix_quotes_out(PYUIFILE))
    
    msg = NAME + ".py and " + NAME + ".pyui were successfully extracted!"
    console.alert("Extraction Successful", msg, "OK", hide_cancel_button=True)
    
if __name__ == "__main__":
    main()'''.format(name=name, pyfile=pyfile, pyuifile=pyuifile)

def fix_quotes_in(s):
    return s.replace("\\", "\\\\").replace("\"\"\"", "\\\"\\\"\\\"")

def pack(path):
    if not os.path.exists(path + ".py"):
        raise IOError(path + ".py does not exist")
    elif not os.path.isfile(path + ".py"):
        raise IOError(path + ".py is not a file")
    elif not os.path.exists(path + ".pyui"):
        raise IOError(path + ".pyui does not exist")
    elif not os.path.isfile(path + ".pyui"):
        raise IOError(path + ".pyui is not a file")
    elif os.path.exists(path + ".uipack.py"):
        raise IOError(path + ".uipack.py already exists")
    
    name = os.path.split(path)[1]

    with open(path + ".py") as f:
        pyfile = fix_quotes_in(f.read())
    
    with open(path + ".pyui") as f:
        pyuifile = fix_quotes_in(f.read())
    
    out = script_text(name, pyfile, pyuifile)
    
    with open(path + ".uipack.py", "w") as f:
        f.write(out)
    
    return out

def main():
    import sys
    if len(sys.argv) > 1: # pack files specified via argv
        arg = ' '.join(sys.argv[1:])

        try:
            pack(arg)
        except IOError as err:
            print("Failed to pack program: " + err.message)
    else: # display prompt for file
        import console
        msg = "Enter path (relative to current directory) of the application to be packaged, without .py or .pyui suffixes."
        arg = console.input_alert("Package UI Application", msg)
        
        try:
            pack(arg)
        except IOError as err:
            console.alert("Failed to pack", err.message)
            return
        
        msg = "Application was successfully packaged into {}.uipack.py!".format(arg)
        console.alert("Packaging Successful", msg, "OK", hide_cancel_button=True)

if __name__ == "__main__":
    main()