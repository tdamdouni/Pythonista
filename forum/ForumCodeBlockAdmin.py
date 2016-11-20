# coding: utf-8

# https://forum.omz-software.com/topic/1664/forumcodeblockadmin

import ui

class ForumCodeBlockAdmin (ui.View):
	def __init__(self):
		self.__make_self()
		self.__make_wv()
		self.layout()
		self.present('panel')
		
	def layout(self):
		self.__wv.frame = (0, 0, self.width, self.height)
		
	def __make_self(self):
		self.ForumCodeBlockAdmin_version = '5.0'
		self.ForumCodeBlockAdmin_source = 'Original by @tony.'
		self.ForumCodeBlockAdmin_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
		self.ForumCodeBlockAdmin_url = 'http://omz-forums.appspot.com/pythonista/post/5825453289897984'
		self.name = 'Forum'
		self.block_type = None
		self.source_file = None
		self.main_class = None
		self.source_code = None
		self.post_id = None
		self.submit = False
		self.count = 0
		
	def update(self):
		with open(self.source_file, 'r') as fS: self.source_code = fS.read()
		sU = self.main_class + '_url '
		iS = self.source_code.find(sU) + len(sU) + 1
		if self.block_type == 'python':
			self.post_id = self.source_code[iS+48:iS+64]
		elif self.block_type == 'plist':
			self.post_id = self.source_code[iS+48+16:iS+64+16]
		self.__wv.load_url('http://omz-forums.appspot.com/login')
		
	def __make_wv(self):
		self.__wv = ui.WebView()
		self.__wv.scales_page_to_fit = False
		self.__wv.delegate = self.__wvDelegate()
		self.add_subview(self.__wv)
		
	class __wvDelegate (object):
		def webview_did_finish_load(self, webview):
			self = webview.superview
			if self.count == 0:
				self.count += 1
			elif self.count == 1:
				webview.load_url('http://omz-forums.appspot.com/edit-post/' + self.post_id)
				self.count += 1
			elif self.count == 2:
				sO = webview.evaluate_javascript('''document.getElementById("wmd-input").value''')
				if self.block_type == 'python':
					iS = sO.find('```python') + 10
					iF = sO.rfind('```')
				elif self.block_type == 'plist':
					iS = sO.find('```xml') + 7
					iF = sO.rfind('```')
				sN = sO[:iS] + self.source_code + sO[iF:]
				sS1 = sN.replace(str(unichr(92)), str(unichr(92)) * 2)
				sS2 = sS1.replace(str(unichr(10)), str(unichr(92) + 'n'))
				sS3 = sS2.replace('"', str(unichr(92) + '"'))
				webview.evaluate_javascript('''document.getElementById("wmd-input").value = "''' + sS3 + '"')
				if self.submit:
					webview.evaluate_javascript('''document.forms[0].submit()''')
				self.count += 1
				
if __name__ == "__main__":
	fcba = ForumCodeBlockAdmin()
	if True:
		fcba.block_type = 'python'
		fcba.source_file = 'ForumCodeBlockAdmin.py'
		fcba.main_class = 'ForumCodeBlockAdmin'
	else:
		fcba.block_type = 'plist'
		fcba.source_file = 'ClassesPlist.txt'
		fcba.main_class = 'ClassesPlist'
	fcba.submit = False
	fcba.update()
# --------------------

