JAVASCRIPT = '''function hello_world() {
    alert('hello {}');
}'''
                
HTML = '''<html>
    <head>
        <title> Hello {} </title>
    </head>
    <body>
        <p> Hello World </p>
    </body>
</html>'''
          
CSS = '''p {
    color: #000000;
}\n'''


## TODO - Update the request handler to work for this setup.
REQUEST_HANDLER = '''class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print self.path
        if self.path in ['', '/', '/index.html']:
            self.send_response(200)
            self.end_headers()
            index = view['editor_view']['file_nav'].selected_index
            if not index == -1:
                file = view['editor_view']['file_nav'].segments[index]
            #print file
            file_data = file_system['data'][file][0]
            #print file_data
            self.wfile.write(file_data)
        else:
            name = self.path.split('/')[-1]
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(file_system['data'][name][0])
            except:
                pass'''
