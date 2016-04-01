# https://gist.github.com/jeffgravitywell/d98c64066213fdd2d7cc

#!/usr/bin/python

# Script to generate a tpToday.taskpaper file containing all priority tasks from other taskpaper files.

import os
import io
import sys
import shutil
import re
import string
from datetime import date, datetime, time

# add as many taskpaper files as you want here
filelist = [ 
                '/Users/person/Dropbox/Elements/tpHomeProjects.taskpaper', 
                '/Users/person/Dropbox/Elements/tpWorkProjects.taskpaper'
            ]

# this is where your today perspective will be stored
targetfile = '/Users/person/Dropbox/Elements/tpToday.taskpaper'
d = date.today()
today = d.strftime('%Y-%m-%d')
dt = datetime.now()

todayText = 'Last Run: ' + dt.strftime('%Y-%m-%d %H:%M')
regex     = "((@+\\bcritical*)|(@+\\btoday*)|(@+\\bhigh)|(@+\\bdue\(" + today + "\)))(?!.*@done)"

for taskfile in filelist:

    # open the file for reading
    currFile = open(taskfile)
    todayText    = todayText + '\n' + 'Filename: ' + taskfile + '\n'
    currentProject = ''
    project  = 'None'
    
    # loop through the lines
    for line in currFile:

        # if you find a project
        if line.find(':') != -1:
            
            if line != project:
                project = line
            else:
                pass
        # if it isn't a project, look for the target regex
        # add more here for extended date math
        else:
            match = re.search(regex, line)
            if match:
                if project == currentProject:
                    pass
                else:
                    currentProject = project
                    todayText = todayText + '\n' + project   
                    
                todayText = todayText + line
            
    currFile.close()

# put the newly created text data into tpToday.taskpaper        
os.remove(targetfile)
todayFile = open(targetfile, "w")
todayFile.write(todayText)
todayFile.close()

# Now set up jobs in Lingon to run when any of your taskpaper files change.