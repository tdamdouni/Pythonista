import sys
from numpy.random import randint  # much faster than random.randint
 
def __quick_sort__(list, left, right):
    def partition(list, left, right, pivotidx):
        pivot = list[pivotidx]
        list[right], list[pivotidx] = list[pivotidx], list[right]
 
        for i in range(left, right):
            if list[i] < pivot:
                list[i], list[left] = list[left], list[i]
                left += 1
 
        list[left], list[right] = list[right], list[left]
        return left
 
    if right > left:
        pivotidx = randint(left, right)
        pivotidx = partition(list, left, right, pivotidx)
        __quick_sort__(list, left,       pivotidx)
        __quick_sort__(list, pivotidx+1, right)
 
    return list
 
def quick_sort(list):
    return __quick_sort__(list, 0, len(list)-1)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        list = []
        with open(sys.argv[1], 'r') as f:
            for line in f:
                list.append(int(line))

        sorted_list = quick_sort(list)
        print(sorted_list)
    else:
        print("Usage: %s [list file]" % sys.argv[0])
