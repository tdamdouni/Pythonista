# Pythonista 2.7: List of Primes, Rotating a List, Maximum of a List, Vandermonde Matrix

_Captured: 2015-09-30 at 17:43 from [edspi31415.blogspot.de](http://edspi31415.blogspot.de/2014/08/pythonista-27-list-of-primes-rotating.html)_

![](https://lh6.googleusercontent.com/-Nt2SMMCvITw/U--ZvmKQtOI/AAAAAAAACgQ/hCOisOQCdqc/1F4DEEFD-0C71-4B6F-8AC3-973F5D6CC99C.jpg)

List of Primes 

# list of primes to n  
# 8/13/2014  
import math  
n=input('maximum n (n>2):')  
# start the list of primes   
l=[2]  
# test all integers from 3 to n  
for k in range(3,n+1):  
# set flag   
x=0  
for j in range(2,k-1):  
# test for composite menu  
if math.fmod(k,j)==0:  
x=1  
if x==0:  
# add to list that k is prime  
l.append(k)  
# return list of primes  
print l

Example: n = 44 returns

[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 43]

I am getting used to the way the range command operates and how the indices go from 0 to n-1, instead of how programming calculators have it: 0 to n.

Rotate a List to the Right 

# rotate a list to the right r places  
import math  
l=input('list: ')  
r=input('number of places: ')  
n=len(l)  
# rotation loop  
for k in range(r):  
# remember range starts at 0  
# remove last element  
w=l.pop()  
# insert that element at position 0  
l.insert(0,w)  
# print rotated list  
print l

Example:

List: [0, 4, -6, 8]

Number of Places: 2; return [-6, 8, 0, 4]  
Number of Places: 3; return [4, -6, 8, 0]

Maximum of a List

import math  
l=input('list: ')  
# sort the list - without a loop  
l.sort()  
print l.pop()

Example: [12, 16, 28, 3, 4] returns 28

Vamdermonde Matrix

# building the Vandermonde matrix a row at a time  
import math  
v=input('vector: ')  
n=len(v)

print('Vandermonde Matrix')

# main routine  
# power  
for i in range(n):  
l=[]  
# element build  
for k in range(n):  
l.append(math.pow(v[k],i))  
print l

Example:  
[0.8, 0.6, -0.5] returns

[1, 0.8, 0.64]  
[1, 0.6, 0.36]  
[1, -0.5, 0.25]

Enjoy!

Have a great weekend!

Eddie

This blog is property of Edward Shore. 2014

![](https://lh4.googleusercontent.com/-710rjxlKPx4/U--ZuacXP3I/AAAAAAAACgI/x8NoeMMITJg/57AE131F-A8C2-415F-AD4A-A3D23A0D4625.jpg)
