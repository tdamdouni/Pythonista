from __future__ import print_function
#Function definition
def quicksort( arr, x, y ):
	if(y - x < 1):
		return	
	start = arr[x]
	i = x
	j = y
	change = False;
	while(i != j):
		while(i != j):
			if(arr[j] < start):
				arr[i] = arr[j]
				change = True
				break
			else:
				j -= 1
		while(i != j):
			if(arr[i] > start):
				arr[j] = arr[i]
				break
			else:
				i += 1
	if(change):
		arr[i] = start
	if(i - x > 1):
		quicksort(arr, x, i - 1)
	if(y - i > 1):
		quicksort(arr, i + 1, y)

#!/usr/bin/python
length = int(raw_input("input the length of array"))
arr = []
for num in range(0, length):
	temp = int(raw_input("input the node of the Array:"))
	arr.append(temp)
quicksort( arr, 0, length - 1 )
print(arr)


