'''
Created on May 25, 2013

@author: Giacomo
'''
from __future__ import print_function


def selectionSort(L):
    for k in range(len(L) - 1):
        minPos = k
        for j in range(k + 1, len(L)):
            if L[j] < L[minPos]:
                minPos = j
        L[minPos], L[k] = L[k], L[minPos]
        
        
def testSelectionSort(L):
    selectionSort(L)
    print(L)
    

if __name__ == "__main__":
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")    
    
    print("### SelectionSort ###")
    testSelectionSort(L)
    
    print("\n\n")