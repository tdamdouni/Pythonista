from __future__ import print_function
#8.4 Open the file romeo.txt and read it line by line.
#For each line, split the line into a list of words using the split() method.
#The program should build a list of words. For each word on each line check to see
#if the word is already in the list and if not append it to the list.
#When the program completes, sort and print the resulting words in alphabetical order.


fhand = open('romeo.txt')           #open file name
lst = list()                        #create an empty list

for line in fhand:                  #For loop traverses each line in file. Next, for each line
	splitz = line.split()           #split the line into a list of words using the split function
	print(splitz)                   #The program has built a list of words.
	print(len(splitz))
	for i in range(len(splitz)):    #The range function creates a list and gives it back to us.
																																#It also corresponds to items in splitz list.
		if splitz[i] not in lst:
			lst.append(splitz[i])
			
lst.sort()
print(lst)

