from __future__ import print_function
# https://gist.github.com/omz/48e80b0223d1eaf37025
# coding: utf-8

# Starting point for emailing a group of people via Dispatch...
# The people in the group are identified by a unique string in the Notes field.

# TODO: Support setting the group identifier with an argument when launching the script via URL scheme (LCP...) - subject, body etc. could also be passed as arguments.

# Change this:
group_note = 'Group1'


import contacts
import webbrowser

addresses = []
people = contacts.get_all_people()
for person in people:
	if person.note and group_note in person.note:
		emails = person.email
		if emails:
			#Note: always uses the first email, could be changed to use a given label...
			addresses.append(emails[0][1])

# c.f. https://gist.github.com/CleanShavenApps/8206141
dispatch_url = 'x-dispatch:///compose?to=%s' % (','.join(addresses))
opened = webbrowser.open(dispatch_url)
if not opened:
	print('Could not open URL:', dispatch_url)