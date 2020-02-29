from __future__ import print_function
#Exercise 8.6 Rewrite the program that prompts the user for a list of numbers and
#prints out the maximum and minimum of the numbers at the end when the user enters done.
#Write the program to store the numbers the user enters in a list and use the max() and min() functions
#to compute the maximum and minimum numbers after the loop completes.

smallest = None
largest = None
lst = list() #create an empty list

while True:

	userinp = raw_input("Enter number:")
	if userinp == 'done': break
	
	try:
		num = int(userinp)
		lst.append(num)
		
		#if smallest == None or num < smallest:
				#smallest = num
		#if largest == None or num > largest:
				#largest = num
				
	except:
		print("Invalid input")
		continue
		
print("Maximum is", max(lst))
print("Minimum is", min(lst))

