#!/usr/bin/env python

from common import debug

def swap(lst, a, b):
    """Inplace swap"""
    lst[a], lst[b] = lst[b], lst[a]

def first_element(lst):
    """Just return index of first element from the list"""
    return 0

def middle_element(lst):
    """Just return index of middle element from the list"""
    return last_element(lst) / 2

def last_element(lst):
    """Just return index of last element from the list"""
    return len(lst) - 1

def median_of_three(lst):
    """
    Return index of median element of first, middle and last

    >>> median_of_three([0, 2, 3, 100, 5, 7, 20])
    6
    >>> median_of_three([3,2,1])
    1
    >>> median_of_three([3,2,1,0,17])
    0
    """
    a, b, c = first_element(lst), middle_element(lst), last_element(lst)
    # Little cheat =))
    return sorted([ a, b, c ], key=lambda x: lst[x])[1]

@debug
def partition(lst, pivot_idx):
    """Partition array inplace"""
    if pivot_idx != 0:
        swap(lst, pivot_idx, 0)
    pivot = lst[0]

    i = 1
    for j, element in enumerate(lst[1:], 1):
        if element < pivot:
            swap(lst, i, j)
            i += 1
    i -= 1
    swap(lst, i, 0)
    return i

@debug
def quicksort(lst, choose_pivot=first_element):
    """
    Quick sort algorithm with pluggable pivot-functions

    >>> quicksort([1,2,3,4,5])
    (10, [1, 2, 3, 4, 5])
    >>> quicksort([5,4,3,2,1])
    (10, [1, 2, 3, 4, 5])
    >>> quicksort([1])
    (0, [1])
    >>> quicksort([1,2])
    (1, [1, 2])

    >>> quicksort([5,2,4,1,0,3], choose_pivot=last_element)
    (8, [0, 1, 2, 3, 4, 5])
    >>> quicksort([5,2,4,1,0,3], choose_pivot=first_element)
    (12, [0, 1, 2, 3, 4, 5])
    >>> quicksort([5,2,4,1,0,3], choose_pivot=median_of_three)
    (9, [0, 1, 2, 3, 4, 5])
    """
    if len(lst) <= 1:
        return 0, lst
    # Index of pivot
    i = partition(lst, choose_pivot(lst))

    # Recurse on partitioned lists
    left_half, right_half = lst[:i], lst[i+1:]
    comp1, left_half = quicksort(left_half, choose_pivot)
    comp2, right_half = quicksort(right_half, choose_pivot)

    result = left_half + [lst[i]] + right_half
    total_comp = comp1 + comp2 + (len(result) - 1)
    return (total_comp, result)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", type="string", dest="file", default="QuickSort.txt")
    (options, args) = parser.parse_args()

    with open(options.file) as lines:
        data = list(lines)

    for func in [first_element, last_element, median_of_three]:
        print quicksort([int(line) for line in data], choose_pivot=func)[0]
