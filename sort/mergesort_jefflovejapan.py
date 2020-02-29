from __future__ import print_function
# https://gist.github.com/jefflovejapan/7493179

# Interactive Python http://interactivepython.org/courselib/static/pythonds/SortSearch/sorting.html
# Example given doesn't allocate new temp array for each mergejoin step

def mergesort(input):
	if len(input) in [0, 1]:
		return input
	else:
		midp = len(input) // 2
		left = mergesort(input[:midp])
		right = mergesort(input[midp:])
		return mergejoin(left, right)
		
		
def mergejoin(left, right):
	sorted_list = []
	while left or right:
		if left and right:
			if left[0] < right[0]:
				sorted_list.append(left.pop(0))
			else:
				sorted_list.append(right.pop(0))
		else:
			if left:
				sorted_list.extend(left)
				break
				
			if right:
				sorted_list.extend(right)
				break
	return sorted_list
	
	
import random
input = random.sample(range(100), 11)
print(mergesort(input), len(input))

