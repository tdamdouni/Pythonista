#!/usr/bin/env python
#coding: utf-8

# https://github.com/nekotaroneko/Transfer3

'''
Trasnfer files by https.
This program may be diffucult to read due to its difficulties and my coding ability sorry!!

***This program is beta.
if there is an error, please restart pythonista

Todo
Support windows by pyqt
More stable
'''
from __future__ import print_function

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading, shutil
import requests
import json
import Queue
from core.Network import Scanner, Port_Scan
from core.other import get_file_list, file_picker, human_size
import ssl
import six
import traceback
import socket
import time
import sys,os
import datetime

password = 'ryo'

def is_pythonista():
	if 'Pythonista' in sys.executable:
		return True
	else:
		return False

pythonista = is_pythonista()

if pythonista:
	import speech
	import console
	import ui
	import clipboard

def to_abs_path(*value):
	import os
	abs_path = os.path.join(os.path.expanduser('~'),'Documents')
	for _value in value:
		abs_path = os.path.join(abs_path,_value)
	return abs_path
	

class Transfer3(ui.View):
	def __init__(self, view):
		self.connect_limit = 5
		
		d = datetime.datetime.today()
		folder = d.strftime("%Y-%m-%d")
		self.save_dir = to_abs_path('Transfer3', folder)
		#print folder
		if not os.path.isdir(self.save_dir):
			os.makedirs(self.save_dir)
		
		self.app_root_path = os.path.dirname(__file__)
		self.core_path = os.path.join(self.app_root_path, 'core')
		self.cert_path = os.path.join(self.app_root_path, 'server.pem')
	
	
		self.view = view
		self.sc_select = self.view['sc_select']
		self.sc_select.action = self.sc_select_action
		
		self.send_view = self.view['send_view']
		self.tv_receiver = self.view['send_view']['tv_receiver']
		
		self.tv_receiver.data_source.tableview_cell_for_row = self.tv_receiver_cell_for_row
		self.tv_receiver.data_source.tableview_delete = self.tv_receiver_delete
		self.tv_receiver.delegate.tableview_did_select = self.tv_receiver_did_select
		self.tv_receiver.delegate.tableview_accessory_button_tapped = self.tv_receiver_info_btn
		
		
		self.tf_send_text = self.view['send_view']['tf_send_text']
		self.tf_send_text.delegate = self.tf_send_text_Delegate
		self.tf_send_text.delegate.textfield_did_change = self.tf_send_text_did_change
		self.tf_send_text.autocorrection_type = False
		self.tf_send_text.spellchecking_type =False
		self.tf_send_text.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
		self.tf_send_text.text = clipboard.get()
		
		self.bt_select = self.view['send_view']['bt_select']
		self.bt_select.action = self.bt_select_action
		
		self.bt_send = self.view['send_view']['bt_send']
		self.bt_send.action = self.bt_send_action
		
		self.bt_send_text = self.view['send_view']['bt_send_text']
		self.bt_send_text.action = self.bt_send_text_action
		
		self.bt_clear = self.view['send_view']['bt_clear']
		self.bt_clear.action = self.bt_clear_action
		
		self.receive_view = self.view['receive_view']
		
		self.send_label1 = self.send_view['send_label1']
		
		self.textv_send_file = self.view['send_view']['textv_send_file']
		
		
		self.tv_progress = self.view['receive_view']['tv_progress']
		self.tv_progress.data_source.items = [ str(x) for x in range(1, self.connect_limit + 1)]
		self.tv_progress.data_source.tableview_cell_for_row = self.tv_progress_cell_for_row
		self.tv_progress.data_source.tableview_delete = self.tv_progress_delete
		self.tv_progress.delegate.tableview_did_select = self.tv_progress_did_select
		self.tv_progress.delegate.tableview_accessory_button_tapped = self.tv_progress_info_btn
		
		self.tf_password = self.view['send_view']['tf_password']
		self.tf_password.delegate = self.tf_password_Delegate
		self.tf_password.delegate.textfield_did_change = self.tf_password_did_change
		self.tf_password.autocorrection_type = False
		self.tf_password.spellchecking_type =False
		self.tf_password.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
		self.tf_password.text = password
		
		# making progress cell obj
		self.progress_cell_dict = {}
		for i in range(1, self.connect_limit + 1): 
			cell = ui.TableViewCell('subtitle')
			
			cell_label = ui.Label(frame=(0,0,ui.get_window_size()[0],44),name="label")
			cell_label.alpha = 0.5
			cell_label.width = 0
			cell_label.flex = "WLRTB"
			#cell_label.frame = (0,0,ui.get_window_size()[0] ,44)
			
			cell.content_view.add_subview(cell_label)
			cell._width = cell.width
			cell.width = 0
			cell.content_view["label"].bg_color = 'yellowgreen'
			cell.text_label.text = 'test'
			self.progress_cell_dict[i] = {}
			self.progress_cell_dict[i]['cell_obj'] = cell
			self.progress_cell_dict[i]['lock'] = threading.Lock()
		
		self.exit_flag = False
		self.exit_receive_server_flag = False
		self.send_file_list = []
		
		self.receiver = None
		self.receive_view['label1'].text = 'Save dir {}'.format(self.save_dir)
	
	def bt_send_text_action(self, sender):
		threading.Thread(target=self.send, args=(self.tf_send_text.text, self.receiver)).start()
		
	def tv_progress_cell_for_row(self, tableview, section, row):
		lst = tableview.data_source
		selected_item = lst.items[row]
		try:
			cell = self.progress_cell_dict[int(selected_item)]['cell_obj']
		except:
			cell = ui.TableViewCell('subtitle')
		"""cell.detail_text_label.text_color = '#757575'
		cell.detail_text_label.text = 'Detail text here'
		
		cell.text_label.text = selected_item
		cell.accessory_type = 'detail_button'
		cell.image_view.image = ui.Image.named('emj:Cat_Face_Grinning')"""
		
		return cell
	
	def tv_progress_did_select(self, tableview, section, row):
		lst = tableview.data_source
		selected_item = lst.items[row]
		lst.selected_row = row
		if lst.action:
			lst.action(lst)
		speech.say(selected_item, 'en-US')
		
	def tv_progress_delete(self, tableview, section, row):
		lst = tableview.data_source
		selected_item = lst.items[row]
		del lst.items[row]
		speech.say(selected_item+' was deleted', 'en-US')
		
	def tv_progress_info_btn(self, tableview, section, row):
		import console
		lst = tableview.data_source
		selected_item = lst.items[row]
		console.hud_alert(selected_item)
		
		
	def did_load(self):
		frame = (0, 40, 540, 530)

		self.receive_view.frame = frame
		self.send_view.frame = frame
		self.bt_send.enabled = False
		self.bt_send_text.enabled = False
		self.tf_send_text.enabled = False
		self.bt_select.enabled = False
		self.tv_receiver.data_source.items = []
		
		self.limit = threading.Semaphore(self.connect_limit)
		self.error_list = Queue.Queue()
		requests.packages.urllib3.disable_warnings()
		self.appear_send_v()
	
		port = 9999
		self.scanner = Scanner(port)
		self.scan()
		
		threading.Thread(target=self.start_receive_server).start()
		
		self.scanner.start_server()
		
	class tf_password_Delegate():
		pass
	
	def tf_password_did_change(self, textfield):
		
		pass		
		
	def bt_clear_action(self, sender):
		self.textv_send_file.text = ''
		self.send_file_list = []
		
	def get_empty_progress(self):
		for i, progress_dict in six.iteritems(self.progress_cell_dict):
			cell_obj = progress_dict['cell_obj']
			lock = progress_dict['lock']
			if lock.acquire(False):
				break
		else:
			Exception('Error')
		return cell_obj, lock
		
	def downloader(self, key):
		try:
			
			# この段階で一つは空いてるはず
			cell_obj, lock = self.get_empty_progress()

			
			response = self.get_data('get_file', key)
			file_path = self.file_list_dict[key]
			
			_file_path = os.path.basename(file_path)
			with open(file_path, "wb") as f:

				total_length = response.headers.get('content-length')
				
				if total_length is None or int(total_length) <= 100: # no content length header
					f.write(response.content)
				else:
					dl = 0
					total_length = int(total_length)
					dl_time = time.time()
					dl_speed = 0
					dl_size_per_sec = 0
					one_sec_passed = False
					eta = 0
					for data in response.iter_content(chunk_size=int(total_length/100)):
						dl += len(data)
						f.write(data)
						done = int(50 * dl / total_length)
						percent = int(100 * dl / total_length )
						dl_size_per_sec += len(data)
						if time.time() - dl_time >= 1:
							#to get dl speed
							dl_time = time.time()
							dl_speed = human_size(dl_size_per_sec)
							eta = (total_length - dl)/dl_size_per_sec
							dl_size_per_sec = 0
							one_sec_passed = True
							
						eta_min = int(eta/60) if int(eta/60)>=10 else "0"+str(int(eta/60))
						eta_sec = int(eta%60) if int(eta%60)>=10 else "0"+str(int(eta%60))
						if eta_min == "00" and eta_sec == "00":
							eta_text = "∞"
						else:
							eta_text = "{}:{}".format(eta_min,eta_sec)
						if percent == 100:
							eta_text = "00:00"
						
						cell_obj.content_view["label"].width = self.view.width * percent / 100
						cell_obj.text_label.text = '{} {} {}% {}/s {}'.format(_file_path, human_size(total_length), percent, dl_speed if one_sec_passed else human_size(dl_size_per_sec), eta_text)
					
					
					
		except Exception as e:
			
			#print traceback.format_exc()
			#print(e)
			self.error_list.put(key)
		finally:
			lock.release()
			self.limit.release()
			
	
	def get_data(self, key, value='True'):
		url = 'https://{}:{}'.format(self.receiver_ip, self.receiver_port)
		headers = {key:value, 'password':self.tf_password.text}
		r = requests.get(url, headers=headers, verify=False, stream=True)
		return r
	
	def receive(self):
		
		print('getting file info')
		r = self.get_data('get_info')
		if not r.status_code == 200:
			
			print('Finish')
			self.get_data('finish')
		
			threading.Thread(target=self.start_receive_server).start()
			print('Password is incorrect')
			return 
			
		self.file_list_dict = json.loads(r.content)
		
		if 'send_text' in self.file_list_dict:
			# send text mode
			print('Text mode')
			text = self.file_list_dict['send_text']
			clipboard.set(text)
			print(text)
			threading.Thread(target=console.hud_alert, args=('Copied to clipboard',) ).start()
			
		else:
			# file transfer mode
			print('Transfer mode')
			for i in range(1, len(self.file_list_dict) + 1):
				key = 'file_' + str(i)
				
				self.file_list_dict[key] = self.save_dir + os.sep + self.file_list_dict[key]
				file_path = self.file_list_dict[key]
				if not os.path.dirname(file_path) == '' and not os.path.exists(os.path.dirname(file_path)):
					os.makedirs(os.path.dirname(file_path))
				self.limit.acquire()
				threading.Thread(target=self.downloader, args=(key,), name='Transfer_Downloader').start()
	
			thread_list = [ x for x in threading.enumerate() if x.name=='Transfer_Downloader' ]
			for _ in thread_list:
				_.join()
			while True:
				if self.error_list.empty():
					break
				
				key = self.error_list.get()
				file_path = self.file_list_dict[key]
				print('Trying to redownload {}'.format(file_path))
				try:
					self.downloader(key)
				except:
					print('Error!!')
					print(traceback.format_exc())
				else:
					print('Done!!')
		
		print('Finish')
		self.get_data('finish')
		
		threading.Thread(target=self.start_receive_server).start()
		
	def start_receive_server(self):
		
	
		print('Waiting for clinet to connect...')
		socket.setdefaulttimeout(5)
		c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		c.settimeout(1)
		c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			c.bind(('', 1234))
		except Exception as e:
			if str(e) == '[Errno 48] Address already in use':
				c.close()
				c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				c.bind(('', 1234))
		c.listen(5)
		
		while True:
			if self.exit_receive_server_flag:
				print('End Rceive Server')
				self.exit_receive_server_flag = False
				return 
			try:
				s, a = c.accept()
				#s.settimeout(30)
			except socket.timeout:
				print('Waiting for clinet to connect...')
			else:
				break
			
			time.sleep(1)
	
		print('Connected. Getting ip.')
		data = s.recv(1024)
		ip, port = json.loads(data)
		print((ip, port))
		print(self.scan_result[ip])
		self.receiver_ip = ip
		self.receiver_port = port
		self.appear_receive_v()
		if console.alert('Receive', '{} is trying to connect'.format(self.scan_result[ip]['host_name']), 'Deny', 'Accept', hide_cancel_button=True) == 2:
			
			self.receive()
		else:
			self.get_data('finish')
			self.appear_send_v()
			
			
		
		s.close()
		c.close()

	def start_send_server(_self, file_list, port):
		class Handler(BaseHTTPRequestHandler):
			
			def server_activate(self):
				self.socket.listen(_self.connect_limit)#self.request_queue_size)
			
			def log_message(self, format, *args):
				pass
				
			def do_GET(self):
				
				#print self.headers
				
				if not 'password' in self.headers:
					self.send_response(111)
					return
					
				if self.headers['password'] == _self.tf_password.text:
					self.send_response(200)
				else:
					print('Password is incorrect')
					self.send_response(111)
					return
				
									
				if 'get_info' in self.headers:
					self.end_headers()
					self.wfile.write(file_list_dict_for_receiver_str)

					return
					
				elif 'finish' in self.headers:
					self.send_header("finish", 'True')
					print('finish')
					self.server.shutdown()
					_self.textv_send_file.text = ''
					_self.send_file_list = []
					console.hide_activity()
					threading.Thread(target=_self.start_receive_server).start()
					return
					
				elif 'get_file' in self.headers:
					file_path = file_list_dict[self.headers['get_file']]
				
				else:
					self.end_headers()
					self.wfile.write("""\
<head>
<title>Error response</title>
</head>
<body>
<h1>Error response</h1>
<p>Message: Please use Transfer application
</body>
""")
					return
					
				
				#self.send_response(200)
				console.show_activity("Sending {}...".format(os.path.basename(file_path)))
				self.send_header("Content-Length", str(os.path.getsize(file_path)))
				self.end_headers()
				
				f = open(file_path, 'r')
				try:
					shutil.copyfileobj(f, self.wfile)
				except Exception as e:
					pass
				finally:
					f.close()
				return
				
		class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
			"""Handle requests in a separate thread."""
		
		if type(file_list) == type(list()):
			file_list_dict = {}
			file_list_dict_for_receiver = {}
			for i, file in enumerate(file_list):
				file_list_dict['file_'+str(i+1)] = file
				file_list_dict_for_receiver['file_'+str(i+1)] = file.replace(to_abs_path()+'/', '')
			
			file_list_dict_for_receiver_str = json.dumps(file_list_dict_for_receiver)
			
		elif type(file_list) == type(str()) or type(file_list) == type(unicode()):
		
			file_list_dict_for_receiver_str = json.dumps({'send_text':file_list})
		
		
			
		server = ThreadedHTTPServer(('', port), Handler)
		print('Starting server')
		server.socket = ssl.wrap_socket (server.socket, certfile=_self.cert_path, server_side=True)
		server.serve_forever()

	def send(self, file_list, ip):
		
	
		print('Trying to connect...')
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#s.settimeout(30)
		try:
			s.connect((ip, 1234))
		except Exception as e:
			if str(e) == '[Errno 48] Address already in use':
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				s.connect((ip, 1234))
					
		print('Connected. Sending ip and port.')
		current_ip = self.scanner.port_scan.current_ip
		port = 7777
		s.sendall(json.dumps([current_ip, port]))
		
		
		s.close()
		self.exit_receive_server_flag = True
		self.start_send_server(file_list, port)
		
		
		
	def scan(self):
		scan_interval = 1
		self.send_label1.text = 'Refresh in {}s'.format(scan_interval)
		def _scan():
			while True:
				self.scan_result = self.scanner.scan()
				
				if self.scan_result:
					self.tv_receiver.data_source.items = self.scan_result.keys()
					self.send_label1.text = ''
					#self.scanner.stop_server()
					break

				for i in range(scan_interval):
					time.sleep(1)
					self.send_label1.text = 'Refresh in {}s'.format(scan_interval-i)
				if self.exit_flag:
					print('End Scan Server')
					break
		threading.Thread(target=_scan, name='Transfer3_scan').start()
		
		
	def appear_receive_v(self):
		self.send_view.hidden = True
		self.receive_view.hidden = False
		self.sc_select.selected_index = 1
	
	def appear_send_v(self):
		self.send_view.hidden = False
		self.receive_view.hidden = True
		self.sc_select.selected_index = 0
		
	def sc_select_action(self, sender):
		selected_item = sender.segments[sender.selected_index]
		if selected_item == 'Receive':
			self.appear_receive_v()
		elif selected_item == 'Send':
			self.appear_send_v()
			
	def tv_receiver_cell_for_row(self, tableview, section, row):
		lst = tableview.data_source
		cell = ui.TableViewCell('subtitle')
		cell.detail_text_label.text_color = '#757575'
		
		selected_item = lst.items[row]
		
		ip_dict = self.scan_result[selected_item]
		
		ip = selected_item
		system = ip_dict['system']
		platform = ip_dict['platform']
		host_name = ip_dict['host_name']
		
		text = '{} {}'.format(host_name, ip)
		detail_text = '{} {}'.format(system, platform)
		cell.text_label.text = text
		cell.detail_text_label.text = detail_text
		cell.accessory_type = 'detail_button'

		if system == 'Darwin':
			cell.image_view.image = ui.Image.named('iob:social_apple_256')
			
		
		return cell
		
	def tv_receiver_did_select(self, tableview, section, row):
		lst = tableview.data_source
		selected_item = lst.items[row]
		lst.selected_row = row
		if lst.action:
			lst.action(lst)
		self.bt_send.enabled = True
		self.bt_send_text.enabled = True
		self.tf_send_text.enabled = True
		self.bt_select.enabled = True
		self.receiver = selected_item
		
	def tv_receiver_delete(self, tableview, section, row):
		lst = tableview.data_source
		selected_item = lst.items[row]
		del lst.items[row]
		speech.say(selected_item+' was deleted', 'en-US')
		
	def tv_receiver_info_btn(self, tableview, section, row):
		import console
		lst = tableview.data_source
		selected_item = lst.items[row]
		console.hud_alert(selected_item)
		
		
	class tf_send_text_Delegate():
		pass
		
	def tf_send_text_did_change(self, textfield):
		pass
		
	def bt_select_action(self, sender):
		files = file_picker('Pick files', multiple=True, select_dirs=True, file_pattern=r'^.+$')
		if files:
			for file in files:
				if os.path.isfile(file):
					self.send_file_list.append(file)
				elif os.path.isdir(file):
					self.send_file_list.extend(get_file_list(file))
		self.textv_send_file.text = '\n'.join(self.send_file_list)
	
	def bt_send_action(self, sender):
		threading.Thread(target=self.send, args=(self.send_file_list, self.receiver)).start() #self.send(self.send_file_list, self.receiver)
		
		
class _Transfer3(Transfer3):
	def __init__(self):
		pass
		
	def did_load(self):
		self.main_view = Transfer3(self)
		self.main_view.did_load()
		
	def will_close(self):
		self.main_view.exit_flag = True
		self.main_view.exit_receive_server_flag = True
		self.main_view.scanner.stop_server()
		

v = ui.load_view()


v.present('sheet')

