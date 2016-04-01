# coding: utf-8

# https://forum.omz-software.com/topic/2496/add-email-to-contacts

import contacts

people = contacts.get_all_people()
print people[0].full_name

emails = people[0].email
emails.append((u'$!<Other>!$', u'test@test.com'))
people[0].email = emails # !!!

contacts.save()