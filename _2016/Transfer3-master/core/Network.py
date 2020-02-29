#!/usr/bin/env python
#coding: utf-8

from __future__ import print_function
import socket
from contextlib import closing
import threading
import time
import json
import platform
import sys,os
import six

def is_pythonista():
	if 'Pythonista' in sys.executable:
		return True
	else:
		return False

pythonista = is_pythonista()

if pythonista:
	import console
	
class Scanner(object):
	'''start_server()で自分の情報を公開する。scan()で情報をゲットする'''
	def __init__(self, port):
		self.port = port
		self.port_scan = Port_Scan(self.port, show_ip=False, alert=False)
		self.backlog = 10
		self.bufsize = 4096
		self.wait_time = 1
		self.scan_server_exit_flag = False
		self.send_server_exit_flag = False
		
	def scan(self, host_name=None, loop_mode=False, show_text=False):
		ip_list = []
		while True:
			if show_text: print('Detecting Server.....')
			result = self.port_scan.scan()
			if result:
				ip_list = result
				break
			if show_text: print('waiting for {}s'.format(self.wait_time))
			if not loop_mode:break
			time.sleep(self.wait_time)
			
		if len(ip_list) == 0:
			return None
		
		all_dict = {}
		for ip in ip_list:
			info = self.get_info(ip)
			if info:
				info_dict = json.loads(info.decode('utf-8'))
				if host_name and info_dict['host_name'] == host_name:
					return ip
				all_dict[ip] = info_dict
		
		if not host_name:
			return all_dict
		
	def get_info(self, ip):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(1)
		try:
			with closing(sock):
				sock.connect((ip, self.port))
				result = sock.recv(self.bufsize)
				return result
		except socket.timeout:
			pass

				
	def start_server(self, add_dict={'Pythonista':pythonista}):
		thread_list = [ x for x in threading.enumerate() if x.name=='Scanner_Server' ]
		if len(thread_list) == 0:
			threading.Thread(name='Scanner_Server', target=self.server, args=(add_dict,)).start()
		else:
			print('Server has already started')
	
	def stop_server(self):
		self.send_server_exit_flag = True
			
	def server(self, add_dict):
		send_text_dict = {'host_name':socket.gethostname(), 'system':platform.system(), 'platform':platform.platform()}
		send_text_dict.update(add_dict)
		send_text = json.dumps(send_text_dict).encode('utf-8')
		
		#socket.setdefaulttimeout(5)

		while True:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(1)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			try:
				with closing(sock):
					sock.bind(('', self.port))
					
					sock.listen(self.backlog)
					while True:
						
						try:
							conn, address = sock.accept()
						except socket.timeout:
							pass
						else:
							with closing(conn):
								conn.send(send_text)
						
						if self.send_server_exit_flag:
							print('End Send Server')
							self.send_server_exit_flag = False
							return
						time.sleep(1)
				
				
						
						
						
			except Exception as e:
				import traceback
				print(traceback.format_exc())
				time.sleep(1)
					
class Port_Scan(object):
	def __init__(self, port, show_ip=True, alert=True):
		self.port = port
		self.alert = alert
		self.current_ip = self.get_ip()
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
			console.show_activity('Scanning.....')
		for x in range(1,30):#256):
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
			if pythonista:
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
			else:
				#PC
				import subprocess
				try:
					result = subprocess.check_output('ifconfig en0 |grep -w inet', shell=True)
				except:
					try:
						result = subprocess.check_output('ifconfig eth0 |grep -w inet', shell=True)
					except:
						return False
				ip = ''
				if result:
					strs = result.split('\n')
					for line in strs:
						# remove \t, space...
						line = line.strip()
						if line.startswith('inet '):
							a = line.find(' ')
							ipStart = a+1
							ipEnd = line.find(' ', ipStart)
							if a != -1 and ipEnd != -1:
								ip = line[ipStart:ipEnd]
								break
				
					return ip
	
def start_up():
	scanner.start_server({'Pythonista':pythonista})

port = 9999
scanner = Scanner(port)

if __name__ == '__main__':
	args = sys.argv
	if len(args) > 1 and args[1] == '-s':
		start_up()
	else:
		result = scanner.scan()
		assert result, 'Not found'
		for ip, data_dict in six.iteritems(result):
			print('IP {}\n{}'.format(ip, data_dict))
			print(data_dict['host_name'])
