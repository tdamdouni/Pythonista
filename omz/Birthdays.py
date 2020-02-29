'''Prints a list of birthdays in your address book (in days from now).

NOTE: This script requires access to your contacts in order to work properly.'''
from __future__ import print_function

import contacts
import dialogs
from datetime import datetime
import operator

def main():
	days_list = []
	people = contacts.get_all_people()
	now = datetime.now()
	for p in people:
		b = p.birthday
		if not b:
			continue
		next_birthday = datetime(now.year, b.month, b.day)
		if next_birthday < now:
			next_birthday = datetime(now.year + 1, b.month, b.day)
		days = (next_birthday - now).days
		days_list.append({'name': p.first_name, 'days': days})
	if not days_list:
		print('You don\'t have any birthdays in your address book.')
	else:
		days_list.sort(key=operator.itemgetter('days'))
		print('Upcoming Birthdays\n' + '=' * 40)
		for item in days_list:
			print('* %s in %i days' % (item['name'], item['days']))

if __name__ == '__main__':
	main()