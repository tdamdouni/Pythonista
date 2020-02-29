# coding: utf-8

# https://gist.github.com/mlgill/8310754

from __future__ import print_function
import keychain

def set_get_user_pass(service):
	
	# store username and password in keychain if not found
	if not service in [x[0] for x in keychain.get_services()]:
		print('Keychain does not contain %s username and password.' % service)
		username = raw_input('Enter your %s username and press enter:' % service)
		password = raw_input('Enter your %s password and press enter:' % service)
		print('Username %s and password saved for %s.' % (username, service))
		keychain.set_password(service, username, password)
		
	else:
		# get the username---can be multiple accounts for one service
		usernamelist = [x[1] for x in keychain.get_services() if x[0]==service]
		
		if len(usernamelist) > 1:
			print('Multiple usernames were found for %s.' % service)
			for uname in enumerate(usernamelist):
				print('     [%d]: %s'%(uname[0]+1, uname[1]))
			unum = int(raw_input('Enter the number of the correct one:').strip()) - 1
			username = usernamelist[unum]
		else:
			username = usernamelist[0]
			
		# get the password based on correct username
		password = keychain.get_password(service, username)
	
	return username, password