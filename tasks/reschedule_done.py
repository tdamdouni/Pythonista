#!/usr/bin/python2.7

# https://gist.github.com/Moving-Electrons/05aacf1766dc98092922

# This script takes the taskpaper file passed as an argument and reschedules completed recurring tasks based on their due date, done date and recurring frequency. The task is put in the project it was completed on, even if it has been archived at the end of the file. The script looks for the following tags: - @due(YYYY-MM-DD) e.g. @due(2015-04-17) - @done(YYYY-MM-DD) e.g. @done(2015-04-17). If the done date is not included, the script won't register that task as completed. - @freq(nF). This is the recurring frequency, where n is an integer and F can be d (days), w (weeks), m (months) or y (years). e.g. if @freq(2m) the task will be done every two months. Note: If a task is completed before its due date, it will be put at the top of the file with the unmodified due date for further manual processing.

from __future__ import print_function
import re
import shutil
import os
import sys
from datetime import date, timedelta

''' This script takes the taskpaper file passed as an argument and reschedules completed recurring tasks based on their 
due date, done date and recurring frequency. The task is put in the project it was completed on, even if it has been 
archived at the end of the file. The script looks for the following tags:

- @due(YYYY-MM-DD) e.g. @due(2015-04-17)
- @done(YYYY-MM-DD) e.g. @done(2015-04-17). If the done date is not included, the script won't register that task as completed.
- @freq(nF). This is the recurring frequency, where n is an integer and F can be d (days), w (weeks), m (months) or y (years). 
e.g. if @freq(2m) the task will be done every two months.

Note: If a task is completed before its due date, it will be put at the top of the file with the unmodified due date for further
manual processing.
'''

# Constant definition
tpFile = sys.argv[1] # taskpaper file


def WriteToTaskpaper(tskList,tskFile):
	
	with open('tmpFile', 'w') as tmpFile:

		print('Writing to file...')
		for line in tskList:
			tmpFile.write(line)


	print('Copying and removing temp file.')
	shutil.copy('tmpFile',tskFile)
	os.remove('tmpFile')


def AddTask(newTask):
	
	'''
	Adds the newly formatted task to the global list 'pendingTaskList' which holds all the pending
	tasks that will be written to the final Taskpaper file. The task is added after the item with 
	the project name contained within the tag @project() in the task.

	If the Project name is 'None' or can't be found in the list of tasks, the task is added to
	the top of the lists.
	'''

	projectFlag = False #flag to be raised when the line where the project name is found
	index = 0
	projectPattern = '\@project\((.*?)\)'
	projectRegex = re.search(projectPattern, newTask)
	
	if projectRegex: pName = projectRegex.group(1)
	else: pName = 'None'
	print('Project Name from Task ----> '+pName)

	newTask = re.sub(projectPattern, '', newTask)


	for item in pendingTaskList:
		index += 1
		projectFound = re.search(pName, item)
		
		if projectFound: 
			projectFlag = True
			break

	if projectFlag == False or pName == 'None' : index = 0

	pendingTaskList.insert(index, newTask)
		
	

def DateFromPattern(pattern, line):
	'''
	Returns a Date object based on the arguments, which are:
	1. Pattern to look for in the form of @tag(xdate). Only group 1 from the pattern will be used.
	2. Line of text to look for the pattern 
	'''

	dateRegex = re.search(pattern, line)
	dateList = dateRegex.group(1).split('-')
	dateObj = date(int(dateList[0]), int(dateList[1]), int(dateList[2]))

	return dateObj

def RescheduleTask(dueDt, freq):
	'''
	This function takes a date object and a frequency as arguments and returns the rescheduled date
	object. If there is an error in the frequency formatting, it returns a string with the error instead.
	
	Notes:
	
	- Frequencies are not case sensitive (e.g. d or D for day intervals can be used).
	- Time/date intervals should be entered as integers. e.g. '3d'
	- The function can also take negative frequencies as arguments and adjust the due date accordingly (e.g. '-1y')
	'''
	
	dPattern = '(.+)[d|D]'
	dFreq = re.search(dPattern, freq)
	
	mPattern = '(.+)[m|M]'
	mFreq = re.search(mPattern, freq)
	
	yPattern = '(.+)[y|Y]'
	yFreq = re.search(yPattern, freq)
	
	wPattern = '(.+)[w|W]'
	wFreq = re.search(wPattern, freq)
	
	try:
		if dFreq:
			baseTime = timedelta(days=+1)
			newDt = dueDt + baseTime*int(dFreq.group(1))
		
		elif mFreq:
			baseTime = timedelta(days=+31)
			newDt = dueDt + baseTime*int(mFreq.group(1))
			newDt = newDt.replace(day = dueDt.day)
		
		elif yFreq:
			baseTime = timedelta(days=+365)
			newDt = dueDt + baseTime*int(yFreq.group(1))
			newDt = newDt.replace(day = dueDt.day)
			
		elif wFreq:
			baseTime = timedelta(weeks=+1)
			newDt = dueDt + baseTime*int(wFreq.group(1))
	except ValueError:
		print('Alert: wrong frequency format.')
		newDt = 'Error in Frequency Provided'
	
	return newDt

# Main program
# ------------

if __name__ == "__main__":

	duePattern = '@due\((.*?)\)'
	freqPattern = '@freq\((.*?)\)' 
	donePattern = '@done\((.*?)\)'
	projPattern = '^(.+?)\:$'
	
	
	doneTaskList = []
	pendingTaskList = []
	ProjectName = 'None'


	with open(tpFile, 'r') as infile:
		contents = infile.readlines()
		
	for line in contents:
		
		dueTag = re.search(duePattern, line)
		freqTag = re.search(freqPattern, line)
		doneTag = re.search(donePattern, line)
		projectFlag = re.search(projPattern, line)

		if projectFlag: ProjectName = projectFlag.group(1)
		
		if dueTag and freqTag and doneTag:
						
			line = line.strip('\r\n')
			doneTaskList.append(line+'@project('+ProjectName+')\n')

		else:
			pendingTaskList.append(line)

	
	for task in doneTaskList:

		doneDate = DateFromPattern(donePattern, task)
		dueDate = DateFromPattern(duePattern, task)
		
		freqPeriod = re.search(freqPattern, task).group(1) # Getting the recurrence interval from the @freq tag. e.g: 4w

		if doneDate >= dueDate:

			newTask = re.sub(duePattern+'|'+donePattern, '', task) # Gets rid of the @done(XXXX-XX-XX) and @due(XXXX-XX-XX) tags.
			newTask = newTask.strip('\r\n')
			newDueDate = RescheduleTask(dueDate, freqPeriod)

			newTask = newTask+'@due('+newDueDate.isoformat()+')\n'
			
			print('Old Task > '+task)
			print('New Task > '+newTask)
			
			AddTask(newTask)
			
	
		else:
			print('Task done before Due Date. Adding to the top of the list.')
			pendingTaskList.insert(0, task)

	WriteToTaskpaper(pendingTaskList, tpFile)
