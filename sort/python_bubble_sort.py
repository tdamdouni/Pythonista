from __future__ import print_function
### Example of a bubble sort in Python where you are given
### a list of unordered numbers and need to order them


ls = [2,1,3,5,4,7,7,9,9,9,8]

def bubbleSort(nums): # Bubble Sort Algorithm
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[j] < nums[i]:
                nums[j], nums[i] = nums[i], nums[j]

    print(nums)

bubbleSort(ls)
