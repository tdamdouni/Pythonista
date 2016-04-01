# coding: utf-8

import ui
import time

class LockController(object):
	def __init__(self):
		self.view = ui.load_view('view_lock.pyui')
		self.passphrase = 'passphrase'
		self.allowed_tries = 8
		self.tries_left = 8
		self.reset_timeout_start = 30
		self.timeout_start = 30
		self.timeout_multiplier = 2
		self.unlock_callback = None
	
	def set_unlock_callback(self, callback):
		self.unlock_callback = callback
	
	def set_passphrase(passphrase):
		self.passphrase = passphrase
	
	def bt_unlock(self, sender):
		pptf = self.view['passphrase_textfield']
		if (self.passphrase != pptf.text):
			self.tries_left -= 1
			pptf.text = ''
			tlb = self.view['tries_label']
			tlb.text = '%d tries remaining' % self.tries_left
			if self.tries_left == 0:
				self.failed()
		else:
			self.tries_left = self.allowed_tries
			self.timeout_start = self.reset_timeout_start
			pptf.text = ''
			if self.unlock_callback != None:
				self.unlock_callback()
			else:
				self.view.close()
	
	@ui.in_background
	def failed(self):
		pptf = self.view['passphrase_textfield']
		ulbt = self.view['unlock_button']
		tlb = self.view['tries_label']
		pptf.enabled = False
		ulbt.enabled = False
		to_now = int(time.time())
		to_end = to_now + self.timeout_start
		while to_now < to_end:
			left = to_end - to_now
			tlb.text = '%d seconds remaining' % left
			time.sleep(0.5)
			to_now = int(time.time())
		self.tries_left = self.allowed_tries
		self.timeout_start *= self.timeout_multiplier
		tlb.text = '%d tries remaining' % self.tries_left
		pptf.enabled = True
		ulbt.enabled = True
		

if __name__ == '__main__':  # pragma: no cover
	my_app = LockController()
	my_app.view.present(hide_title_bar=True)
