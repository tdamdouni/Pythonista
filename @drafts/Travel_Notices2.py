import console
import sys
import webbrowser
import urllib

base = "launchpro-messaging://"
to = "?to="
xcb = 'x-callback-url/'
body = "&body="
success = '&x-success='

def get_location():
    import location
    console.show_activity()
    location.start_updates()
    ldata = location.get_location()
    city = location.reverse_geocode(ldata)[0].get('City')
    return city

INPUT_STRING = sys.argv[-1]

if INPUT_STRING == 'landed':
    cityname = get_location()
    land_location = console.input_alert("Location", "Where did you just land?", cityname)

contacts = [
     {
        'address': 'person1@gmail.com',
        'landed': 'Hi, Mom. Just landed in ',
        'boarding': 'Boarding now!',
        'shuttingdown': 'Shutting down. I\'ll text when I land.'
     },
     {
        'address': '+1 555 867 5309',
        'landed': 'Hi, John. Just landed in ',
        'boarding': 'Boarding now.',
        'shuttingdown': 'Shutting down. See you soon!'
     },
]
    
def quote(s, count=1):
    for i in range(count):
        s = urllib.quote(s, safe='') 
    return s

def get_message(contact):
    if INPUT_STRING == 'landed':
        return quote(contact.get('landed', '') + land_location + '!')
    else:
        return quote(contact.get(INPUT_STRING, console.input_alert("Message", "Enter a message.")))


first_contact = contacts.pop(0)

final_action = base + xcb + to + quote(first_contact['address']) + body + get_message(first_contact) + success

actions_list = [final_action]
for index, contact in enumerate(contacts):
    if len(contacts) == (index + 1):
        actions = base + to + contact['address'] + body + get_message(contact)
    else:
        actions = base + xcb + to + contact['email'] + body + get_message(contact) + success
    actions_list.append(actions)

for i in range(len(actions_list)):
    actions_list[i] = quote(actions_list[i], i)

webbrowser.open("".join(actions_list))


