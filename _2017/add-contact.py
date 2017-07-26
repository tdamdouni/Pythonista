# https://gist.github.com/daveaiello/1f338fae359148d755d6a58dfb170258

# https://forum.omz-software.com/topic/3965/add-an-address-to-a-contact/2

import contacts
import clipboard

name = clipboard.get().split('|')
pers = contacts.Person()
pers.organization = bytes(name[0], encoding='UTF-8')
pers.address = [(contacts.WORK,
				{contacts.STREET: name[1],
					contacts.CITY: name[2],
					contacts.STATE: name[3],
					contacts.ZIP: name[4],
					contacts.COUNTRY: name[5]})]
pers.phone = [(contacts.MAIN_PHONE, name[6])]
if len(name) == 8:
	pers.url = [(contacts.WORK, name[7])]
contacts.add_person(pers)
contacts.save()
