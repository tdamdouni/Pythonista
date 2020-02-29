'''
Created on May 25, 2013

@author: Giacomo
'''
from __future__ import print_function


from structure.basic.Queue import QueueDeque as Queue
import math

def radixSort(L, limit, base):
    cifrek = int(math.ceil(math.log(limit + 1, base)))
    
    for t in range(1, cifrek + 1):
        bucket = []
        for i in range(0, base):
            bucket.append(Queue())
        for j in range(0, len(L)):
            cifratj = L[j] % math.pow(base, t)
            cifratj = int(cifratj / math.pow(base, t - 1))
            bucket[cifratj].enqueue(L[j])

        j = 0
        for e in bucket:
            while not e.isEmpty():
                L[j] = e.dequeue()
                j += 1
                
                
def testRadixSort(L):
    radixSort(L, 1000000, 10)
    print(L)
    

if __name__ == "__main__":
    
    print("\n\n")
    
    print("# L #")   
    L = [3,2,1,7,6,5,4,10,9,8]
    print(L)
    
    print("\n\n")    
    
    print("### RadixSort ###")
    testRadixSort(L)
    
    print("\n\n")