### NAME

**TaskPaper Date Entry** – Translates relative and natural language date/time expressions into standard TaskPaper formats

### DESCRIPTION 

A [script](https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/TaskPaperDateEntry-004.applescript) which facilitates entering date/times in the [Taskpaper](http://www.hogbaysoftware.com/products/taskpaper)  application (OS X) by [Hog Bay Software](http://www.hogbaysoftware.com).

Displays a dialog which:

1. allows you to enter a relative date/time expression in natural language, and 
2. either
	- pastes a TaskPaper version of the corresponding date (and, optionally, time), at the current cursor position in TaskPaper, or
	- simply places the date/time in the clipboard


**Note** This script requires installation of Mike Taylor and Darshana Chhajed's Python [parsedatetime](https://github.com/bear/parsedatetime) module:
	
1. Visit [https://github.com/bear/parsedatetime](https://github.com/bear/parsedatetime)
2. Download and expand [https://github.com/bear/parsedatetime/archive/master.zip](https://github.com/bear/parsedatetime/archive/master.zip)
3. in Terminal.app, cd to the unzipped folder 
   
	(e.g. type cd followed by a space, and drag/drop the folder to the Terminal.app command line, then tap return)
4. Enter:
	
            sudo python setup.py install
    
    
#### To disable direct pasting into TaskPaper 

You can adapt the script to only place the date in the clipboard, rather than pasting it into TaskPaper.

Edit the value of boolean variable *pblnPaste* near the top of the script.

        property pblnPaste : false


#### Screen shot

![Translating relative to absolute dates](https://raw.github.com/RobTrew/tree-tools/master/TaskPaper%20scripts/TPDates.png)

