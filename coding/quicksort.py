# https://gist.github.com/Subject22/6d340d7e2ef9a8f3ff1b49c48af57e7e

def qs(items):
	pivot = items[0]

	smaller = []
	equal = []
	larger = []

	for item in items:
		if item < pivot:
			smaller.append(item)
		elif item > pivot:
			larger.append(item)
		else:  # item == pivot
			equal.append(item)
	
	return qs(smaller) + equal + qs(larger)
	
	
def qs_in_place(array, begin=0, end=None):
    if end is None:
        end = len(array) - 1
    
    if begin >= end:
        return
    
    pivot = partition(array, begin, end)
    qs_in_place(array, begin, pivot-1)
    qs_in_place(array, pivot+1, end)
    
    
def partition(array, start, end):
    pivot = start
    
    for i in range(start+1, end+1):
        if array[i] <= array[start]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
    
    array[pivot], array[start] = array[start], array[pivot]
    
    return pivot
