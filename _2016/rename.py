#!/usr/bin/env python

# https://github.com/dgelessus/pythonista-scripts/blob/master/rename.py

"""Simple editor script to rename a file. Unlike Pythonista's built-in
way to rename files, this does not automatically append any suffixes
and works on files that are not openable in the text editor.
"""

from __future__ import division, print_function

import console
import editor
import os
import sys

DOCUMENTS = os.path.realpath(os.path.expanduser("~/Documents"))
if DOCUMENTS.startswith("/private"):
    DOCUMENTS = DOCUMENTS[len("/private"):]

def main(args):
    try:
        # Source and destination are passed via runtime args
        src, dest = args
    except (TypeError, ValueError):
        # Get source and destination from user
        curfile = os.path.relpath(editor.get_path() or "", DOCUMENTS)
        
        shortsrc = console.input_alert(
            "Source Name", # title
            "Path is relative to Script Library root", # message
            curfile, # input
        )
        src = os.path.join(DOCUMENTS, shortsrc)
        
        if not os.path.exists(src):
            console.hud_alert("Source file does not exist", "error")
            sys.exit(1)
        
        dest = os.path.join(DOCUMENTS, console.input_alert(
            "Destination Name", # title
            "Path is relative to Script Library root", # message
            shortsrc, # input
        ))
    else:
        # Process source and destination from runtime args
        src, dest = os.path.join(DOCUMENTS, src), os.path.join(DOCUMENTS, dest)
        
        if not os.path.exists(src):
            console.hud_alert("Source file does not exist", "error")
            sys.exit(1)
    
    if os.path.exists(dest):
        console.hud_alert("Destination file already exists", "error")
        sys.exit(1)
    
    os.rename(src, dest)
    
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])

