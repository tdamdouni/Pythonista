#!python2
# coding: utf-8

# [Demography](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/demography.py) is the study of human population. Check out how to explore this using OOP in Python.

#How to make member variables permanent?
#Customizing class creation 3.4.3
#print '#'+'-'*79
#Tutorial Doctor 5/28/15-6/1/15
#------------------------------------------------------------------------------


#CLASSES
#------------------------------------------------------------------------------
from __future__ import print_function
class Human(object):
	#class variable. accesed by all instances. only one copy.
	#if an object changes it, change is seen by all instances.
	
	population = 0
	members = []
	
	def __init__(self,name='Null',age=0):
		stages=['null','infant','toddler','?','adolescent','adult']
		Human.population+=1
		self.name = name
		self.age=age
		self.stage=stages[0]
		Human.members.append(self.name)
		print("%s has entered the world"%(self.name))
		
		if self.age<=2:
			self.stage=stages[1]
		elif self.age<=5:
			self.stage=stages[2]
		elif self.age<18 and self.age >=13:
			self.stage=stages[4]
		elif self.age>=18:
			self.stage=stages[5]
		else:
			self.stage=stages[3]
	
	def __str__(self):
		return (str(self.name))
	
	def get_info(self):
		print('Name: %s Age: %d'%(self.name,self.age))
	
	#'@classmethod' is called a decorator.
	#Same as: how_many=classmethod(how_many)
	@classmethod
	def how_many(cls):
		print('There are now %s humans in this world.' %(cls.population))
	
	def die(self):
		Human.population-=1
		Human.members.remove(self.name)
		print('%s has died. The population is now %s.\n %s' %(self.name,Human.population,Human.members))
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
class Female(Human):
	#This is the init function for the present class
	def __init__(self,name='Female',age=0):
		#Loading the init function for the inherited class and whichever variables you want to inherit
		Human.__init__(self,name,age)
		#Adding more variables
		self.SYMBOL = 'o+'
#------------------------------------------------------------------------------
class Male(Human):
	def __init__(self,name='Male',age=0):
		Human.__init__(self,name,age)
		Human.__str__(self)
		self.SYMBOL='o->'
#------------------------------------------------------------------------------
class Woman(Female):
	def __init__(self,name='Woman',age=18):
		Female.__init__(self,name,age)
#------------------------------------------------------------------------------
class Girl(Female):
	def __init__(self,name='Girl',age=0):
		Female.__init__(self,name,age)
#------------------------------------------------------------------------------		
class Man(Male):
	def __init__(self,name='Man',age=18):
		Male.__init__(self,name,age)
#------------------------------------------------------------------------------
class Boy(Male):
	def __init__(self,name='Boy',age=0):
		Male.__init__(self,name,age)
#-------------------------------------------------------------------------------


#INSTANTIATION
#-------------------------------------------------------------------------------
human=Human()
print(human.name)
print(human.age)

print()

sarah=Woman('Sarah',35)
print(sarah.name)
print(sarah.SYMBOL)
print(sarah.age)
print(sarah.stage)

print()

joey=Man('Joey',17)
print(joey.name)
print(joey.SYMBOL)
print(joey.age)
print(joey.stage)

billy = Boy('Bill',1)
print(billy.stage + " is billy's stage")

jill = Girl('Jill',5)
print(jill.stage + " is jill's stage")
joey.get_info()

print(Human.how_many())
billy.die()
print(Human.how_many())
#------------------------------------------------------------------------------


#FUNCTIONS
#------------------------------------------------------------------------------
#Returns True if input is a male
def is_male(x):
	if x.SYMBOL=='o->':
		return True
	return False
#------------------------------------------------------------------------------
#Returns True if input is a female
def is_female(x):
	if x.SYMBOL=='o+':
		return True
	return False
#------------------------------------------------------------------------------
#Returns True if input exists in the class of humans
def exists(x):
	if x not in Human.members:
		return False
	return True
#------------------------------------------------------------------------------
print()

print(is_male(sarah))
print(is_male(joey))
print(is_female(sarah))

if is_female(sarah):
	print(sarah.name + ' is old enough.')

print(exists('Sarah'),'existance')
#------------------------------------------------------------------------------


#
#------------------------------------------------------------------------------
"""
print Human.__subclasses__()
print
print sarah.__class__()
print
print dir()
print
print dir(Man)
#Delete and set attributes
#delattr(object,'name')
#setattr(object,'name',value)
"""
