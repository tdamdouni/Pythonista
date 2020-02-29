# coding: utf-8

# https://gist.github.com/Moving-Electrons/4f23009ba3c84278e49f

# This script generates a text/markdown file with the tasks from a taskpaper file sorted by due date in three groups: Overdue, Today and Tomorrow. Check out www.movingelectrons.net for more information.

from __future__ import print_function
import sys
import re
import operator
import datetime

'''
This script generates a text/markdown file with the tasks from a taskpaper file sorted by due date in three groups:
Overdue, Today and Tomorrow. Also, all tasks with the @today tag are placed in the Today group.

The following parameters should be passed when running the script:
1. Taskpaper file.
2. text/markdown output file.
3. "c"  or "p" (optional). If this argument is passed, tasks are ordered by either Context (c) or Priority (p)
	after they have been ordered by due date.
4. Word (optional). If this argument is passed, the output file will only include tasks that have the Word passed
	as an argument, filtering out all other tasks.
'''
 
# Contants definition
file = sys.argv[1] # .taskpaper file
output = sys.argv[2] # Output .txt/md file


td = datetime.date.today() #gets today's date
tn = datetime.datetime.now()

contextList = ['driving','@work','@home'] #Contexts in the taskpaper file in order.
priorityList = ['@high'] #Priorities in order.

#contextList = ['@work','@home'] #Contexts in the taskpaper file in order.
#priorityList = ['@priority\(1\)','@priority\(2\)','@priority\(3\)'] #Priorities in order. Escaping parenthesis because elements will be used in a Regular Expression.

# These lists are global and used in the main program and some functions.
overdueLst = []
todayLst = []
tomorrowLst = []
#---------------------

def SortbyCriteria(taskList,orderList): 
	'''
	Returns a sorted list based on the items in the orderList argument list, leaving items not matching the 
	items in the orderList at the end.
	'''

	sortedList = []
	# The actual sorting process takes place here. The sorted lines are put in the sortedList
	# based on the order of items in the orderList argument list
	for taskTag in orderList: 
		regex = re.compile('.*'+taskTag+'.*')
		for task in taskList:
			findCtx = re.match(regex,task)
			if findCtx: sortedList.append(task)
	

	# Putting together Regular Expression based on all the items in orderList
	regexString = ''
	for taskTag in orderList:
		regexString = regexString+'.*'+taskTag+'.*|'
	regexString = regexString[:-1] #removes the last '|' character in the string
	
	# Finding items in the list without the tag and adding them at the end of sortedList
	regex = re.compile(regexString)
	for task in taskList:
		findCtx = re.match(regex,task)
		if not findCtx: sortedList.append(task)
	return sortedList			

def FilterbyCriteria(taskList,filter):
	filteredList = []
	regex = re.compile('.*'+filter+'.*')
	for task in taskList:
		findFilter = re.match(regex,task)
		if findFilter: filteredList.append(task)
	return filteredList


def LoadTodos():
	'''
	Opens taskpaper file and returns all lines/tasks in a list.
	'''
	print('Opening Taskpaper file...')
	todo_file = open(file, 'rb')
	raw_todos = todo_file.readlines()
	todo_file.close()
	todos = []
	for item in raw_todos:
		item = item.strip('\r\n')
		todos.append(item)
	return todos

def SortbyDueDate(list): 
	'''
	Goes over ToDos and distributes tasks in three lists according to their due date.
	'''
	print('Going through Due Dates...')
	pjtNme = 'Unknown' # Default project name for task
	regex = re.compile('.*@due\((....\-..\-..)\).*') # group 1 is the date
	reDone = re.compile('.*@done.*')
	reToday = re.compile('.*@today.*')
	rePjt = re.compile('^([a-zA-Z0-9].*)\:$')
	
	for line in list:

		pjtLine = re.match(rePjt, line)
		findDt = re.match(regex, line)
		done = re.search(reDone, line)
		dueToday = re.search(reToday, line)

		if pjtLine: pjtNme = pjtLine.group(1)
		if dueToday and not done: todayLst.append(line+' <'+pjtNme+'>\n')
		if findDt and not done: # it should be checked first if it matches. If not, it may assign dueDt a Null value.
			dueDt = findDt 
			dueDtlst = dueDt.group(1).split('-') # Takes group 1 of dueDt (which is the date string found), splits it and puts it in a list
			print(dueDtlst)
			dueDtdte = datetime.date(int(dueDtlst[0]), int(dueDtlst[1]), int(dueDtlst[2]))
			dtDif = dueDtdte-td

			if dtDif.days<0: overdueLst.append(line+' <'+pjtNme+'>\n')
			elif dtDif.days==0: todayLst.append(line+' <'+pjtNme+'>\n')
			elif dtDif.days==1: tomorrowLst.append(line+' <'+pjtNme+'>\n')
	print('Done.')

def WriteFile(title,list,workingFile):
	workingFile.write("%s" % title)
	for row in list:
		workingFile.write("%s" % row)


# Main program
# -----------------------------------------
if __name__ == "__main__":

	todoList = LoadTodos()
	#sorting by date:
	SortbyDueDate(todoList)
	# If the sort argument is passed:
	if len(sys.argv) >= 4:
		
		sortOrder = sys.argv[3]
		# sorting by the third argumentL:
		'''
		Sorting by the third argument. It sorts by either Context or priority
		using the lists at the beginning of the script as reference.
		'''
		if sortOrder == 'c':
			overdueLst = SortbyCriteria(overdueLst,contextList)
			todayLst = SortbyCriteria(todayLst,contextList)
			tomorrowLst = SortbyCriteria(tomorrowLst,contextList)
		if sortOrder == 'p':
			overdueLst = SortbyCriteria(overdueLst,priorityList)
			todayLst = SortbyCriteria(todayLst,priorityList)
			tomorrowLst = SortbyCriteria(tomorrowLst,priorityList)


	# Filtering
	'''
	If a 4th argument is passed, then results are filtered by the argument.
	'''
	if len(sys.argv) == 5:
		filterBy = sys.argv[4]
		overdueLst = FilterbyCriteria(overdueLst,filterBy)
		todayLst = FilterbyCriteria(todayLst,filterBy)
		tomorrowLst = FilterbyCriteria(tomorrowLst,filterBy)
		
	# Writing to the file
	print('Writing tasks to file...')
	txtFile= open(output, 'w')

	WriteFile("## Sorted Tasks ## \n**Do not edit this file.**\n\n",[],txtFile)
	WriteFile("### Overdue:\n",overdueLst,txtFile)
	WriteFile("\n",[],txtFile)
	
	todayText = '### Due Today (%s):\n' % str(tn.strftime("%Y-%m-%d %H:%M"))
	WriteFile(todayText,todayLst,txtFile)
	WriteFile("\n",[],txtFile)
	WriteFile("### Due Tomorrow:\n",tomorrowLst,txtFile)

	txtFile.close()
	print('Done.')

