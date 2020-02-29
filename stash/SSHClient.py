from __future__ import print_function
# Very simple SSH client for Pythonista
import paramiko
import console

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
host = console.input_alert('Connect to')
user, passwd = console.login_alert('Login')
ssh.connect(host, username=user, password=passwd)
print('Connected to %s. Type `exit` to disconnect.' % host)
while True:
	cmd = raw_input()
	if cmd == 'exit':
		break
	stdin, stdout, stderr = ssh.exec_command(cmd)
	print(stdout.read())
ssh.close()
print('Disconnected.')

