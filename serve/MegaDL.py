from __future__ import print_function
# https://gist.github.com/pudquick/5562741

import os.path, sys, os, SimpleHTTPServer, SocketServer, clipboard, webbrowser, shutil, zipfile, console

__mega_acct__ = 'yourname@example.com'
__mega_pass__ = 'passwordhere'

def _unzip(a_zip=None, path='.', altpath='unzipped'):
    if a_zip is None:
        return
    filename = os.path.abspath(a_zip)
    if not os.path.isfile(filename):
        return
    # PK magic marker check
    f = open(filename, 'rb')
    try:
        pk_check = f.read(2)
    except Exception:
        pk_check = ''
    finally:
        f.close()
    if pk_check != 'PK':
        print("unzip: %s: does not appear to be a zip file" % a_zip)
    else:
        altpath = os.path.join(os.path.dirname(filename), altpath)
        location = os.path.abspath(altpath)
        if not os.path.exists(location):
            os.makedirs(location)
        zipfp = open(filename, 'rb')
        try:
            zipf = zipfile.ZipFile(zipfp)
            # check for a leading directory common to all files and remove it
            dirnames = [os.path.join(os.path.dirname(x), '') for x in zipf.namelist()]
            common_dir = os.path.commonprefix(dirnames or ['/'])
            # Check to make sure there aren't 2 or more sub directories with the same prefix
            if not common_dir.endswith('/'):
                common_dir = os.path.join(os.path.dirname(common_dir), '')
            for name in zipf.namelist():
                data = zipf.read(name)
                fn = name
                if common_dir:
                    if fn.startswith(common_dir):
                        fn = fn.split(common_dir, 1)[-1]
                    elif fn.startswith('/' + common_dir):
                        fn = fn.split('/' + common_dir, 1)[-1]
                fn = fn.lstrip('/')
                fn = os.path.join(location, fn)
                dirf = os.path.dirname(fn)
                if not os.path.exists(dirf):
                    os.makedirs(dirf)
                if fn.endswith('/'):
                    # A directory
                    if not os.path.exists(fn):
                        os.makedirs(fn)
                else:
                    fp = open(fn, 'wb')
                    try:
                        fp.write(data)
                    finally:
                        fp.close()
        except Exception:
            zipfp.close()
            print("unzip: %s: zip file is corrupt" % a_zip)
            return
        zipfp.close()
        return os.path.abspath(location)

def req12_setup():
    import requests as old_req
    relative_dir = os.path.abspath(os.path.dirname(__file__))
    curdir = os.getcwd()
    os.chdir(relative_dir)
    print('!!! requests-1.2.0 not installed, downloading rev.d06908d ...')
    zip_url = 'https://github.com/kennethreitz/requests/archive/v1.2.0.zip'
    print('  * Downloading: requests_1.2.0.zip (565KB)...')
    f = open('requests_1.2.0.zip', 'wb')
    try:
        f.write(old_req.get(zip_url).content)
    except Exception:
        sys.exc_clear()
    f.close()
    # Unload built-in requests module
    del old_req
    print("!!! zip downloaded, extracting ...")
    try:
        shutil.rmtree('requests_zip', ignore_errors=True)
    except Exception:
        sys.exc_clear()
    _ = _unzip('requests_1.2.0.zip', altpath='requests_zip')
    print("!!! Extraction complete, re-arranging ...")
    try:
        shutil.rmtree('requests_1_2', ignore_errors=True)
    except Exception:
        sys.exc_clear()
    os.rename('requests_zip/requests', 'requests_1_2')
    print("!!! Re-arranging complete, cleaning up ...")
    try:
        os.remove('requests_1.2.0.zip')
        shutil.rmtree('requests_zip', ignore_errors=True)
    except Exception:
        sys.exc_clear()
    os.chdir(curdir)

def mega_setup():
    print('!!! richardasaurus/mega.py not installed, downloading rev.878f095056 ...')
    base_git = 'https://raw.github.com/richardasaurus/mega.py/878f095056b31d5f675aa96fecb59ffcaa180143/mega/'
    relative_dir = os.path.abspath(os.path.dirname(__file__))
    # Change directory to the one containing this script
    curdir = os.getcwd()
    os.chdir(relative_dir)
    if not os.path.exists('mega'):
        os.makedirs('mega')
    os.chdir('mega')
    for fname in ['__init__.py', 'crypto.py', 'errors.py', 'mega.py']:
        print('  * Downloading: ', fname, '...')
        f = open(fname, 'wb')
        try:
            f.write(requests.get(base_git + fname).content)
        except Exception:
            sys.exc_clear()
        f.close()
    print("!!! Complete, attempting to import again ...")
    os.chdir(curdir)

def mega_patch():
    # Need to patch mega to use requests_1_2
    relative_dir = os.path.abspath(os.path.dirname(__file__))
    curdir = os.getcwd()
    os.chdir(relative_dir)
    f = open('mega/mega.py','r')
    old_mega = f.read()
    f.close()
    if 'import requests\n' in old_mega:
        print('!!! Patching mega/mega.py to use requests_1_2 ...')
        new_mega = old_mega.replace('import requests\n', 'import requests_1_2 as requests\n')
        f = open('mega/mega.py','w')
        f.write(new_mega)
        f.close()
    os.chdir(curdir)

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

class SmarterHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    server_version = 'SimpleHTTP/0.6'
    file_name   = ''
    file_delete = True
    def do_GET(self):
        if self.path.startswith('/transfer'):
            self.get_transfer()
        else:
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
    def get_transfer(self):
        global ready_to_stop
        print('* Transferring to browser ...')
        # Perform the actual file download
        self.send_response(200)
        # Content-Disposition: attachment; filename="fname.ext"
        self.send_header('Content-Disposition', 'attachment; filename="%s"' % (self.file_name))
        self.send_header('Content-Length', '%s' % (os.path.getsize('mega_dl/' + self.file_name)))
        self.send_header('Content-Type', 'application/octet-stream')
        self.end_headers()
        f = open('mega_dl/' + self.file_name, 'rb')
        self.copyfile(f, self.wfile)
        f.close()
        if self.file_delete:
            os.remove('mega_dl/' + self.file_name)
            print('* Download complete, file deleted.')
        else:
            print('* Download complete, file preserved.')
        ready_to_stop = True
    def log_message(self, format, *args):
        return

class SmarterHTTPD(SocketServer.ThreadingTCPServer):
    keep_running  = True
    requests_left = None
    did_timeout   = False
    def serve_limited(self, timeout=None, max_requests=None):
        global ready_to_stop
        self.timeout       = timeout
        if max_requests is None:
            self.requests_left = None
        else:
            self.requests_left = abs(int(max_requests))
        self.keep_running  = True
        self.did_timeout   = False
        while self.keep_running:
            self.handle_request()
            # print "Request handled."
            if self.requests_left is not None:
                self.requests_left -= 1
                if self.requests_left <= 0:
                    self.keep_running = False
                    # print "EXIT: HIT MAX REQUESTS"
                    continue
            if ready_to_stop:
                self.keep_running = False
                # print "EXIT: TOLD TO STOP"
                continue
    def handle_timeout(self):
        self.did_timeout  = True
    def release(self):
        try:
            self.server_close()
        except Exception:
            sys.exc_clear()
        try:
            self.socket.close()
        except Exception:
            sys.exc_clear()

def do_download():
    # Get what's on the clipboard
    try:
        down_url = clipboard.get()
    except Exception:
        down_url = ''
    # Make sure it's the right format
    if not down_url.startswith('https://mega.co.nz/#'):
        print('!!! Clipboard contents are not a mega URL, aborting. Please try again.')
        sys.exit()
    # Log in
    print('* Logging into Mega ...')
    mega = Mega({'verbose': True})
    m = mega.login(__mega_acct__, __mega_pass__)
    # Check file stats
    print('* Looking up URL file details ...')
    details = m.get_public_url_info(down_url)
    print('* Filename:', details['name'])
    print('* Size:', sizeof_fmt(details['size']))
    # Download
    print('* Downloading ...')
    if not os.path.exists('mega_dl'):
        os.makedirs('mega_dl')
    m.download_url(down_url, 'mega_dl')
    print("Download complete.")
    # Interactive choices
    answer = raw_input('Transfer out using Safari (for Open In ...)? [Y/n]: ')
    if not answer.strip().lower() in ['', 'y', 'yes']:
        # Quit here, they must be using iFunbox or something
        print('* Complete.')
        sys.exit()
    # Delete afterwards?
    answer = raw_input('Delete when complete? [Y/n]: ')
    if not answer.strip().lower() in ['', 'y', 'yes']:
        mega_file_delete = False
        print('* Preserving file after transfer.')
    else:
        mega_file_delete = True
        print('* Will delete file when transfer ends.')
    # Prep webserver
    global ready_to_stop
    ready_to_stop = False
    port = 8000
    handler = SmarterHTTPRequestHandler
    # Configure transfer settings
    handler.file_name   = details['name']
    handler.file_delete = mega_file_delete
    httpd = SmarterHTTPD(("", port), handler, False)
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    # print "serving at port", port
    download_url = 'http://localhost:8000/transfer'
    download_url = download_url.replace('http://', 'safari-http://')
    webbrowser.open(download_url)
    # print 'OPEN: http://localhost:8000/transfer'
    httpd.serve_limited(timeout=3,max_requests=4)
    httpd.release()
    print('* Complete.')
    sys.exit()

def main():
    console.clear()
    global requests
    # Ensure that the requests v.1.2.0 module is available
    requests = None
    init_tries = 3
    while init_tries > 0:
        try:
            import requests_1_2 as requests
            init_tries = 0
        except:
            print("!!! Init failure %s of 3 ..." % (4 - init_tries))
            sys.exc_clear()
            req12_setup()
        init_tries -= 1
    if not requests:
        print('!!! Please check your network connection and try again.')
        sys.exit()
    global Mega
    # Ensure that the mega module is available
    Mega = None
    init_tries = 3
    while init_tries > 0:
        try:
            from mega import Mega
            init_tries = 0
        except:
            print("!!! Init failure %s of 3 ..." % (4 - init_tries))
            sys.exc_clear()
            mega_setup()
            mega_patch()
        init_tries -= 1
    if not Mega:
        print('!!! Please check your network connection and try again.')
        sys.exit()
    # Begin download
    do_download()

if __name__ == "__main__":
    main()