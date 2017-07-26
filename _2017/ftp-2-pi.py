# coding: utf-8

# https://forum.omz-software.com/topic/3883/upload-any-files-from-any-app-via-pythonista-script-to-my-raspberry-pi-connected-harddisk/5

import appex
import console
import os
import ui
from ftplib import FTP

class MyView(ui.View):
	global file_path,loc_dir,books,lus_sur_ipad,authors_without_book
	
	def __init__(self,w,h):
		self.width = w
		self.height = h
		
		# Message Label for my_hud_alert
		msg = ui.Label(name='msg_label')
		msg.frame = (50,50,w-2*50,40)
		msg.background_color=(0.00, 0.50, 1.00, 0.5)
		msg.bg_color = 'bisque'
		msg.alignment = ui.ALIGN_CENTER
		msg.font= ('Courier-Bold',20)
		msg.hidden = True
		self.add_subview(msg)
		
		# progressbar
		progress_bar = ui.Label(name='progress_bar', flex='')
		progress_bar.background_color=(0.00, 0.50, 1.00, 0.5)
		progress_bar.bg_color=(0.00, 0.50, 1.00, 0.5)
		progress_bar.hidden = True
		self.add_subview(progress_bar)
		
	def will_close(self):
		appex.finish()
		
def callback(p):            # only one system parameter = buffer sent/receive
	global my_ui_view,total_file_size,transmit_file_size
	transmit_file_size = transmit_file_size + len(p)
	if my_ui_view['progress_bar'].hidden:
		my_ui_view['progress_bar'].x = my_ui_view['msg_label'].x
		my_ui_view['progress_bar'].y = my_ui_view['msg_label'].y
		my_ui_view['progress_bar'].height = my_ui_view['msg_label'].height
		my_ui_view['msg_label'].hidden = False
		my_ui_view['progress_bar'].hidden = False
		my_ui_view['progress_bar'].bring_to_front()
	my_ui_view['progress_bar'].width = my_ui_view['msg_label'].width *  (transmit_file_size/total_file_size)
	if transmit_file_size == total_file_size:
		my_ui_view['msg_label'].hidden = True               # hide msg
		my_ui_view['progress_bar'].hidden = True    # hide progress bar
		
def main():
	global my_ui_view,total_file_size,transmit_file_size
	
	w, h = (540,620)
	disp_mode = 'sheet'
	my_ui_view = MyView(w,h)
	my_ui_view.background_color='white'
	my_ui_view.name = 'Upload'
	my_ui_view.present(disp_mode,hide_title_bar=False)
	
	# Sharing: receive file
	fil = appex.get_file_path()
	if fil == None:
		print('no file passed')
		return
		
	server = 'Xxxxx'
	user = 'Xxxxx'
	pwd = 'xxxx'
	server_file = os.path.basename(fil)
	my_ui_view['msg_label'].text =server_file
	
	try:
		ftp = FTP(server) #connect
		ftp.encoding = 'utf-8'
		ftp.login(user,pwd)
		ipad_file = open(fil,'rb')
		transmit_file_size = 0
		total_file_size = os.path.getsize(fil)
		ftp.storbinary('STOR '+server_file,ipad_file,blocksize=8192,callback=callback)
		ipad_file.close()
		ftp.close()
	except Exception as e:
		print(str(e))
		
		
if __name__ == '__main__':
	main()

