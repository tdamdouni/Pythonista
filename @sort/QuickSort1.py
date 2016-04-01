import random
import unittest

def quicksort(array):
    def swap(a, b):
        temp = array[a]
        array[a] = array[b]
        array[b] = temp
        
    def partition(array, begin, end):
        # pick pivot elem and move to end
        pivotIndex = random.randint(begin, end)
        pivotElem = array[pivotIndex]
        swap(pivotIndex, end)
        
        swapindex = begin
        for i in xrange(begin, end):
            if array[i] < pivotElem:
                swap(swapindex, i)
                swapindex += 1
            
        swap(swapindex, end)
        return swapindex
    
    def doquicksort(array, begin, end):
        arraylen = end-begin+1
        
        if arraylen < 2:
            return
        
        pivotIndex = partition(array, begin, end)
        
        doquicksort(array, begin, pivotIndex-1)
        doquicksort(array, pivotIndex+1, end)

    doquicksort(array, 0, len(array)-1)
    
class QuickSortTestFunctions(unittest.TestCase):

    def isSorted(self, array):
        if len(array) < 2:
            return True
        
        prev_index = 0
        
        for i in xrange(1, len(array)):
            if array[prev_index] > array[i]:
                return False
            prev_index = i
            
        return True

    def sort_and_test(self, array):
        quicksort(array)
        return self.isSorted(array)
    
    def test_sorted_empty(self):
        self.assertTrue(self.sort_and_test([]))

    def test_sorted_one(self):
        self.assertTrue(self.sort_and_test([1]))

    def test_sorted_two(self):
        self.assertTrue(self.sort_and_test([2,1]))
        self.assertTrue(self.sort_and_test([1,1]))
        
    def test_random(self):
        for i in xrange(0, 100):
            array = [ random.randint(-1000000, 1000000) for j in xrange(0, random.randint(20,100))]
            self.assertTrue(self.sort_and_test(array))

if __name__ == "__main__":
    
    array = [ random.randint(0, 100) for i in xrange(0, 20) ]
    
    print("Initial array is:", array)
    quicksort(array)
    print("Quicksorted array is:", array)

    unittest.main()