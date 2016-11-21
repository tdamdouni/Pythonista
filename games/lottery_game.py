# coding: utf-8

# https://github.com/philipkalinda

# # lottery_game :This is a lottery game! you bet any amount from £1-100 and pick 5 numbers between 1 and 20 and see if you win! good luck! the values can be changed in the #GameSettings within the code.

#### Lottery Game ####

import random
import os
import sys
import time
import math

# - Game Settings

minimum_bet = 0
maximum_bet = 101
min_num_range = 0
max_num_range = 21
number_of_choices = 5
numbers_generated = []

def choose_numbers(initial_bet_amount):
	choices = 0
	choices_list = []
	numbers = 5
	numbers_generated = []
#random numbers generated unique
	while numbers>0:
		new_number = random.randint((min_num_range)+1,(max_num_range)-1)
		if new_number in numbers_generated:
			continue
		elif new_number not in numbers_generated:
			numbers_generated.append(new_number)
			numbers -= 1
#number choices
	matched_numbers = 0
	not_matched = 0
	print('''
********************
Now it's time to choose those lucky numbers!
You are allowed to pick any number between {} and {}.'''.format((min_num_range)+1,(max_num_range)-1))
	while choices < number_of_choices:
		print('''
You have {} choices left! Choose wisely!'''.format(int(number_of_choices - choices)))
		print('''So far you have chosen the following:''')
		print(choices_list)
		choice = input('''
********************
Choose a number between {} and {}.
> '''.format((min_num_range)+1,(max_num_range)-1))
		try:
			if int(choice) in choices_list:
				print('''
********************
You have already chosen that number! pick another number!
''')
			elif int(choice) <= min_num_range:
				print('''
********************
That number is too low! you need to pick a number between {} and {}'''.format(min_num_range,max_num_range))
			elif int(choice) >= max_num_range:
				print('''
********************
That number is too high! you need to pick a number between {} and {}'''.format(min_num_range,max_num_range))
			elif int(choice) <= max_num_range and int(choice) >= min_num_range and choice not in choices_list:
				choices_list.append(int(choice))
				choices += 1
		except ValueError:
			print('''
********************
That\'s not a valid entry! please enter a numerical value between {} and {}'''.format(min_num_range,max_num_range))
	print('''
********************
You have chosen the following numbers!
GOOD LUCK!!
''')
	print(choices_list)
	confirming=True
	while confirming==True:
		confirm_choices = (input('''
********************
Are you sure you would like to pick the following numbers?
{} y/n
> '''.format(choices_list))).upper()
		if confirm_choices == 'Y':
			
			print('Time to see the numbers!')
			print('Here are your choices: ')
			print(choices_list)
			print('''The first number is
...''')
			time.sleep(2)
			print(numbers_generated[0])
			time.sleep(1)
			print('''The second number is
...''')
			time.sleep(2)
			print(numbers_generated[1])
			time.sleep(1)
			print('''The third number is
...''')
			time.sleep(2)
			print(numbers_generated[2])
			time.sleep(1)
			print('''The forth number is
...''')
			time.sleep(2)
			print(numbers_generated[3])
			time.sleep(1)
			print('''The fifth number is
...''')
			time.sleep(2)
			print(numbers_generated[4])
			time.sleep(1)
			print('''
********************
''')
			print('Here are all the winning numbers!')
			print(numbers_generated)
			print('')
			print('Here are the numbers you chose!')
			print(choices_list)
			print('''
********************
''')
			print('Calculating....')
			time.sleep(5)

			print('''
********************
''')
			for i in choices_list:
				if i in numbers_generated:
					matched_numbers += 1
				elif i not in numbers_generated:
					not_matched += 1

			print('You managed to guess {} out of {}'.format(matched_numbers,number_of_choices))
			print('')
			print('You couldn\'t match {} out of {}'.format(not_matched,number_of_choices))
			print('')
			
			amount_won = int((matched_numbers * initial_bet_amount) * math.exp(matched_numbers+1))
			
			print('You win £{}'.format(amount_won))

			while True:
				playing_again = (input('''Would you like to play again? y/n 
> ''')).upper()
				if playing_again == 'Y':
					intro_game()
				elif playing_again == 'N':
					print('''********************
Hope you enjoyed!
Come back soon!''')
					quit()
				else:
					print('That\'s an invalid entry! please enter \'y\' or \'n\' ')

			confirm=False
			break
		elif confirm_choices == 'N':
			print('''
********************
Ok, let's try pick some different numbers!
Here are the rules:
''')
			choose_numbers(initial_bet_amount)
			confirm=False
			break
		else:
			print('''
********************
That\'s an invlaid entry!
Please enter \'y\' or \'n\' 
''')
			confirm=True

def confirmation(initial_bet_amount):
	confirm=True
	while confirm==True:
		confirm_initial = (input('''
********************
Are you sure you would like to bet £{}? y/n
> '''.format(initial_bet_amount))).upper()
		if confirm_initial == 'Y':
			choose_numbers(initial_bet_amount)
			confirm=False
			break
		elif confirm_initial == 'N':
			print('''
********************
Ok, let's try bet again!
Here are the rules:
''')
			place_bet()
			confirm=False
			break
		else:
			print('''
********************
That\'s an invlaid entry!
Please enter \'y\' or \'n\' 
''')
			confirm=True

def place_bet():
	print('''
********************
Now is the time to set your bet!
There is a minimum bet of £{}.
There is a maximum bet of £{}.
Good luck!
'''.format(minimum_bet,maximum_bet))
	while True:
		initial_bet_amount = input('''
How much money would you like to bet?
> £''')
		try:
			if int(initial_bet_amount) < minimum_bet:
				print('''
********************
That bet is too low! please enter a number between £{} and £{}'''.format(minimum_bet,maximum_bet))
			elif int(initial_bet_amount) > maximum_bet:
				print('''
********************
That bet is too high! please enter a number between £{} and £{}'''.format(minimum_bet,maximum_bet))
			elif int(initial_bet_amount) < maximum_bet and int(initial_bet_amount) > minimum_bet:
				initial_bet_amount = int(initial_bet_amount)
				confirmation(initial_bet_amount)
				return initial_bet_amount
				break
		except ValueError:
			print('''
********************
That\'s not a valid entry! please enter a numerical value between £{} and £{}'''.format(minimum_bet,maximum_bet))
			continue

def intro_game():
	print('''
********************
Welcome to the lottery game! 
I hope you enjoy the game!

********************
Created by PhilipKalinda

********************
Instructions:
1. Choose the amount of money you would like to bet!
2. Then choose your 5 luckiest numbers!
3. Play to see if you win any money
''')
	start_game()

def start_game():
	ready_to_play = True
	while True:
		ready_to_play = (input('''
********************
Are you ready to play? y/n
> ''')).upper()
		if ready_to_play == 'Y':
			place_bet()
			break
		elif ready_to_play == 'N':
			print('''
********************
Come back to play soon!
Bye!
********************
''')
			quit()
		else:
			print('''
********************
That\'s not a valid entry!
Please enter \'y\' for yes or \'n\' for no
''')

intro_game()



