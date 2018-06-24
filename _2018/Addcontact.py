# https://gist.github.com/my4paws/ae7dc32ba9937996d4d13848ab13404c

# https://forum.omz-software.com/topic/4821/add-contact-to-a-group

import contacts
import clipboard
import webbrowser
import dateutil
name = clipboard.get().split(',')
pers = contacts.Person()
grp = contacts.Group()
pers.first_name = name[0]
pers.last_name = name[1]
pers.middle_name = name[2]
pers.prefix = name[3]
pers.job_title = name[4]
pers.department = name[5]
pers.email = [(contacts.HOME, name[6])]
pers.address = [(contacts.HOME,
				{contacts.STREET: name[7],
					contacts.CITY: name[8],
					contacts.STATE: name[9],
					contacts.ZIP: name[10],
					contacts.COUNTRY: name[11]})]
pers.nickname = name[13]
pers.organization = name[14]
pers.phone = [(contacts.HOME, name[15]),(contacts.IPHONE, name[16]),(contacts.WORK, name[17])]
from dateutil import parser
string_date = parser.parse(name[18])
pers.birthday = string_date
pers.url = [(contacts.HOMEPAGE, name[19])]

#here name[20] would provide the name of the group I want the contact to be added to

contacts.add_person(pers)
contacts.save()
webbrowser.open('workflow://')