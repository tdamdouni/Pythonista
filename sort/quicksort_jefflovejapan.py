from __future__ import print_function
# https://gist.github.com/jefflovejapan/7493176

# leftmark
# rightmark
# pivot
#
# Assume pivot is in pos 0: pos(leftmark) always going to be pos(pivot) + 1
# Going to recurse on the different parts
# going to do everything in place
#
# Either need to pass the whole input list or set it to global in order to sort
# in place. Also need to pass around indices to indicate where we are in the
# input list

# Terminating condition -- i, j = start, end of sublist

import pudb
import random


def quicksort(input, left=0, right=0):
    pivot_index = left
    ind_l = pivot_index + 1

    if right == 0:
        right = len(input) - 1

    ind_r = right

    while 1:
        # Looking for the first term that's greater than the pivot
        # because we're going to swap it to the right side
        while ind_l <= right and input[ind_l] <= input[pivot_index]:
            ind_l += 1

        while ind_r > pivot_index and input[ind_r] >= input[pivot_index]:
            ind_r -= 1

        if ind_r < ind_l:
            break

        input[ind_l], input[ind_r] = input[ind_r], input[ind_l]
            
    if input[pivot_index] > input[ind_r]:
        input[pivot_index], input[ind_r] = input[ind_r], input[pivot_index]
    if ind_r - left >= 1:
        quicksort(input, left=left, right=ind_r)
    if right - ind_r >= 1:
        quicksort(input, left=ind_r + 1, right=right)


def main():
    input = random.sample(range(100), 50)
    quicksort(input)
    print(input)

if __name__ == '__main__':
    main()
