# @Markdown
# pymdlist2headers

# Just a simple python script that takes some kind markdown content from the clipboard, and takes the list items and convert it to headers. Each level of indention applies one extra "#".

# https://github.com/hjertnes/pymdlist2headers/blob/master/main_pythonista.py

#!/usr/bin/python

import re,clipboard
def setClip(data):
    clipboard.set(data)

def getClip():
    return clipboard.get()

output = ""
def find_tabs_and_return_count(line):
    matches = re.findall("\t",line)
    tab_num = len(matches)
    matches = re.findall("    ",line)
    tab_num += len(matches)
    return tab_num
    
for line in getClip().split("\n"):
    tab_num = find_tabs_and_return_count(line)
    line = re.sub("    ","",line)
    line = re.sub("\t","",line)
    status = False
    if re.findall("^\*",line) or re.findall("^-",line):
        status=True
    line = re.sub("^-","#",line)
    line = re.sub("^\*","#",line)
    if status is True:
        for r in range(tab_num):
            line = "#%s"%line
    output="%s\n%s"%(output,line)
setClip(output)