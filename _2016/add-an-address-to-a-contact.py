# https://forum.omz-software.com/topic/3965/add-an-address-to-a-contact

import contacts
import clipboard
import webbrowser

name = clipboard.get().split(',')
pers = contacts.Person()
pers.first_name = name[0]
pers.last_name = name[1]
contacts.add_person(pers)
contacts.save()
webbrowser.open('workflow://')
# --------------------
import contacts
import clipboard
import webbrowser

name = clipboard.get().split('|')
pers = contacts.Person()
pers.organization = bytes(name[0], encoding='UTF-8')
# --------------------
import contacts

person = contacts.Person()
person.address = [(contacts.WORK,
    {contacts.STREET: 'Infinite Loop 1',
     contacts.CITY: 'Cupertino'})
]
person.url = [(contacts.WORK, 'http://apple.com')]
contacts.add_person(person)
contacts.save()
# --------------------
# Person.url and Person.address are slightly more complicated than Person.organization because you can have multiple addresses and URLs for each person. Each value in the list of addresses is a tuple with a label (contacts.WORK) and the actual address (a dictionary with the keys contacts.STREET, contacts.CITY etc.).
