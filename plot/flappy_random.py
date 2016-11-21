from pylab import *
import random as rd

total=150
p=.587

np=[]
sp=[]

n=0

while n<total:
    temp=rd.random()
    tempscore=0
    while temp>=p:
        tempscore=tempscore+1
        temp=rd.random()
        
    n=n+1
    np=np+[n]
    sp=sp+[tempscore]

scatter(np,sp, s=40)
xlabel('Number of Trials')
ylabel('Score')
show()
