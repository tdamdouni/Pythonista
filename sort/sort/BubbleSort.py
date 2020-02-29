'''
Created on May 25, 2013

@author: Giacomo
'''
from __future__ import print_function


def bubbleSort(L):
    swapped = True
    while swapped:
        swapped = False
        for j in range(len(L) - 1):
            if L[j] > L[j + 1]:
                L[j], L[j + 1] = L[j + 1], L[j]
                swapped = True


def testBubbleSort(L):
    bubbleSort(L)
    print(L)
    

if __name__ == "__main__":
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")    
    
    print("### BubbleSort ###")
    testBubbleSort(L)
    
    print("\n\n")