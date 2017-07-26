# coding: utf-8

# https://forum.omz-software.com/topic/1282/edit

import ui, os, io, photos, console, SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from PIL import Image as ImageP

class EditView (ui.View):
	def __init__(self):
		self.__make_self()
		self.__make_wv()
		self.did_load()
		self.layout()
		self.present('panel')
		self.__server.serve_forever()
		
	def did_load(self):
		pass
		
	def layout(self):
		self.__wv.frame = (0, 0, self.width, self.height)
		self.__wv.evaluate_javascript('CKEDITOR.instances.editor1.resize(%s, %s);' % (self.__wv.frame[2] - self.margin_w, self.__wv.frame[3] - self.margin_h))
		
	def set_data(self, data):
		self.__wv.evaluate_javascript("CKEDITOR.instances.editor1.setData('" + data + "')")
		
	def get_data(self):
		return self.__wv.evaluate_javascript("CKEDITOR.instances.editor1.document.getBody().getHtml()")
		
	def keyboard_frame_will_change(self, frame):
		self.__wv.evaluate_javascript('CKEDITOR.instances.editor1.resize(%s, %s); setTimeout(function(){window.scrollTo(0,0)},1);' % (self.__wv.frame[2] - self.margin_w, self.__wv.frame[3] - (10 if frame[3] > 0 else self.margin_h) - frame[3]))
		
	def __make_self(self):
		self.EditView_version = '4.0'
		self.EditView_source = 'Original by @tony.'
		self.EditView_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
		self.name = 'Edit'
		os.chdir(os.path.expanduser('~/Documents'))
		self.__server = SocketServer.TCPServer(("", 0), EditRequestHandler)
		self.margin_w = 10
		self.margin_h = 10
		global _gdI
		_gdI = getattr(self, 'document_images', None)
		
	def __make_wv(self):
		self.__wv = ui.WebView()
		self.__wv.load_url('http://localhost:' + str(self.__server.server_address[1]) + '/dummy.html')
		self.__wv.scales_page_to_fit = False
		self.__wv.delegate = self.__wvDelegate()
		self.add_subview(self.__wv)
		
	class __wvDelegate (object):
		def webview_did_finish_load(self, webview):
			webview.superview.layout()
			
	def will_close(self):
		self.__server.shutdown()
		console.hide_output()
		
class EditRequestHandler(SimpleHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		self.__make_self()
		SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
		
	def __make_self(self):
		self.EditRequestHandler_version = '4.0'
		self.EditRequestHandler_source_code = 'Original by @tony.'
		self.EditRequestHandler_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
		
	def do_GET(self):
		if os.path.splitext(self.path)[1] == '.html':
			self.send_response(200)
			self.send_header("Content-type", 'text/html')
			self.send_header("Last-Modified", self.date_time_string())
			self.end_headers()
			self.wfile.write('<!DOCTYPE html><html><head><meta charset="utf-8"><script src="../ckeditor/ckeditor.js"></script></head><body><textarea cols="1" id="editor1" name="editor1" rows="1"></textarea><script>CKEDITOR.replace("editor1",{on: {}});</script></body></html>')
		elif os.path.splitext(self.path)[1] == '.jpg':
			try:
				bI = _gdI[self.path[1:]]
			except:
				with io.BytesIO() as bIO:
					ip = photos.pick_image(show_albums = True)
					ip.save(bIO, ip.format)
					bI = bIO.getvalue()
					_gdI[self.path[1:]] = bI
			self.send_response(200)
			self.send_header("Content-type", 'image/jpeg')
			self.send_header("Content-Length", str(len(bI)))
			self.send_header("Last-Modified", self.date_time_string())
			self.end_headers()
			self.wfile.write(bI)
		else:
			SimpleHTTPRequestHandler.do_GET(self)
			
	def log_message(self, format, *args):
		pass
		
class Documents (object):
	def __init__(self):
		self.__make_self()
		
	def __make_self(self):
		self.Documents_version = '4.0 cut down and bundled with example'
		self.Documents_source_code = 'Original by @tony.'
		self.Documents = 'Permission to use/subclass/redistribute, but NOT to modify code.'
		self.document_images = dict()
		
	def document_read(self):
		sC = 'This<img src = "image1.jpg"> is the <b><i>document</i></b> with multiple images and added images persisted...<br><br><img src = "image2.jpg"> <br>End'
		with io.BytesIO() as bIO:
			ip = ImageP.open('Smiling_1')
			ip.save(bIO, ip.format)
			self.document_images['image1.jpg'] = bIO.getvalue()
		with io.BytesIO() as bIO:
			ip = ImageP.open('Test_Sailboat')
			ip.save(bIO, ip.format)
			self.document_images['image2.jpg'] = bIO.getvalue()
		return sC
		
class MyEditView (Documents, EditView):
	def __init__(self):
		Documents.__init__(self)
		EditView.__init__(self)
		
	def did_load(self):
		self.__make_self()
		
	def layout(self):
		self.margin_h = 40
		self.__bO.frame = (30, self.height - 30, 32, 32)
		super(MyEditView, self).layout()
		
	def __make_self(self):
		self.__make_bO()
		
	def __make_bO(self):
		self.__bO = ui.Button()
		self.__bO.image = ui.Image.named('ionicons-ios7-folder-outline-32')
		self.__bO.action = self.__bOA
		self.add_subview(self.__bO)
		
	def __bOA(self, sender):
		self.set_data(self.document_read())
		
if __name__ == "__main__":
	MyEditView()
	
# --------------------

# w.load_url(os.path.abspath(srcname))

# --------------------

import SocketServer, os
from SimpleHTTPServer import SimpleHTTPRequestHandler
from WebBrowser import WebBrowser

class ViewHandler(SimpleHTTPRequestHandler):
	def log_message(self, format, *args):
		pass
		
if __name__ == "__main__":
	os.chdir(os.path.expanduser('~/Documents/ckeditor/'))
	wb = WebBrowser()
	wb.server = SocketServer.TCPServer(("", 0), ViewHandler)
	wb.open('http://localhost:' + str(wb.server.server_address[1]) + '/samples/')
	wb.server.serve_forever()
	
# --------------------

