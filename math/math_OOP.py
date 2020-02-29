from __future__ import print_function
# You can also do math using OOP(**Object-Oriented-Programming**). Check [it](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/math_OOP.py) out.

class MathGenius():
	def add(self,a,b):
		print(a+b)
	#Silas isnt a genius yet
	def subtract(self,a,b):
		print(a-b)
	#Better
	def multiply(self,a,b):
		print(a*b)
	def divide(self,a,b):
		print(a/b)
	def __init__(self,name,age):
		self.name = name
		self.age = age
		self.dad = ''
		self.mom = ''
		self.school = ''
	#Returns the largest of two numbers:
	def bigger(self,a,b):
		if a>b:
			return a
		elif b>a:
			return b
		else:
			return 'They are equal'
			
class LanguageGenius():
	def __init__(self,name):
		self.name = name
		self.words = {}
	def backwards(self,a):
		print(a[::-1])
	def define(self,word):
		if word not in self.words:
			definition = raw_input('Definition of %s: '%word)
			self.words.update({word:definition})
		else:
			print("'"+word+"'" + " Already defined")
			
			
silas = MathGenius('Silas',13)
silas.add(2,4)
silas.subtract(9292,323)
silas.multiply(3243,333)
silas.divide(2333,43)

print(silas.name)
print(silas.age)
silas.school='ieie'
print(silas.school)
print(silas.bigger(100,101))

molly = LanguageGenius('Moll')
solly.backwards('Hello')
molly.define('kamira')
molly.define('door')
molly.define('door')
print(molly.words)

# Create a class for the LagnaugeGenius. Think of some homework subjects that your Language genius could do for you.
# Implement the necessary functions and variables in your class.

