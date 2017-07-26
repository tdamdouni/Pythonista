import random

guessesTaken = 0
number = random.randint(1, 100)
maxGuesses = 10

name = input('What is your Name? ')

print('Well, ' + Name + ', I am thinking on a number between 1 und 100.')

while guessesTaken < maxGuesses:
	guess = int(input('Guess The numbers: ')
	
	if guess == number:
		print('You guessed it!')
		break
	elif guess < number:
		print('Too low!')
	elif guess > number:
		print('Too high!')
	
	guessesTaken = guessesTaken + 1

if guessesTaken == maxGuesses:
	print('Time es up!')
print('Thanks vor playing!')
