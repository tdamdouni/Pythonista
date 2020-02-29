# If your head is in the clouds, good! You can use programming to [explore the planets](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/astronomy.py)!

# If your head is in the clouds, good! 
# This program allows you to get various properties of planets in the solar system


# This data was pulled offline
"""
DATA:				
	           Rad   Mass(kg) Dens   Abo  Vo     Rot(days)
Mercury      2440  3.30e23  5.43  .11  -1.9    58.6
Venus        6052  4.87e24  5.24  .65  -4.4    -243 
Earth        6378  5.97e24  5.52  .30   -      0.99
Mars         3397  6.42e23  3.93  .15  -2.0    1.03
Jupiter     71492  1.90e27  1.33  .52  -2.7    0.41
Saturn      60268  5.68e26  0.69  .47   0.7    0.45
Uranus      25559  8.68e25  1.32  .51   5.5   -0.72
Neptune     24766  1.02e26  1.64  .41   7.8    0.67
Pluto        1150  1.27e22  2.06  .55  13.6   -6.39  (z)
"""
from __future__ import print_function

# There is a little math involved, so we need to import the math module
#Module
import math

# This is lesson 1
#Integer
lesson_number = 1

# We need a title for this code.
#String
title = "Calculate the Area of a Planet\n"

#\n is like hitting the RETURN key. A backslash is an escape character.

# Of course PI is not the pie you eat, but I thought it was funny.
# These variables are the ingredients we need for this program.
#Variables
pie = math.pi 
e = math.e
radius_of_my_head = None
planet_to_head_ratio = None

# We need to know what units we will use
abbr = '(km)' 
km = 'kilometers'


# Dictionaries or Associative arrays can store different types of variables within one variable.
# They are used for inventories in video games. We are just storing the data I saw in the internet.
mercury = {'name':'Mercury','radius':2440,'units':km,'abbr':abbr}
venus = {'name':'Venus','radius':6052,'units':km,'abbr':abbr}
earth = {'name':'Earth','radius':6378,'units':km,'abbr':abbr}
mars = {'name':'Mars','radius':3397,'units':km,'abbr':abbr}
jupiter = {'name':'Jupiter','radius':71492,'units':km,'abbr':abbr}
saturn = {'name':'Saturn','radius':60268,'units':km,'abbr':abbr}
uranus = {'name':'Uranus','radius':25559,'units':km,'abbr':abbr}
neptune = {'name':'Neptune','radius':24766,'units':km,'abbr':abbr}
pluto = {'name':'Pluto','radius':1150,'units':km,'abbr':abbr}

sun = {'name':'Sun','radius':695000,'units':km,'abbr':abbr}
moon = {'name':'Moon','radius':1738,'units':km,'abbr':abbr}


# A little note on how to add new things to a dictionary
#Add to dictionary
#list['new_key']='new_value'


# We will store our planets and celestial bodies in a regular ol' array
#List
planet = [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune,pluto]
body = [sun,moon]


# Now we need to DO STUFF with these variables
# This function calculates the area of the planet using the formula for the area of a sphere (had to look it up)
def Calculate_Area(planet_arg):
	area = 4 *(pie * math.pow(planet_arg['radius'],2))
	print('The area of ' + planet_arg['name'] + ' is ' + str(area) + ' ' + planet_arg['units'] + planet_arg['abbr'])
	return area


print("Lesson " + str(lesson_number))
print(title)

# Using the Calculate_Area() function:
Calculate_Area(mercury)
Calculate_Area(planet[8])
Calculate_Area(earth)

# Getting the radius of the planet using another formula I looked up on google and returning it
def Get_Radius(planet_arg):
	print('The radius of ' + planet_arg['name'] + ' is ' + str(planet_arg['radius']) + ' ' + planet_arg['units'] + planet_arg['abbr'])
	return planet_arg['radius']

# We can return the mass of something given it's coefficient and power
def Set_Mass(coefficient,power):
	mass = str(coefficient) + 'e' + str(power)
	return mass
	
# And we can get the mass or a particular planet
def Get_Mass(planet_arg):
	print('The mass of ' + planet_arg['name'] + ' is ' + planet_arg['mass'])
	return planet_arg['mass']
	

# Now let us set the masses of the planets
mercury['mass']= Set_Mass(3.30,23)
venus['mass']= Set_Mass(4.87,24)
earth['mass']= Set_Mass(5.97,24)
mars['mass']= Set_Mass(6.42,23)
jupiter['mass']= Set_Mass(1.90,27)
saturn['mass']= Set_Mass(5.68,26)
uranus['mass']= Set_Mass(8.68,25)
neptune['mass']= Set_Mass(1.09,26)
pluto['mass']= Set_Mass(1.27,22)

# And we can get their radii 
Get_Radius(pluto)
Get_Radius(sun)

# Or their mass
Get_Mass(earth)

# Get the mass and radius of other planets!
# Create your own planet, and set it's mass and radius. Give it a cool name though!



