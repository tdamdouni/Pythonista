from pylab import *
from random import *

def drunk(s):
# s is the distance the two drunks start from each other
	n=0
	x1=0
	y1=0
	
	x2=s
	y2=0
	
	found=False
	
	while found==False:
		step1=randint(1,4)
		if step1==1: y1=y1+1
		if step1==2: x1=x1+1
		if step1==3: y1=y1-1
		if step1==4: x1=x1-1
		
		step2=randint(1,4)
		if step2==1: y2=y2+1
		if step2==2: x2=x2+1
		if step2==3: y2=y2-1
		if step2==4: x2=x2-1
		
		n=n+1
		
		r=sqrt((x2-x1)**2+(y2-y1)**2)
		if r<2.:found=True
		if n>10000:
			found=True
			n=-1
			
	return(n)
	
mov=[]
runs=1000
nbetter=0
for m in range(runs):
	temp=drunk(10)
	if temp !=(-1):
		mov=mov+[temp]
	if temp<332 and temp>0:
		nbetter=nbetter+1
		
##for m in range(runs):
##    mov=mov+[drunk(10)]

print(len(mov))
print(mean(mov))
print(std(mov))
print(nbetter)
hist(mov, alpha=.5)
grid(True)
xlabel('Number of Moves')
title('Starting 10 Apart')
show()

