# coding: utf-8

# https://forum.omz-software.com/topic/2959/sympy-solve-rounds-to-0/2

from sympy import *
x, y, z = symbols('x y z')

# this works because its only 1e-5
rslt = solve(Eq(0+1e-5, x), x, rational=False))
rslt = rslt[0]
print rslt

#this outputs zero cause number is too small? :(
rslt = solve(Eq(0+1e-10, x), x, rational=False))
rslt = rslt[0]
print rslt
