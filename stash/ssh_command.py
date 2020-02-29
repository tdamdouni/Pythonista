# coding: utf-8

# https://gist.github.com/Moving-Electrons/e7dcb5f0659c2c661c0f

# This script connects through SSH to the Computer/Server using the Username & Password defined in the header. It then runs a command/script that is passed as an argument by long pressing the Run icon in Pythonista or by calling the script through Pythonista's URL scheme with an argument. More information in www.movingelectrons.net , scripting sec…

from __future__ import print_function
import paramiko
import console
import sys
import keychain

'''This script connects through SSH to the Computer/Server using the Username & Password defined in the header.
It then runs a command/script that is passed as an argument by long pressing the Run icon in Pythonista or by
calling the script through Pythonista's URL scheme with an argument.

General Notes:
- The keychain module is used to save the username's password so it's not out in the open.
- All sections in CAPS are meant to be revised according to each user's specific information.

'''

#Constants
print('Configuring parameters...')
strComputer = 'YOUR COMPUTER IP'
strUser = 'REMOTE COMPUTER USERNAME'
strPwd = keychain.get_password('KEYCHAIN ACCOUNT','KEYCHAIN USERNAME') # assign '' if you want the password to be entered via console input
print('Parameters configured.')

print('Verifying parameters...')
if not strComputer:
	strComputer = raw_input('Enter computer name/IP address:')
if not strUser:
	strUser = raw_input('Enter user name:')
if not strPwd:
	strPwd = console.secure_input('Enter password:')
	
try:
	strCommand = sys.argv[1] #checks if the command was entered as an argument. if it was not, asks for it.
except:
	strCommand = raw_input('Enter command:')
print('Parameters verified.')

# Initialize connection
print('Initiating SSH connection...')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=strComputer, username=strUser, password=strPwd)
print('SSH connection established with ' + strComputer + ' as user ' + strUser + '.')

print('Executing command [' + strCommand + ']...')
stdin, stdout, stderr = client.exec_command(strCommand)
print(stdout.read())
print('Command execution complete.')

#Close the connection
print('Closing SSH connection...')
client.close()
print('SSH connection closed.')

