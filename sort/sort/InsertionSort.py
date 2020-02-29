'''
Created on May 25, 2013

@author: Giacomo
'''
from __future__ import print_function


def insertionSortUp(L):
    for k in range(1, len(L)):
            
        val = L[k]
        for pos in range(k - 1, -1, -1):
            if L[pos] <= val:
                break
        else:
            pos = -1
        
        if pos < k - 1:
            for j in range(k, pos + 1, -1):
                L[j] = L[j - 1]
            L[pos + 1] = val
        

def insertionSortDown(L):
    for k in range(1, len(L)):
            
        val = L[k]
        for pos in range(k):
            if L[pos] > val:
                break
        else:
            pos = k 
                
        if pos < k: 
            for j in range(k, pos, -1):
                L[j] = L[j - 1]
            L[pos] = val
        
        
def testInsertionSortUp(L):
    insertionSortUp(L)
    print(L)
    
def testInsertionSortDown(L):
    insertionSortDown(L)
    print(L)
    

if __name__ == "__main__":
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")    
    
    print("### InsertionSortUp ###")
    testInsertionSortUp(L)
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")
    
    print("### InsertionSortDown ###")
    testInsertionSortDown(L)
    
    print("\n\n")