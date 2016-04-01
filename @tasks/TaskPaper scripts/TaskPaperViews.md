### NAME

**TaskPaper Views** – Offers a choice of saved queries which can use relative dates

### DESCRIPTION 

A [script](https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/TaskPaperViews-005.applescript) which displays an editable menu of saved views for the [Taskpaper](http://www.hogbaysoftware.com/products/taskpaper)  application (OS X) by [Hog Bay Software](http://www.hogbaysoftware.com).

- Each view can appear on the menu either in the form of a descriptive name, or in raw TaskPaper syntax.

- View queries can include relative (and natural language) date expressions, {enclosed in curly brackets}

        Due soon | @due < {now +7d}

- When an item is chosen from the script menu:
	1. Any relative date/time expressions are translated into a corresponding absolute date/time, and
	2. the filter is applied to the front TaskPaper OS X document.

	**Note** The relative date function requires installation of Mike Taylor and Darshana Chhajed's Python [parsedatetime](https://github.com/bear/parsedatetime) module:
	
	1. Visit [https://github.com/bear/parsedatetime](https://github.com/bear/parsedatetime)
	2. Download and expand [https://github.com/bear/parsedatetime/archive/master.zip](https://github.com/bear/parsedatetime/archive/master.zip)
	3. in Terminal.app, cd to the unzipped folder 
   
		(e.g. type cd followed by a space, and drag/drop the folder to the Terminal.app command line, then tap return)
	4. Enter:
	
            sudo python setup.py install
    
#### The menu of custom Taskpaper views is stored in a simple text file

- Each custom View is stored as a line of plain text in a menu file.
- The default file name is:

        TPCustomViews.txt 


	(in the same folder as this script)

#### Queries can be displayed in the menu as descriptive names

(Rather than in raw query language syntax)

- Each query can optionally be prefixed by a descriptive label, 
- and the default separator after the label is a single pipe character |

        Due this week | @due < {now +7d}

#### An Edit option in the menu offers a cheat sheet

TPCustomViews.txt can, of course, be edited directly in your preferred text editor. Alternatively, an Edit option at the bottom of the script menu allows you to add and customise optionally labelled query lines, seeing their effect in Taskpaper as soon as you save.

- To amend or delete existing queries, multiselect 'Edit' and one or more queries (⌘-Click)
- To delete a query, place a pipe character at the end of the line, followed by no further printing characters

        Due this week | 
        (or)
        Due this week | @due < {now +7d} |

- A cheat sheet with a copy button lists:
	-  query language terms, and 
	- current document @tags.

#### View names can be displayed with or without query terms 

Queries prefixed by a label and pipe character are, by default, displayed in the menu as View names only.

To display both label and query terms in the menu, edit the value of boolean variable *pblnLabelOnly* near the top of the script.

        property pblnLabelOnly : false


### EXAMPLES AND SCREEN SHOTS

Sample file and default display below.


        Available | not @done and not @cancel and not @hold and (@start <=  {today} or @due <=  {today} or @today)
        Due this week | @due < {now +7d}
        In Progress | not @done and (@start < {today} or @draft or @waiting or @today)
        Overdue | @due < {now}

![Menu of Taskpaper views](https://raw.github.com/RobTrew/tree-tools/master/TaskPaper%20scripts/ViewMenu.png)

![Edit mode](https://raw.github.com/RobTrew/tree-tools/master/TaskPaper%20scripts/EditMode.png)

![Cheat sheet](https://raw.github.com/RobTrew/tree-tools/master/TaskPaper%20scripts/CheatSheet.png)

### SOURCE

[TaskPaperViews.applescript](https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/TaskPaperViews-005.applescript)
