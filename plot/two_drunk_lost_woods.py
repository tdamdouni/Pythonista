from pylab import *
from random import *

n=0


x1p=[0]
y1p=[0]
x1=0
y1=0

x1se=[x1]
y1se=[y1]

x2p=[10]
y2p=[0]
x2=10
y2=0

x2se=[x2]
y2se=[y2]
found=False

while found==False:
	step1=randint(1,4)
	if step1==1: y1=y1+1
	if step1==2: x1=x1+1
	if step1==3: y1=y1-1
	if step1==4: x1=x1-1
	x1p=x1p+[x1]
	y1p=y1p+[y1]
	
	step2=randint(1,4)
	if step2==1: y2=y2+1
	if step2==2: x2=x2+1
	if step2==3: y2=y2-1
	if step2==4: x2=x2-1
	x2p=x2p+[x2]
	y2p=y2p+[y2]
	n=n+1
	
	r=sqrt((x2-x1)**2+(y2-y1)**2)
	if r<2.:found=True
print(n)
print(x1,y1)
print(x2,y2)
x1se=x1se+[x1]
y1se=y1se+[y1]
x2se=x2se+[x2]
y2se=y2se+[y2]

plot(x1p,y1p, linewidth=3, alpha=.5)
plot(x2p,y2p, linewidth=3, alpha=.5)
scatter(x1se,y1se,s=60,c='r')
scatter(x2se,y2se, s=60, c='y')
grid(True)
show()

