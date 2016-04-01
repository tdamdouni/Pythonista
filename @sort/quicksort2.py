import random

class Quicksort:
    def __init__(self):
        self.l = [None] + list(range(1,100))
        self.l= [k*k % 17 for k in list(range(101))]
        

    def partition(self, A, a, b):
        self.count = self.count + 1
        i = a-1
        j = a
        m = random.randint(a, b-1)    #select a random pivot point
        A[m], A[b-1] = A[b-1], A[m]
        while j <= b-2:
            self.count = self.count + 1
            if A[j] <= A[b-1]:
                i = i + 1
                A[i], A[j] = A[j], A[i]
            j = j + 1
        A[i+1], A[b-1] = A[b-1], A[i+1]
        return i + 1   # i+1 is the index of where the pivot lands
    
    def quicksort(self, A, a, b):
        self.count = self.count + 1
        if a >= b - 1:
            return
        x = self.partition(A, a, b)
        self.quicksort(A, a, x)
        self.quicksort(A, x+1, b)

    def run(self):
        self.count = 0    #to count the running time
        q.quicksort(q.l, 1, len(q.l))
        print("Count = ", self.count)
        
q = Quicksort()
