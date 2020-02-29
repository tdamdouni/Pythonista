# coding: utf-8

# https://gist.github.com/lukaskollmer/52a20e8d6447b1fe6033f95386405c27

from __future__ import print_function
import contacts
import ui
from datetime import datetime
import operator
import console

console.clear()

if not contacts.is_authorized():
	print('You need to allow acces to contacts to use this application')

	


def load_upcoming_birthdays(pretty_output=True, leading_zeros=False):
	
	all_contacts = contacts.get_all_people()
	all_birthdays = []
	all_output = []
	number_of_contacts_without_birthday = 0
	now = datetime.now()
	
	for person in all_contacts:
		if person.kind == 0: #0: Person, 1: company
			if person.birthday:
				birthday = person.birthday
				next_birthday = datetime(now.year, birthday.month, birthday.day)
				if next_birthday < now:
					next_birthday = datetime(now.year + 1, birthday.month, birthday.day)
				number_of_days_to_next_birthday = (next_birthday - now).days
				all_birthdays.append({'first_name': person.first_name, 'last_name': person.last_name, 'days': number_of_days_to_next_birthday, 'date': birthday})
			else: # no birthday set
				number_of_contacts_without_birthday += 1
	
	
	all_birthdays.sort(key=operator.itemgetter('days'))
	
	
	# add the first part (* 012 days to Renate)
	for birthday in all_birthdays:
		if pretty_output:
			if leading_zeros:
				days_formatted = '%.3i' % birthday['days'] # old format (leading 0s)
			else:
				days_as_string = '{0}'.format(birthday['days'])
				days_formatted = ' '*(3-len(days_as_string)) + '{0}'.format(birthday['days'])
		else:
			days_formatted = '{0}'.format(birthday['days'])
		
		days_text_string = ''
		if not birthday['days'] == 1:
			days_text_string = 'days'
		else:
			days_text_string = 'day '
		output = '* {0} {1} to {2}'.format(days_formatted, days_text_string, birthday['first_name'])
		all_output.append(output)
	
	
	
	length_first_name = 0
	for output_string in all_output:
		first_name = output_string.split()[4]
		if len(first_name) > length_first_name:
			length_first_name = len(first_name)
	
	
	
	
	# add the second part (Altinger)
	for birthday in all_birthdays:
		index = all_birthdays.index(birthday)
		_length_shorter = length_first_name+1 - len(birthday['first_name'])
		new_output = ''
		if pretty_output:
			new_output = all_output[index] + ' '* _length_shorter + birthday['last_name']
		else:
			new_output = all_output[index] + ' ' + birthday['last_name']
		all_output[index] = new_output
	
	
	
	#
	# add the birthdate at the end
	#
	length_last_name = 0
	for output_string in all_output:
		last_name = output_string.split()[5]
		if len(last_name) > length_last_name:
			length_last_name = len(last_name)
	
	
	
	
	# add the date
	for birthday in all_birthdays:
		index = all_birthdays.index(birthday)
		_length_shorter = length_last_name+1 - len(birthday['last_name'])
		actual_birthday = birthday['date']
		date_format = ''
		trailing_text = ''
		if actual_birthday.year < 1900:
			actual_birthday = actual_birthday.replace(2015)
			date_format = '%d. %b'
			trailing_text = '    *'
		else:
			date_format = '%d. %b %y'
			trailing_text = ' *'
		new_output = ''
		if pretty_output:
			new_output = all_output[index] + ' '* _length_shorter + '({0}){1}'.format(actual_birthday.strftime(date_format), trailing_text)
		else:
			new_output = all_output[index] + ' ' + '({0}){1}'.format(actual_birthday.strftime(date_format), trailing_text)
		all_output[index] = new_output
	
	
	
	longest_row = 0
	for output in all_output:
		output_length = len(output)
		if output_length > longest_row:
			longest_row = output_length
	
	
	
	
	console.clear()
	
	print('Next Birthdays from your Address Book')
	print('='*longest_row)
	
	
	for output in all_output:
		print(output)
	
	#print '='*longest_row
	
	print()
	print('{0} of {1} contacts have no birthday set'.format(number_of_contacts_without_birthday, len(all_contacts)))


load_upcoming_birthdays()
