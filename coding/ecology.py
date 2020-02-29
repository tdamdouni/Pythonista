from __future__ import print_function
# Interested in how organisms are related? Then explore and expand upon this [Ecology](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/ecology.py) script.

# Based on:
# Biology: Homework Helpers
# Mathew Distefano
# p.173: Ecology
# By the Tutorial Doctor

class Organism():
	def __init__(self,name):
		self.name=name
		Species.population+=1
	def __str__(self):
		return str(self.name)

class Species(Organism):
	organisms=[]
	population=0
	def __init__(self,name,habitat=None,community=None):
		self.name=name
	def __str__(self):
		return str(self.name)
	def add_organism(self,org):
		Species.organisms.append(org.name)

u = Organism('food')
A = Species('pyhla')
A.add_organism(u)

print(A.organisms)
print(A.population)

