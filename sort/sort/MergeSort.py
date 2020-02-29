'''
Created on May 25, 2013

@author: Giacomo
'''
from __future__ import print_function


def mergeSort(L):
    recursiveMergeSort(L, 0, len(L) - 1)

def recursiveMergeSort(L, left, right):    
    if left >= right:
        return
    
    mid = int((left + right) / 2)
    
    recursiveMergeSort(L, left, mid)
    recursiveMergeSort(L, mid + 1, right)
    mergePartitions(L, left, mid, right)

def mergePartitions(L, left, mid, right):        
    idLeft = left
    idRight = mid + 1
    tempList = []
    
    while True :
        if L[idLeft] < L[idRight]:
            tempList.append(L[idLeft])
            idLeft += 1

            if idLeft > mid: 
                for v in L[idRight:right + 1]:
                    tempList.append(v)
                    
                break 
        else:   
            tempList.append(L[idRight])
            idRight += 1

            if idRight > right: 
                for v in L[idLeft:mid + 1]:
                    tempList.append(v)
                    
                break 
            
    for i in range(left, right + 1):
        L[i] = tempList[i - left]
        
        
def testMergeSort(L):
    mergeSort(L)
    print(L)
    

if __name__ == "__main__":
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")    
    
    print("### MergeSort ###")
    testMergeSort(L)
    
    print("\n\n")