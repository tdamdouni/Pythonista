# https://forum.omz-software.com/topic/3745/successive-ftp-sessions/3

import ftplib
F1=ftplib.FTP('ftp.FreeBSD.org',user='ftp')
F2=ftplib.FTP('ftp.FreeBSD.org',user='ftp')
print(F1.sendcmd('CWD pub'))
print('f1 dir')
F1.dir()
print('f2 dir')
F2.dir()

# https://forum.omz-software.com/topic/3745/successive-ftp-sessions/5

import keychain
from ftplib import FTP
import time
import console
def test_successive_ftp():
	console.hud_alert('mac')
	user = 'Xxxxx'
	pwd = keychain.get_password('FTPiMac',user)
	try:
		FTP  = FTP('iMac.local') #connect
		FTP.encoding = 'utf-8'
		FTP.login(user,pwd)
		print('mac')
		print(list(FTP.mlsd('Google Drive/Budget')))
		FTP.quit()
		del FTP
	except:
		console.alert('Mac not accessible','','ok',hide_cancel_button=True)
		
	console.hud_alert('adrive')
	user = 'xxxxxx'
	pwd = keychain.get_password('ADrive',user)
	try:
		FTP = FTP('ftp.adrive.com') #connect
		FTP.encoding = 'utf-8'
		FTP.login(user,pwd)
		print('adrive')
		print(list(FTP.mlsd('Google Drive/Budget')))
		FTP.quit()
		del FTP
	except:
		console.alert('ADrive not accessible','','ok',hide_cancel_button=True)
		
test_successive_ftp()

