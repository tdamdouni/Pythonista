#!/usr/bin/python
#
# How to get markdown data out of Ulysses (http://ulyssesapp.com) sheets and into straight markdown files
#
# Step 1: Select all sheets in the Ulysses app and drag to a folder on the desktop
# Step 2: Run the following:
#

import os

udir = '/Users/petersafarik/Desktop/Ulysses-Backup' # specify folder containing copied Ulysses pages here
outdir = '/Users/petersafarik/Desktop/Ulysses-Backup/md' # specify output folder here (with no trailing "/")

ufiles = []

for dirname in os.walk(udir):
    ufiles.append(dirname)

ufiles.remove(ufiles[0])

for sheet in ufiles:
    title = sheet[0].split("/")[5].split(".")[0][6:]
    textfile = sheet[0] + "/" + sheet[2][1]
    with open(textfile) as f:
        temptext = f.read()
    with open(outdir + "/" + title + ".md", 'wb') as outfile:
        outfile.write(temptext)
