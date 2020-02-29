from __future__ import print_function
# When making 3d video games, vector math is very helpful. Simulate the [dot and cross product](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/dotAndCross.py) with Python!

import math

V1 = [0,7,1]
V2 = [0,0,6]

V3 = [0,7,0]
V4 = [0,0,6]

V5 = [4,5,11]
V6 = [-3,-2,2]

# Dot Product
def dot(A,B):
	dotprod = A[0]*B[0] + A[1]*B[1] + A[2]*B[2]
	if dotprod == 0:
		print('perpendicular')
	elif dotprod > 0:
		print('acute')
	elif dotprod < 0:
		print('obtuse')
	return dotprod

# Implementation
print(dot(V1,V2))
print(dot(V2,V1))
print(dot(V3,V4))
print(dot(V5,V6))


# Cross Product
def cross(A,B):
	x = 0
	y = 1
	z = 2
	cx = (A[y]*B[z]) - (A[z]*B[y])
	cy = (A[z]*B[x]) - (A[x]*B[z])
	cz = (A[x]*B[y]) - (A[y]*B[x])
	return (cx,cy,cz)


# Implementation
print(cross(V1,V2))
print(cross(V2,V1))


# Add and subtract vectors
def vecDiff(A,B):
	diff = []
	for x in range(3):
		diff.append(A[x]-B[x])
	return diff

def vecSum(A,B):
	sum = []
	for x in range(3):
		sum.append(A[x]+B[x])
	return sum

def vecProduct(A,B):
	prod = []
	for x in range(3):
		prod.append(A[x]*B[x])
	return prod
