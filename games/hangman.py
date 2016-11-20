#!/usr/bin/env python
# Written by: DGC
# Debugged by KLS

# https://davidcorne.com/2012/06/17/hangman/#more-217
# http://goo.gl/VLx1M

import os
import random
import string
import sys


players = 1
if (len(sys.argv) > 2):
	print("Too many arguments")
	quit()
if (len(sys.argv) == 2):
	if (sys.argv[1] == "-2"):
		players = 2
		
# different set up for 1 or 2 player
word = ""
if (players == 1):
	dictionary = os.path.dirname(str(sys.argv[0])) + "/dictionary.txt"
	if (not os.path.exists(dictionary)):
		print("No dictionary found in %s\n" %(dictionary))
		quit()
	dict_file = open(dictionary)
	lines = dict_file.readlines()
	num = len(lines)
	line_no = random.randrange(num)
	word = str(lines[line_no])
	word = word[:-2]
else:
	# enter word
	word = raw_input("Enter word?\n")
	word = str(word)
	if ("_" in word):
		print("That's Cheating!!!!!!\n")
		quit()
	if (not word):
		print("Don't enter a blank word\n")
		quit()
word = word.upper()

guessed = False
underscores = 52*"_"
trans = string.maketrans(string.ascii_uppercase + string.ascii_lowercase, underscores)
show = word.translate(trans)
lives = 10
guesses = []
# set up men

men = []
for i in range(0,lives+1):
	men.append("")
men[0] += ' _|_________\n'
men[0] += '  | /      |\n'
men[0] += '  |/       O\n'
men[0] += '  |       -+-\n'
men[0] += '  |       / \\\n'
men[0] += '  |\\\n'
men[0] += ' _|_\\________'

men[1] += ' _|_________\n'
men[1] += '  | /      |\n'
men[1] += '  |/       O\n'
men[1] += '  |       -+\n'
men[1] += '  |       / \\\n'
men[1] += '  |\\\n'
men[1] += ' _|_\\________'

men[2] += ' _|_________\n'
men[2] += '  | /      |\n'
men[2] += '  |/       O\n'
men[2] += '  |        |\n'
men[2] += '  |       / \\\n'
men[2] += '  |\\\n'
men[2] += ' _|_\\________'

men[3] += ' _|_________\n'
men[3] += '  | /      |\n'
men[3] += '  |/       O\n'
men[3] += '  |        |\n'
men[3] += '  |       / \n'
men[3] += '  |\\\n'
men[3] += ' _|_\\________'

men[4] += ' _|_________\n'
men[4] += '  | /      |\n'
men[4] += '  |/       O\n'
men[4] += '  |        |\n'
men[4] += '  |\n'
men[4] += '  |\\\n'
men[4] += ' _|_\\________'

men[5] += ' _|_________\n'
men[5] += '  | /\n'
men[5] += '  |/\n'
men[5] += '  |\n'
men[5] += '  |\n'
men[5] += '  |\\\n'
men[5] += ' _|_\\________'

men[6] += ' _|_________\n'
men[6] += '  |\n'
men[6] += '  |\n'
men[6] += '  |\n'
men[6] += '  |\n'
men[6] += '  |\\\n'
men[6] += ' _|_\\________'

men[7] += '  |\n'
men[7] += '  |\n'
men[7] += '  |\n'
men[7] += '  |\n'
men[7] += '  |\n'
men[7] += '  |\\\n'
men[7] += ' _|_\\________'

men[8] += '  |\n'
men[8] += '  |\n'
men[8] += '  |\n'
men[8] += '  |\n'
men[8] += '  |\n'
men[8] += '  |\n'
men[8] += ' _|__________'

men[9] += ' \n'
men[9] += ' \n'
men[9] += ' \n'
men[9] += ' \n'
men[9] += ' \n'
men[9] += ' \n'
men[9] += ' ____________'

men[10] += '\n'
men[10] += '\n'
men[10] += '\n'
men[10] += '\n'
men[10] += '\n'
men[10] += '\n'
men[10] += '             '


message = "Word length is %i, Start guessing" %(len(show))

while (True):
	for i in range(0,100):
		print("")
	message = " " + message + "\n"
	print(message)
	print(men[lives]),
	print("    "),
	show_space = ""
	for char in show:
		if (char == " "):
			char = "/"
		show_space += char
		show_space += " "
	print(show_space),
	guesses.sort()
	if (guesses):
		print("Guesses:"),
		for i in range(0,len(guesses)):
			print(guesses[i]),
	print("\n ")
	if (guessed or lives == 0):
		break
	guess = raw_input()
	guess = str(guess)
	guess = guess.upper()
	if (guess in guesses):
		message = "You've guessed %s before." %(guess)
		message += " Lives remaining: %i" %(lives)
		continue
	if (len(guess) > 1):
		message = "You can only guess one character at a time!!"
		message += " Lives remaining: %i" %(lives)
		continue
	if (not guess):
		message = "Enter a non-blank string."
		message += " Lives remaining: %i" %(lives)
		continue
	# after this it must be a valid guess
	if (not guess in string.ascii_letters):
#    if (ord(guess) < 65 or 122 < ord(guess)):
		message = "Only input nice characters."
		message += " Lives remaining: %i" %(lives)
		continue
	guesses.append(guess)
	if (guess in word):
		message = "Correct!"
		point = ord(guess) - 65
		underscores = underscores[0:point] + guess + underscores[point+1:]
		trans = string.maketrans(string.ascii_uppercase + string.ascii_lowercase, underscores)
		show = word.translate(trans)
		if (not "_" in show):
			guessed = True
	else:
		message = "No."
		lives -= 1
	message += " Lives remaining: %i" %(lives)
	
if (lives > 0):
	print("\n\n Well done! The word was %s\n You finished with %i lives remaining" %(word, lives))
else:
	print("\n\n You are dead! The word was %s" %(word))
print("\n")

