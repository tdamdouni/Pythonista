# https://forum.omz-software.com/topic/3633/feature-request-password-to-lock-pythonista-app-for-parental-control

from passlib.hash import pbkdf2_sha256
import dialogs
import os

file = './.passwd'

if not os.path.isfile(file):
	p1 = None
	p2 = 'password'
	
	while p1 != p2:
		p1 = dialogs.password_alert('Create a password:\nPleaes enter your password', hide_cancel_button=True)
		
		if len(p1) == 0:
			dialogs.hud_alert('Password can\'t be empty!')
			continue
		p2 = dialogs.password_alert('Pleaes enter your password again to confirm', hide_cancel_button=True)
		
		if p1 != p2:
			dialogs.hud_alert('The password you entered does not match. Try again')
			
	hash = pbkdf2_sha256.encrypt(p1, rounds=200000, salt_size=16)
	
	with open(file, 'w+') as F:
		F.write(hash)
		
	if os.path.isfile(file) and os.path.getsize(file) > 0:
		dialogs.hud_alert('Your password has been saved successfully!')
	else:
		dialogs.hud_alert('Error! Password has not been saved!')
else:
	p1 = None
	trial = 0
	success = False
	
	while not success:
		p1 = dialogs.password_alert('Pleaes enter your password', hide_cancel_button=True)
		with open(file, 'r') as F:
			hash = F.read()
		success = pbkdf2_sha256.verify(p1, hash)
		if success:
			dialogs.hud_alert('Login Success!')
		else:
			dialogs.hud_alert('Login Failed! Try again!')
			trial += 1

