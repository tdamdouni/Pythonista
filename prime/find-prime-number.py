# https://forum.omz-software.com/topic/3614/prime-number-finder

import time

print('Made by Yasas Kulatunga, Dhari Prashanth and Dhivy Prashanth')
print(' ')
number = int(input("Enter a Number: "))
print(' ')
time.sleep(0.5)
print('THINKING.')
time.sleep(0.5)
print('THINKING..')
time.sleep(0.5)
print('THINKING...')
time.sleep(0.5)

print(' ')
c = 0
while number:
	for i in range(2,number):
		if number % i == 0:
			print(str(i),"times",str(number//i),"is",str(number))
			time.sleep(0.3)
			c = c + 1
	if c == 0:
		print(' ')
		print(str(number),"has no factors apart from 1 and itself, therefore it is a prime number")
		print(' ')
		time.sleep(0.3)
	else:
		print(' ')
		print(str(number),"is not a prime number, the number has factors more than 1 and the number itself.")
		print(' ')
		time.sleep(0.3)
	number = int(input('Enter a number: '))
	print(' ')
	time.sleep(0.3)
	c = 0
# --------------------
import time

print('Made by Yasas Kulatunga, Dhari Prashanth and Dhivy Prashanth')
print(' ')
number = int(input("Enter a Number: ").strip())
print(' ')
time.sleep(0.5)
print('THINKING.')
time.sleep(0.5)
print('THINKING..')
time.sleep(0.5)
print('THINKING...')
time.sleep(0.5)

print(' ')
while number:
	for i in range(2, number):
		if number % i == 0:
			print('{} is not prime.'.format(number))
			break
	else:
		print('{} is prime!'.format(number))
	number = int(input("Enter a Number: ").strip())
# --------------------
import time
from math import sqrt

print('Made by Yasas Kulatunga, Dhari Prashanth and Dhivy Prashanth')
print(' ')
number = int(input("Enter a Number: ").strip())
maxfact = int(sqrt(number)-1)
print(' ')
time.sleep(0.5)
print('THINKING.')
time.sleep(0.5)
print('THINKING..')
time.sleep(0.5)
print('THINKING...')
time.sleep(0.5)

print(' ')
while number:
	for i in range(2, maxfact):
		if number % i == 0:
			print('{} is not prime.'.format(number))
			break
	else:
		print('{} is prime!'.format(number))
	number = int(input("Enter a Number: ").strip())
	maxfact = int(sqrt(number)-1)
# --------------------

