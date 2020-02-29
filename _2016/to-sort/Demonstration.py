# coding: utf-8

# https://gist.github.com/ejetzer/7685539

from __future__ import print_function
from math import sqrt, pi

# Program examples

def double(some_number):
	return 2 * some_number

def dbl(n):
	return  2*n

print(dbl(3))

def sdfsdf(dfdf):
	return 2*dfdf

print(sdfsdf(3))

def double(number):
	return 2 * number

print(double(3))

def f(x):
	return 2*x

print(f(3))

def cylinder_volume(height, base_radius):
	return pi * base_radius**2 * height

def quadratic_roots(a, b, c):
	discriminant = b**2 - 4*a*c
	if discriminant > 0:
		root1 = ( -b + sqrt(discriminant) ) / ( 2*a )
		root2 = ( -b - sqrt(discriminant) ) / ( 2*a )
		return root1, root2
	elif discriminant == 0:
		root = -b / (2*a)
	else:
		return None

roots = quadratic_roots(1, 0, -1)
print(roots)

my_tuple = (1, 2, 3)
my_list = [1, 2, 3]

print((my_tuple[2], my_list[2]))

# Some vector, represented by a list

some_vector = [1, 2, 3]
print(some_vector[2])

some_vector[2] = 5
print(some_vector[2])

# Some vector, represented as a tuple

some_vector = (1, 2, 3)
print(some_vector[2])

try: 
	some_vector[2] = 5
except Exception as e:
	print(e)
	
some_tuple = (1, 2, 3)
print(some_tuple)

some_tuple = (some_tuple[0], 7, some_tuple[2])
print(some_tuple)


first_vector = [1, 2, 3]
second_vector = [3, 2, 1]
print(first_vector, second_vector)

third_vector = []
index = 0
while index < 3:
	added_terms = first_vector[index] + second_vector[index]
	third_vector.append(added_terms)
	index += 1
print(third_vector)

third_vector = []
for index in range(3):
	added_terms = first_vector[index] + second_vector[index]
	third_vector.append(added_terms)
print(third_vector)

def add_vectors(first_vector, second_vector):
	added_terms = first_vector[0] + second_vector[0]
	if len(first_vector) > 1:
		return [added_terms] + add_vectors(first_vector[1:], second_vector[1:])
	else:
		return [added_terms]
third_vector = add_vectors(first_vector, second_vector)
print(third_vector)

a = [1, 2, 3, 4, 5]
print(a)
print(a.pop())
print(a)

first_vector = [1, 2, 3]
second_vector = [3, 2, 1]
third_vector = [first_vector[index] + second_vector[index] for index in range(3)]
print(third_vector)