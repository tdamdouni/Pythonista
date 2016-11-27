# http://code.activestate.com/recipes/579051-get-inversion-number-of-a-permutation/

# coding: utf-8

def I(tupPerm):
	tmpList=[]
for k in tupPerm:
	tmpL=list(tupPerm)
	kIndex=tmpL.index(k)
	copyTup=[x for x in tmpL]
	copyTup2=copyTup[(kIndex+1):]
	ctInversionsForKList=[]
	for x in copyTup2:
		if x<k:
			ctInversionsForKList.append(1)
			tmpList.append(sum(ctInversionsForKList))
return sum(tmpList)

def p(n,r):
	from itertools import permutations
	tmp=permutations([x for x in range(1,n+1)],r)
	tupPermList=list(tmp)
return tupPermList

def convertStdForm(tupPerm):
	tmpS=''
for u in tupPerm:
	tmpS+=str(u)
return eval(tmpS)     

ans=""
from itertools import permutations
while ans!="N":
	print()
n=eval(input("Please enter the int n for which permutations will be taken from: "))
print()
tupPerms=p(n,n)
permsWithLessThan3Inversions=[]
for tup in tupPerms:
	if I(tup)<3:
		permsWithLessThan3Inversions.append(tup)   
stdPermForm=[]
for tup in permsWithLessThan3Inversions:
	stdPermForm.append(convertStdForm(tup))
print("The number of permutations of length ",n," from the set ",[x for x in range(1,n+1)]," that have inversion numbers no greater than 2 are given as follows: ")
print()
for x in stdPermForm:
	print(x,end=", ")
print()
