# coding: utf-8

# https://forum.omz-software.com/topic/2412/share-code-doc-strings-from-a-class/12

# program, which will find all such numbers between 1000 and 3000 (both included) such that each digit of the number is an even number

from __future__ import print_function
L=[]
j=0
for i in range(1000,3001):
# Changing the integer to string to check each digit
	s=str(i)
while (j<=len(s)):
	if(int(s[j])%2==0):
		j=j+1
	L.append(s);
	print(L);
	
# Answer:
L=[]
for i in range(1000,3001):
	s=str(i)
	j=0
	
while (j<len(s)):
	if(int(s[j])%2==0):
		flag=1
	else:
		flag=0
	break
	
#print j
j=j+1
if flag==1:
	L.append(s)
print(L);

# My answer:
def test():
	return [str(i) for i in xrange(1000, 3001) if not i% 2]
	
print(test())
#i also mention generator syntax to reduce memory dependence

