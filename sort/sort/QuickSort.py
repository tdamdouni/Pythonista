'''
Created on May 25, 2013

@author: Giacomo
'''
from __future__ import print_function


from structure.basic.Stack import StackArrayList as Stack
import random


def recursiveQuickSort(L, det = False):
    recQuickSort(L, 0, len(L) - 1, det)
    
    
def recQuickSort(L, left, right, det=False):   
    if left >= right:
        return
    
    mid = partition(L, left, right, det)
    recQuickSort(L, left, mid - 1, det)
    recQuickSort(L, mid + 1, right, det)


def partition(L, left, right, det = False):
    inf = left
    sup = right + 1
    
    if not det:
        mid = random.randint(left, right)
        L[left], L[mid] = L[mid], L[left]
    
    mid = left 
    
    while True:
        inf += 1
        while inf <= right and L[inf] <= L[left]:
            inf += 1
        
        sup -= 1
        while L[sup] > L[left]:
            sup -= 1
        
        if inf < sup:
            L[inf], L[sup] = L[sup], L[inf]
        else:
            break
        
    L[left], L[sup] = L[sup], L[left]
    
    return sup


def iterativeQuickSort(L, det = False):
    iterQuickSort(L, 0, len(L) - 1, det)


def iterQuickSort(L, left, right, det = False):
    theStack = Stack()
    theStack.push(left)
    theStack.push(right)
    while not theStack.isEmpty():
        right = theStack.pop()
        left = theStack.pop()
        
        if right <= left:
            continue
        
        mid = partition(L, left, right, det)
        
        theStack.push(left)
        theStack.push(mid - 1)
        
        theStack.push(mid + 1)
        theStack.push(right)
        
        
def testRecursiveQuickSort(L):
    a = L
    b = L
    
    print("\n")
    
    print("# Deterministic #")
    recursiveQuickSort(a, True)
    print(a)
    
    print("\n\n")
    
    print("# Randomic #")
    recursiveQuickSort(b, False)
    print(b)
    
def testIterativeQuickSort(L):
    a = L
    b = L
    
    print("\n")
    
    print("# Deterministic #")
    iterativeQuickSort(a, True)
    print(a)
    
    print("\n")
    
    print("# Randomic #")
    iterativeQuickSort(b, False)
    print(b)
    

if __name__ == "__main__":
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")    
    
    print("### RecursiveQuickSort ###")
    testRecursiveQuickSort(L)
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")    
    
    print("### IterativeQuickSort ###")
    testIterativeQuickSort(L)
    
    print("\n\n")