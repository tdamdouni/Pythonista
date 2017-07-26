#!/usr/bin/env python3

# https://forum.omz-software.com/topic/3871/could-not-convert-string-to-float

prompt = 'Enter income, if no more income press enter: '
total = 0  # avoid using the word 'sum' because sum() is a Python builtin function
while True:
	income = input(prompt).strip()
	if not income:
		break
	total += float(income)
print('Your total income is: ${:,.2f}'.format(total))

