import keychain
import console

get_or_set = console.alert('Get or set?','','Get','Set')

if get_or_set == 1:
	 service = console.input_alert('Service to get?')
	 user = console.input_alert('What user?')
	 mypass = keychain.get_password(service, user)
	 if mypass == None:
	 	console.alert('Couldn\'t find that one.')
	 else:
	 	copy_here = console.alert('Print, clipboard, or console?','','Print','Clipboard','Console')
	 	if copy_here == 1:
	 		console.clear()
	 		print(mypass)
	 	elif copy_here == 2:
	 		import clipboard
	 		clipboard.set(mypass)
	 	elif copy_here == 3:
	 		console.alert(mypass)
	 		
elif get_or_set == 2:
	service = console.input_alert('Service name to store')
	user = console.input_alert('Username to store')
	mypass = console.input_alert('Password to store')
	keychain.set_password(service, user, mypass)
	console.alert('All done.')
