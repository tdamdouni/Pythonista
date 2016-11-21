# coding: utf-8

# https://github.com/philipkalinda

# This is the times table game where you get to practise your times table! whether you want to practise you 5 x 12 times table or even your 89 x 25 times table, this game will allow you to do so and provide feedback as to which questions you should work on.

### Times Table Game ###

import time, random, math

print('''********************
Welcome To The Times Table Game!

Time To Test Your Knowledge Mathmematicians!
''')

multiplyee = 12

verify = 0
while verify==0:
	base_multiplier = input('''Which times table would you like to do? 
> ''')
	try:
		int(base_multiplier)
		base_multiplier = int(base_multiplier)
		verify += 1
	except ValueError:
		print('''********************
That\'s not a valid entry! Please enter a number
''')
		continue

verification = 0
while verification==0:
	multiplyee = input('''********************
How far would you like to do your times table? (The default is 12)
> ''')
	try:
		if multiplyee == '':
			multiplyee = 12
			int(multiplyee)
			verification += 1
		else:
			int(multiplyee)
			multiplyee = int(multiplyee)
			verification += 1
	except ValueError:
		print('''********************
That\'s not a valid entry! Please enter a number
''')
		continue

questions = []
answers = []

number_of_answers = multiplyee
number_of_questions = multiplyee

asked = 0
questions_asked = []


starting = 0
while starting == 0:
	start = input('''********************
You have chosen to do your {} times table!
With {} iterations!

Are you ready to start? 
Enter y/n
> '''.format(base_multiplier,multiplyee))
	if start.lower() == 'y':
		starting += 1
	elif start.lower() == 'n':
		print('''********************
Come back and play again soon!
''')
		quit()
	else:
		print('''********************
That\'s not a valid entry! 
Please enter \'y\' or \'n\'''')

#populate questions
while multiplyee > 0:
	add_question = '{} X {}'.format(multiplyee,base_multiplier)
	questions.append(add_question)
	multiplyee -= 1

#populate answers
while number_of_answers > 0:
	add_answer = number_of_answers*base_multiplier
	answers.append(add_answer)
	number_of_answers -= 1

start_time = time.time()
count = 1
correct_answers = 0
incorrect_answers = 0
answered_wrong = []
answered_correctly = []

#Countdown to gameplay
print('Loading...')
time.sleep(3)
countdown = 3
print('Game will begin in...')
time.sleep(1)
while countdown > 0:
	print(countdown)
	time.sleep(1)
	countdown -= 1

while asked < number_of_questions:
	question = random.choice(questions)
	if question in questions_asked:
		continue
	elif question not in questions_asked:
		answer_is_number = 0
		while answer_is_number == 0:
			answer = input('''********************
Question {}:
What is {} ?
> '''.format(count, question))
			try:
				int(answer)
				answer = int(answer)
				answer_is_number += 1
				asked += 1
			except ValueError:
				print('''********************
		That\'s not a valid entry! Please enter an integer
		''')
				continue
		if answer == answers[(questions.index(question))]:
			correct_answers += 1
			count += 1
			answered_correctly.append(question)
		elif answer != answers[(questions.index(question))]:
			incorrect_answers += 1
			count += 1
			answered_wrong.append(question)
		questions_asked.append(question)

elapsed_time = int(time.time() - start_time)

elapsed_time_minutes = int(elapsed_time/60)
elapsed_time_seconds = int(elapsed_time%60)

percentage = (correct_answers) / (correct_answers + incorrect_answers)
percentage = int(percentage * 100)

print('''********************
Well Done! You have completed the Times Table Game!
''')
print('''Loading Stats...
''')

time.sleep(3)

print('''********************
Your Stats
Percentage: {}%

Correct Answers: {} out of {}
Incorrect Answers: {} out of {}
Time Taken: {} Minutes {} Seconds
'''.format(percentage,correct_answers,number_of_questions,incorrect_answers,number_of_questions,elapsed_time_minutes,elapsed_time_seconds))


if len(answered_wrong) == 0:
	print('''Well Done! You got them all right!''')
	print('Come back and play soon!')

elif len(answered_wrong) != 0:
	print('''
Here are the questions that you answered incorrectly:''')
	wrong_counter = 1
	for each_wrong in answered_wrong:
		print('{}. {}'.format(wrong_counter, each_wrong))
		wrong_counter += 1
	print('You should probably work on these questions')
	print('Come back and play soon!')

