#!/bin/sh
# requires that you have already done `pip install pyinstaller`
pyinstaller --onefile Phantom/Run_this.py -n Phantom_for_MacOSX_64bit
echo "Phantom_for_MacOSX_64bit has been built in Phantom/dist:"
ls -la dist  # display file size, etc. of new app
open dist    # show the new app in a Finder window
