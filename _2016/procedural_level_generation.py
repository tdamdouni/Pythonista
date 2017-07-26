# -*- coding: utf -*-

# https://gist.github.com/TutorialDoctor/3122f2ce5b211c9afce1

# add to soft dev/examples
# By the Tutorial Doctor
# Sep 2, 2015

# Procedural Level Generation
#--------------------------------------------------


# THE CODE
#--------------------------------------------------
def spaces(x):
	return ' o '*x

def sidewall():
	return '|'

def basewall(x):
	return ' ' + ' _ '*x

def Level(w,h):
	# Let the user know what is happening (string formatting)
	print('\nGenerating ' +'({}w x {}h)'.format(w,h) + ' level...')
	
	# Make the level (using a for loop)
	print(basewall(w))
	for eachSideWall in range(0,h):
		print(sidewall() + spaces(w) + sidewall())
	print(basewall(w))
#--------------------------------------------------


# IMPLEMEMTATION
#--------------------------------------------------
Level(5,5)
print
Level(20,10)
print
Level(2,24)
#--------------------------------------------------


# Make it random!
#--------------------------------------------------
import random

def randomLevels(amount,maxW=5,maxH=5):
	# Let the user know whst is happening
	print('\nGenerating {} random levels(s)...'.format(amount))
	print('---------------------------------------------------')
	
	for i in range(1,amount+1):
		Level(random.randrange(1,maxW+1),random.randrange(1,maxH+1))
	# All of this +1 jazz is to avoid "off by one"" issues
	
	# maxW = max width
	# maxH = max height
	# By default they are set to 5
#--------------------------------------------------


# The ways you can use it:
randomLevels(4)
randomLevels(amount=20,maxW=8,maxH=12)
randomLevels(2,8,9)
randomLevels(3,maxH=4)
randomLevels(4,maxW=7)

