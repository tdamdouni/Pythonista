# coding: utf-8

# https://gist.github.com/Gerzer/370da8cbe0f6066811b5

# https://forum.omz-software.com/topic/2240/ftp-sync

# Pythonista FTP Sync

import ui
import console
import keychain
import ftplib
import os
import re
import time
from datetime import datetime
global cur_dir
cur_dir = os.path.abspath(os.getcwd())
ftp_files = []
def walkftp(ftp_inst, dirname):
	global ftp_files
	ftp_inst.cwd(dirname)
	for name in ftp_inst.nlst(ftp_inst.pwd()):
		path = os.path.join(ftp_inst.pwd(), name)
		try:
			ftp_inst.cwd(path)
			ftp_inst.cwd('..')
			ui.in_background(walkftp(ftp_inst, path))
		except ftplib.error_perm:
			ftp_files.append(path)
def save_handler(sender):
	addr_file = open(os.path.join(cur_dir, 'ftp_addr.txt'), 'w')
	name_file = open(os.path.join(cur_dir, 'ftp_name.txt'), 'w')
	dir_file = open(os.path.join(cur_dir, 'ftp_dir.txt'), 'w')
	root_dir_file = open(os.path.join(cur_dir, 'ftp_rootdir.txt'), 'w')
	addr_file.write(root['addr'].text)
	name_file.write(root['name'].text)
	dir_file.write(root['dir'].text)
	root_dir_file.write(os.path.abspath(root['rootdir'].text))
	addr_file.close()
	name_file.close()
	dir_file.close()
	root_dir_file.close()
	keychain.set_password('ftpsync', root['name'].text, root['pswd'].text)
@ui.in_background
def sync_handler(sender):
	try:
		addr_file = open(os.path.join(cur_dir, 'ftp_addr.txt'), 'r')
		name_file = open(os.path.join(cur_dir, 'ftp_name.txt'), 'r')
		dir_file = open(os.path.join(cur_dir, 'ftp_dir.txt'), 'r')
		root_dir_file = open(os.path.join(cur_dir, 'ftp_rootdir.txt'), 'r')
		addr = addr_file.read()
		name = name_file.read()
		sync_dir = dir_file.read()
		root_dir = root_dir_file.read()
		addr_file.close()
		name_file.close()
		dir_file.close()
		root_dir_file.close()
		pswd = keychain.get_password('ftpsync', name)
	except:
		console.hud_alert('Couldn\'t find a saved FTP host', 'error', 2.3)
		return
	console.show_activity('Syncing with FTP server...')
	os.chdir(root_dir)
	time.sleep(0.35)
#  try:
#    state_file = open('ftp_state.txt', 'r')
#    state = state_file.readlines()
#    state_file.close()
#  except IOError:
#    state_file = open('ftp_state.txt', 'a+')
#    state_file.close()
#    state = []
	if name == '#anonymous#' and pswd == '@anonymous@':
		ftp_inst = ftplib.FTP(addr)
		ftp_inst.login()
	else:
		ftp_inst = ftplib.FTP(addr)
		ftp_inst.login(name, pswd)
	try:
		ftp_inst.nlst(ftp_inst.pwd())
		ftp_inst.set_debuglevel(1)
		walkftp(ftp_inst, sync_dir)
	except:
		pass
	for ftp_file in ftp_files:
		ftp_mod_date = datetime.strptime(ftp_inst.sendcmd('MDTM ' + ftp_file)[4:], "%Y%m%d%H%M%S")
		local_file = ftp_file.replace(sync_dir + '/', '')[1:]
		if os.path.exists(local_file) == True:
			local_mod_date = datetime.fromtimestamp(os.path.getmtime(local_file))
			if ftp_mod_date > local_mod_date:
				ftp_inst.retrbinary('RETR ' + ftp_file, open(local_file, 'wb').write)
			else:
				pass
		else:
			head, tail = os.path.split(local_file)
			if not os.path.exists(head) and head != '':
				os.makedirs(head)
			local_file_obj = open(local_file, 'a+')
			local_file_obj.close()
			ftp_inst.retrbinary('RETR ' + ftp_file, open(local_file, 'wb').write)
	for local_dir, local_dirs, local_filenames in os.walk('.'):
		if local_dir == './.Trash':
			for local_filename in local_filenames:
				local_file = os.path.join(local_dir, local_filename)
				local_file = local_file.replace('./', '')
				ftp_file = '/' + os.path.join(sync_dir, local_file)
				if ftp_file in ftp_files:
					ftp_inst.delete(ftp_file)
			for local_trash_subdir in local_dirs:
				local_full_dir = os.path.join(local_dir, local_trash_subdir)
				local_full_dir = local_full_dir.replace('./', '')
				ftp_dir = '/' + os.path.join(sync_dir, local_full_dir)
				try:
					ftp_inst.rmd(ftp_dir)
				except:
					pass
		else:
			for local_filename in local_filenames:
				local_file = os.path.join(local_dir, local_filename)
				local_file = local_file.replace('./', '')
				ftp_file = '/' + os.path.join(sync_dir, local_file)
				if ftp_file in ftp_files:
					ftp_mod_date = datetime.strptime(ftp_inst.sendcmd('MDTM ' + ftp_file)[4:], "%Y%m%d%H%M%S")
					local_mod_date = datetime.fromtimestamp(os.path.getmtime(local_file))
					if local_mod_date > ftp_mod_date:
						local_file_obj = open(local_file, 'rb')
						head, tail = os.path.split(ftp_file)
						if tail.startswith('.') == False:
							ftp_inst.storbinary('STOR ' + ftp_file, local_file_obj)
						local_file_obj.close()
				else:
					ftp_inst.cwd('/')
					head, tail = os.path.split(ftp_file)
					do_store_file = True
					for dir_level in head.split('/'):
						try:
							ftp_inst.cwd(dir_level)
						except:
							ftp_inst.mkd(dir_level)
							ftp_inst.cwd(dir_level)
					if do_store_file == True:
						local_file_obj = open(local_file, 'rb')
						if tail.startswith('.') == False:
							ftp_inst.storbinary('STOR ' + ftp_file, local_file_obj)
						local_file_obj.close()
	ftp_inst.close()
	console.hide_activity()
def mode_handler(sender):
	if sender.selected_index == 0:
		root['rootdir'].enabled = False
		root['addr'].enabled = False
		root['name'].enabled = False
		root['pswd'].enabled = False
		root['anon'].enabled = False
		root['save'].enabled = False
		root['dir'].enabled = False
		root['sync'].enabled = True
	elif sender.selected_index == 1:
		root['rootdir'].enabled = True
		root['addr'].enabled = True
		if root['anon'].value == False:
			root['name'].enabled = True
			root['pswd'].enabled = True
		root['anon'].enabled = True
		root['save'].enabled = True
		root['dir'].enabled = True
		root['sync'].enabled = False
def anon_handler(sender):
	if sender.value == True:
		root['name'].text = '#anonymous#'
		root['pswd'].text = '@anonymous@'
		root['name'].enabled = False
		root['pswd'].enabled = False
	elif sender.value == False:
		root['name'].text = ''
		root['pswd'].text = ''
		root['name'].enabled = True
		root['pswd'].enabled = True
root = ui.load_view('FTP sync')
try:
	addr_file = open(os.path.join(cur_dir, 'ftp_addr.txt'), 'r')
	name_file = open(os.path.join(cur_dir, 'ftp_name.txt'), 'r')
	dir_file = open(os.path.join(cur_dir, 'ftp_dir.txt'), 'r')
	root_dir_file = open(os.path.join(cur_dir, 'ftp_rootdir.txt'), 'r')
	addr = addr_file.read()
	name = name_file.read()
	sync_dir = dir_file.read()
	root_dir = root_dir_file.read()
	addr_file.close()
	name_file.close()
	dir_file.close()
	root_dir_file.close()
	pswd = keychain.get_password('ftpsync', name)
except:
	addr = ''
	name = ''
	pswd = ''
	root_dir = ''
	sync_dir = ''
root['addr'].enabled = False
root['addr'].text = addr
root['name'].enabled = False
root['name'].text = name
root['pswd'].enabled = False
root['pswd'].text = pswd
root['rootdir'].enabled = False
root['rootdir'].text = root_dir
root['anon'].enabled = False
if name == '#anonymous#' and pswd == '@anonymous@':
	root['anon'].value = True
root['save'].enabled = False
root['dir'].enabled = False
root['dir'].text = sync_dir
root['mode'].action = mode_handler
root.present('sheet')