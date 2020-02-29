#!/usr/bin/env python
#coding: utf-8

from __future__ import print_function
import socket
import threading
import console
import os,sys
import paramiko
from stat import S_ISDIR
import time
import objc_util
import ui
import logging

class Port_Scan(object):
	def __init__(self, port, show_ip=True, alert=True):
		self.port = port
		self.alert = alert
		try:
			self.current_ip = self.get_ip()
		except:
			raise Exception('Cannot find IP')
		assert self.current_ip, 'Cannot find IP'
		if show_ip: print('This device IP is {}'.format(self.current_ip))
		self.thread_limit = threading.Semaphore(100)
		
		
	def pscan(self, ip, port):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(1)
			s.connect((ip,port))
			s.close()
		except:
			#print('Port',port,'is close')
			return False
		else:
			if ip == self.current_ip:
				return False
			else:
				self.result.append(ip)
		finally:
			self.thread_limit.release()
			
	def scan(self):
		self.result = []
		_gate_way = '.'.join(self.current_ip.split('.')[:3])
		gate_way = _gate_way+'.1'
		if self.alert:
			console.show_activity('Scanning Port {}'.format(self.port))
		for x in range(1,256):
			ip = '{}.{}'.format(_gate_way, x)
			self.thread_limit.acquire()
			threading.Thread(target=self.pscan, args=(ip, self.port),name='PortScanner').start()
			
		thread_list = [x for x in threading.enumerate() if x.name == 'PortScanner']
		for _ in thread_list:
			_.join()
			
		if self.alert:
			if self.result:
				console.hud_alert(' '.join(self.result), 'success', 1)
			else:
				console.hud_alert('Not found', 'error', 1)
				
			console.hide_activity()
		return self.result
		
	def get_ip(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8",80))
			ip = s.getsockname()[0]
			s.close()
			return ip
		except:
			#offline
			try:
				from objc_util import ObjCClass
				NSHost = ObjCClass('NSHost')
				addresses = []
				for address in NSHost.currentHost().addresses():
					address = str(address)
					if 48 <= ord(address[0]) <= 57 and address != '127.0.0.1':
						addresses.append(address)
				#return '   '.join(addresses)
				return addresses[-1]
				
			except ImportError:
				return ''
					
		
def get_table_list(table):
	new_list1 = []
	new_list = []
	for row in table.selected_rows:
		new_list1.append(table.delegate._items[row[1]])
		
	for _item in table.data_source.items:
		if _item in new_list1:
			new_list.append(_item)
	new_list = remove_repeated_word(new_list)
	_new_list = [x for x in new_list if not x == ".."]
	return _new_list
	
def remove_repeated_word(seq):
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if x not in seen and not seen_add(x)]
	
def to_abs_path(*value):
	import os
	abs_path = os.path.join(os.path.expanduser('~'),'Documents')
	for _value in value:
		abs_path = os.path.join(abs_path,_value)
	return abs_path
	
def to_relpath(path):
	relpath = os.path.relpath(path, to_abs_path())
	return relpath
	
def human_size(size_bytes, no_suffixs=False):
	'''Helper function for formatting human-readable file sizes'''
	if size_bytes == 1:
		return "1 byte"
	suffixes_table = [('bytes',0),('KB',0),('MB',1),('GB',2),('TB',2), ('PB',2)]
	num = float(size_bytes)
	for suffix, precision in suffixes_table:
		if num < 1024.0:
			break
		num /= 1024.0
	if precision == 0:
		formatted_size = "%d" % num
	else:
		formatted_size = str(round(num, ndigits=precision))
	if not no_suffixs:
		return "%s %s" % (formatted_size, suffix)
	else:
		return formatted_size
		
def rmtree(sftp, remotepath, level=0):
	import posixpath,stat
	for f in sftp.listdir_attr(remotepath):
		rpath = posixpath.join(remotepath, f.filename)
		if stat.S_ISDIR(f.st_mode):
			rmtree(sftp, rpath, level=(level + 1))
		else:
			rpath = posixpath.join(remotepath, f.filename)
			#print('removing %s%s' % ('    ' * level, rpath))
			sftp.remove(rpath)
	#print('removing %s%s' % ('    ' * level, remotepath))
	sftp.rmdir(remotepath)


class SSHSession(object):
	def __init__(self,hostname,username='root',key_file=None,password=None):
		self.ssh = ssh = paramiko.SSHClient()  # will create the object
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())# no known_hosts error
		
		if key_file is not None:
			key=open(key_file,'r')
			try:
				pkey=paramiko.RSAKey.from_private_key(key, password=password)
			except paramiko.SSHException as e:
				if e.message == 'not a valid RSA private key file':
					logging.info('color:red not a valid RSA private key file')
					pkey=paramiko.DSSKey.from_private_key(key, password=password)
				else:
					raise e
			
			ssh.connect(hostname, username=username, password=password, pkey=pkey, timeout=5)#key_filename=key_file)
		else:
			if password is not None:
				ssh.connect(hostname, username=username, password=password,timeout=5)
			else: raise Exception('Must supply either key_file or password')
			
		self.sftp = self.ssh.open_sftp()
	
	def close(self):
		self.ssh.close()
		self.sftp.close()
		
	def command(self,cmd):
		stdin,stdout,stderr = self.ssh.exec_command('{}\n'.format(cmd))
	
		for line in stdout:
			logging.info('color:green {}'.format(line))
			
		for line in stderr:
			logging.info('color:red {}'.format(line))
			raise Exception(line)
		
		
	def put(self,localfile,remotefile,sftp_callback=None):
		#  Copy localfile to remotefile, overwriting or creating as needed.
		self.sftp.put(localfile,remotefile,sftp_callback)
		
	def put_all(self,localpath,remotepath,progress=None):
		#  recursively upload a full directory
		os.chdir(os.path.split(localpath)[0])
		parent=os.path.split(localpath)[1]
		for walker in os.walk(parent):
			try:
				self.sftp.mkdir(os.path.join(remotepath,walker[0]))
			except:
				pass
			for file in walker[2]:
				if progress:
					sftp_callback = progress(file, os.path.join(remotepath,walker[0],file), 'put', open_path=os.path.join(localpath,file))
					
				else:
					sftp_callback = None
				self.put(os.path.join(walker[0],file),os.path.join(remotepath,walker[0],file),sftp_callback)
				
	def get(self,remotefile,localfile,sftp_callback=None):
		#  Copy remotefile to localfile, overwriting or creating as needed.
		self.sftp.get(remotefile,localfile,sftp_callback)
		
	def sftp_walk(self,remotepath):
		# Kindof a stripped down  version of os.walk, implemented for
		# sftp.  Tried running it flat without the yields, but it really
		# chokes on big directories.
		path=remotepath
		files=[]
		folders=[]
		for f in self.sftp.listdir_attr(remotepath):
			if S_ISDIR(f.st_mode):
				folders.append(f.filename)
			else:
				files.append(f.filename)
		#print (path,folders,files)
		yield path,folders,files
		for folder in folders:
			new_path=os.path.join(remotepath,folder)
			for x in self.sftp_walk(new_path):
				yield x
				
	def get_all(self,remotepath,localpath, progress=None):
		#  recursively download a full directory
		#  Harder than it sounded at first, since paramiko won't walk
		#
		# For the record, something like this would gennerally be faster:
		# ssh user@host 'tar -cz /source/folder' | tar -xz
		
		self.sftp.chdir(os.path.split(remotepath)[0])
		parent=os.path.split(remotepath)[1]
		try:
			os.mkdir(localpath)
		except:
			pass
		for walker in self.sftp_walk(parent):
			try:
				os.mkdir(os.path.join(localpath,walker[0]))
			except:
				pass
			for file in walker[2]:
				if progress:
					sftp_callback = progress(os.path.join(walker[0],file), file, 'get', open_path=os.path.join(localpath,walker[0],file))
				else:
					sftp_callback = None
				self.get(os.path.join(walker[0],file),os.path.join(localpath,walker[0],file),sftp_callback)
				
	def write_command(self,text,remotefile):
		#  Writes text to remotefile, and makes remotefile executable.
		#  This is perhaps a bit niche, but I was thinking I needed it.
		#  For the record, I was incorrect.
		self.sftp.open(remotefile,'w').write(text)
		self.sftp.chmod(remotefile,755)

def wait_tab_closed(tab_name):
	rootVC = objc_util.UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	
	while True:
		try:
			time.sleep(1)
			
			tab_title_list = [ x.title() for x in tabVC.tabViewControllers()]
			web_count = len([ x for x in tab_title_list if str(x)==tab_name])
			if web_count == 0:
				break
		except KeyboardInterrupt:
			console.hud_alert("When finish editing file, close current tab",'',5)
			
			
class Color_Text_View(ui.View):
	def __init__(self,frame,**value):
		self.auto_scroll=True		
		self.text_view = ui.TextView()
		
		self.text_view.frame = self.frame = frame
		self.text_view.flex = "WHLRTB"
		self.flex = "WHLRTB"
		self.text_view.frame = self.bounds
		self.add_subview(self.text_view)
		
		self.limit = threading.Semaphore(1)
		
		for param in value.keys():
			if param == "auto_scroll":
				self.auto_scroll = value[param]
			if param == "editable":
				self.text_view.editable = value[param]
			if param == "selectable":
				self.text_view.selectable = value[param]
					
		self.all_text = ''
		self.color_data = []
		self.UIColor=objc_util.ObjCClass('UIColor')
		'''for _ in dir(UIColor):
			if len(_)<15 and "Color" in _:
				print _'''
		self.colors={
		'red': objc_util.UIColor.redColor(),
		'green':objc_util.UIColor.greenColor(),
		'blue':objc_util.UIColor.blueColor(),
		'cyan':objc_util.UIColor.cyanColor(),
		'magenta':objc_util.UIColor.magentaColor(),
		'black':objc_util.UIColor.blackColor(),
		'yellow':objc_util.UIColor.yellowColor(),
		'orange':objc_util.UIColor.orangeColor(),
		'purple':objc_util.UIColor.purpleColor(),
		'white':objc_util.UIColor.whiteColor(),
		'blown':objc_util.UIColor.brownColor(),
		'darkgray':objc_util.UIColor.darkGrayColor(),
		'lightgray':objc_util.UIColor.lightGrayColor(),
		'gray':objc_util.UIColor.grayColor()}
		
	@objc_util.on_main_thread
	def setAttribs(self):
		import objc_util
		tv = self.text_view
		tvo=objc_util.ObjCInstance(tv)
		
		tvo.setAllowsEditingTextAttributes_(True)
		tvo.setAttributedText_(self.str_object)
		if self.auto_scroll:
			tvo.scrollRangeToVisible_((len(self.all_text), 0))

	def write(self, text):
		'''logging.info('color:red Text')'''
		import threading
		def _write():
			self.add_text(str(time_info), 'black',False)
			self.add_text(str(text_body), Color,True)
			
		Color = 'orange'
		text = text.strip()
		time_info = ' '.join(text.split()[:2])+' '
		#self.add_text(str(time_info), 'black',False)
		#threading.Thread(target=self.add_text, args=(str(time_info), 'black',False)).start()
		
		text = ' '.join(text.split()[2:])
		if text.find('color:') == 0:
			text = text.replace('color:','')
			Color = text.split()[0]
			text = ' '.join(text.split()[1:])
			
			text_body = text
		else:
			text_body = text
		
		threading.Thread(target=_write).start()
		#self.add_text(str(text_body), Color,True)
		
	def flush(self):
		pass
	
	def add_text(self,text,color='black',new_line=True):
		import objc_util
		import traceback
		self.limit.acquire()
		try:
			text = unicode(text)
			self.all_text += text+"\n" if new_line else text
			self.str_object=objc_util.ObjCClass('NSMutableAttributedString').alloc().initWithString_(self.all_text)
			
			if self.colors.has_key(color):
				range = len(text)+1 if new_line else len(text)
				start = len(self.all_text)-range
				color_obj = self.colors[color]
				self.color_data.append((color_obj,start,range))
				
			for color_obj,start,range in self.color_data:
				self.str_object.addAttribute_value_range_('NSColor',color_obj,objc_util.NSRange(start,range))
				
			
			self.setAttribs()
		except :
			print('{}のテキスト処理に失敗'.format(text))
			print(traceback.format_exc())
		finally:
			self.limit.release()
		
def stash_installer():
	try:
		from stash.stash import StaSh
	except:
		console.show_activity('Installing stash.....')
		import requests
		exec(requests.get('http://bit.ly/get-stash').text,globals(), locals())
		console.hide_activity()
	finally:
		from stash.stash import StaSh
		ssh_path = to_abs_path('site-packages', 'stash', '.ssh')
		if not os.path.isdir(ssh_path):
			os.makedirs(ssh_path)
			
