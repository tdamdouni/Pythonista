import BaseHTTPServer, cgi, editor, os, ui

class CaptureMedia(ui.View):
    def __init__(self):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.width, self.height = 320, 160
        self._wv = ui.WebView()
        self._wv.hidden = True
        self.add_subview(self._wv)
        self.layout()  # subclasses can override
        self.present('popover')
        global gCaptureMedia
        gCaptureMedia = self
        self.httpsrvr = BaseHTTPServer.HTTPServer(('', 0), TransferRequestHandler)
        self._wv.load_url('http://localhost:' + str(self.httpsrvr.server_address[1]))
        ui.delay(self._start, 0.5)
        self.httpsrvr.serve_forever()

    def layout():
        pass  # subclasses can override
    
    def _start(self):
        self._wv.evaluate_javascript('''
        document.getElementById("file").click();
        function f(){
            if (document.forms["form"]["file"].value == '') {
            setTimeout(function(){f()}, 500);
            } else
            {
                document.getElementById("submit").click();
            }
        }
        setTimeout(function(){f()}, 500);
        ''')

    def will_close(self):
        self.httpsrvr.shutdown()

class TransferRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''--------ideas from OMZ's File Transfer script--------'''
    HTML = '''<!DOCTYPE html><html><body><form id="form" action="/" method="POST"
    enctype="multipart/form-data"><input id="file" name="file" type="file"></input>
    <button id="submit" type="submit">Upload</button></form></body></html>'''

    def do_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        self.do_headers()
        self.wfile.write(self.HTML)

    def get_unused_filename(self, filename, count=0):
        alt_name = filename
        if count:
            basename, ext = os.path.splitext(filename)
            alt_name = '{}-{}{}'.format(basename, count, ext)
        if not os.path.exists(alt_name):
            return alt_name
        return self.get_unused_filename(filename, count + 1)
    
    def do_POST(self):
        environ={'REQUEST_METHOD' : 'POST',
                 'CONTENT_TYPE'   : self.headers['Content-Type']}
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ=environ)
        self.do_headers()
        form_file = form['file']
        dest_filename = self.get_unused_filename(form_file.filename)
        with open(dest_filename, 'w') as outfile:
            outfile.write(form_file.file.read())
        editor.reload_files()
        samename = form_file.filename == dest_filename
        rename_msg = '' if samename else ' (renamed to {})'.format(dest_filename)
        print('{} uploaded{}.'.format(form_file.filename, rename_msg))
        '''--------end omz--------'''
        ui.delay(gCaptureMedia.close, 0)
        ui.delay(self.server.shutdown, 0)

    def log_message(self, format, *args):
        pass

class MyCaptureMedia(CaptureMedia):
    def layout(self):
        self.name = 'My Capture Media'
        self.height = 200
        self.background_color = 'Lime'
        image = ui.Image.named('ionicons-close-24')
        self.left_button_items = [ui.ButtonItem(image=image, action=lambda sender: self.close())]
        self.lHelp = ui.Label(frame=(30, 10, 180, 30))
        self.lHelp.text = 'Please choose media...'
        self.add_subview(self.lHelp)

if __name__ == "__main__":
    #CaptureMedia()
    MyCaptureMedia()
