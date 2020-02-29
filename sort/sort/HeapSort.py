'''
Created on May 25, 2013

@author: Giacomo
'''
from __future__ import print_function

from structure.basic.Heap import HeapMax as Heap

def heapSort(L):
    heap = Heap(L);
    
    heap.heapify();
    
    while not heap.isEmpty():
        heap.deleteMax() 
        
        
def testHeapSort(L):
    heapSort(L)
    print(L)
    

if __name__ == "__main__":
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")
    
    print("### HeapSort ###")
    testHeapSort(L)
    
    print("\n\n")