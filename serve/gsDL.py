from __future__ import print_function
# https://gist.github.com/pudquick/5606582

import re, hashlib, uuid, json, random, os, urllib2, os.path, time, sys, SimpleHTTPServer, SocketServer, string, console, webbrowser, shutil, zipfile

class SmarterHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    server_version = 'SimpleHTTP/0.6'
    file_name   = ''
    def do_GET(self):
        if self.path.startswith('/transfer'):
            self.get_transfer()
        else:
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
    def get_transfer(self):
        global did_download
        try:
            # Perform the actual file download
            self.send_response(200)
            # Content-Disposition: attachment; filename="fname.ext"
            self.send_header('Content-Disposition', 'attachment; filename="%s"' % (self.file_name.split('/',1)[-1]))
            self.send_header('Content-Length', '%s' % (os.path.getsize(self.file_name)))
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            f = open(self.file_name, 'rb')
            self.copyfile(f, self.wfile)
            f.close()
        except:
            sys.exc_clear()
        did_download = True
    def log_message(self, format, *args):
        return
    def finish(self):
        # Fix for iDownload when it early terminates a transfer to get file details
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except:
                sys.exc_clear()
        try:
            self.wfile.close()
        except:
            sys.exc_clear()
        try:
            self.rfile.close()
        except:
            sys.exc_clear()

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
    def handle_error(self, request, client_address):
        # Overidden, don't care to see any messages
        return
    def release(self):
        try:
            self.server_close()
        except Exception:
            sys.exc_clear()
        try:
            self.socket.close()
        except Exception:
            sys.exc_clear()

class pyGroovClient:
    def __init__(self):
        self.client_url   = 'http://html5.grooveshark.com/'
        self.s_client_url = self.client_url.replace('http', 'https')
        # This user agent is in the top 7% of user agents on the web
        self.user_agent   = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'
        # Trigger client setup
        pyGroovClient.setupClient(self)
    def _chunk_report(self, bytes_so_far, chunk_size, total_size):
        if (total_size != None):
            percent = float(bytes_so_far) / total_size
            percent = round(percent*100, 2)
            print('Downloaded %d of %d bytes (%0.2f%%)' % (bytes_so_far, total_size, percent))
            if bytes_so_far >= total_size:
                print('')
        else:
            print('Downloaded %d bytes' % (bytes_so_far))
    def _chunk_read(self, response, chunk_size=32768, report_hook=None, filename=None, streamDict=None):
        # Delete old file if it's present
        if os.path.exists(filename):
            os.remove(filename)
        # Set up the file handler
        try:
            f = open(filename, 'wb')
        except Exception:
            print('! Error:', sys.exc_info()[1])
            raise        
        start_time = time.time()
        did_hit_30 = False
        time_so_far = 0
        if response.info().has_key('Content-Length'):
            total_size = response.info().getheader('Content-Length').strip()
            total_size = int(total_size)
        else:
            # No size
            total_size = None
            if report_hook:
                print('* Warning: No total file size available.')
        bytes_so_far = 0
        i = 0
        while True:
            chunk = response.read(chunk_size)
            bytes_so_far += len(chunk)
            # Check time, notify when complete
            now_time = time.time()
            if not did_hit_30:
                if abs(now_time - start_time) >= 30:
                    did_hit_30 = True
                    print("* Notifying 30 seconds of play ...")
                    self._markStreamKeyOver30Seconds(streamDict)
                    # Set remaining time to 0
                    time_so_far = 31.0
            if not chunk:
                break
            else:
                f.write(chunk)
            if not i:
                report_hook(bytes_so_far, chunk_size, total_size)
            i = (i+1)%5
        if not did_hit_30:
            # We didn't hit 30 seconds during the download, better let parent method know
            # For safety, since we know we didn't send the message and don't want a race condition, assume no greater than 29 seconds
            time_so_far = min(29.0, time.time() - start_time)
        try:
            f.close()
        except:
            _ = False
        if bytes_so_far > 0:
            print('* Saved to:', filename)
            return (os.path.abspath(filename), time_so_far)
        else:
            print('* Error: 0 bytes downloaded, not saved.')
        return (None, time_so_far)
    def _download(self, src_url, fname='download.mp3', streamDict=None):
        headers = {'User-Agent': self.user_agent, 'Cookie': 'PHPSESSID=%s' % self.session}
        print('INFO: This download will take a *minimum* of 30 seconds, to keep Grooveshark from banning you.')
        print('* Downloading:', src_url)
        req = urllib2.Request(src_url, headers=headers)
        response = urllib2.urlopen(req)
        filename,time_spent = self._chunk_read(response, report_hook=self._chunk_report, filename=fname, streamDict=streamDict)
        if filename:
            if time_spent < 30.0:
                # Need to sleep a little longer, then notify the 30 second download
                print("* Waiting remaining seconds to reach 30 ...")
                time.sleep(31.0 - time_spent)
                print("* Notifying 30 seconds of play.")
                self._markStreamKeyOver30Seconds(streamDict)
            print("* Completed.")
            return filename
        else:
            print("* Error, aborting.")
            if os.path.exists(fname):
                os.remove(fname)
    def setupClient(self):
        # Generally only called by __init__, but can be called manually to create a new session
        # Create a single web browsing session to retain cookies, headers, etc.
        self.sess         = requests.Session()
        # Fake our user agent
        self.sess.headers.update({'User-Agent': self.user_agent})
        # Load the initial page to get a PHP session cookie and a few other configuration settings
        _ = self.sess.get(self.client_url)
        self.base_html = _.content
        # Some of these help fake out Grooveshark so it doesn't know this is a software library.
        # Download but ignore /build/app.min.css?####
        _ = re.search(r'build/app\.min\.css\?[0-9]+', self.base_html).group()
        _ = self.sess.get(self.client_url + _)
        # Download but ignore /build/libs.min.js?####
        _ = re.search(r'build/libs\.min\.js\?[0-9]+', self.base_html).group()
        _ = self.sess.get(self.client_url + _)
        # Download and keep /build/app.min.js?####
        _ = re.search(r'build/app\.min\.js\?[0-9]+',  self.base_html).group()
        _ = self.sess.get(self.client_url + _)
        self.app_js = _.content
        # Exctract the app and base configuration blocks
        app_snip  = re.search(r'SERVICE_CREATE_TOKEN_FAIL.+?(var .+?lastRandomizer.+?;)', self.app_js).groups()[0]
        base_snip = re.search(r'window\.GS\.config.+?(\{.+?\});', self.base_html).groups()[0]
        # From app determine: client, clientRevision, revToken
        self.client         = re.search(r'client:[ ]*"(.+?)"', app_snip).groups()[0]
        self.clientRevision = re.search(r'clientRevision:[ ]*"(.+?)"', app_snip).groups()[0]
        self.revToken       = re.search(r'="([^"]+?)"', app_snip).groups()[0]
        # From base determine: privacy, country
        self.privacy        = re.search(r'"Privacy":[ ]*([0-9]+?)', base_snip).groups()[0]
        self.country        = re.search(r'"country":[ ]*(\{.+?\})', base_snip).groups()[0]
        # From sess determine: session, secretKey (it's present in base, but we're using sess's cookies to do future requests - should be same)
        self.session        = self.sess.cookies['PHPSESSID']
        self.secretKey      = hashlib.md5(self.session).hexdigest()
        # Generate a UUID
        self.uuid           = str(uuid.uuid4()).upper()
        # Get our communication token
        self._getCommunicatonToken()
    def search(self, searchStr):
        # Song search, in order of best match
        try:
            return self._getResultsFromSearch(searchStr.replace('"', '\\"'))['result']['result']['Songs']
        except:
            return []
    def download(self, songDict, filepath):
        stream_info = self._getStreamKeyFromSongIDEx(songDict)
        if not stream_info:
            # Song was either removed by Grooveshark or is not available to HTML5/mobile/non-Flash client
            return False
        # A download is available, download it - but mark it as downloaded first (HTML5 client does this)
        _ = self._markSongDownloadedEx(stream_info)
        # Then download it :)
        download_url = 'http://%s/stream.php?streamKey=%s' % (stream_info['ip'],stream_info['streamKey'])
        return self._download(download_url, fname=filepath, streamDict=stream_info)
    def _getCommunicatonToken(self):
        # Use the secure client for the token
        gCT_json = '{"header":{"client":"%s","clientRevision":"%s","privacy":%s,"country":%s,"uuid":"%s","session":"%s"},"method":"getCommunicationToken","parameters":{"secretKey":"%s"}}'
        _ = self.sess.post(self.s_client_url + '/more.php?getCommunicationToken', data=gCT_json % (self.client, self.clientRevision, self.privacy, self.country, self.uuid, self.session, self.secretKey))
        # Use json lib to future proof against newer versions of requests
        self.token = json.loads(_.content)['result']
    def _prepToken(self, method):
        rnd = hashlib.md5(str(random.random())).hexdigest()[:6]
        return rnd + hashlib.sha1(':'.join([method, self.token, self.revToken, rnd])).hexdigest()
    def _buildAPIcall(self, method, parameters):
        core_msg = '{"header":{"client":"%s","clientRevision":"%s","privacy":%s,"country":%s,"uuid":"%s","session":"%s","token":"%s"},"method":"%s","parameters":%s}'
        return core_msg % (self.client, self.clientRevision, self.privacy, self.country, self.uuid, self.session, self._prepToken(method), method, parameters)
    def _doAPIcall(self, method, parameters):
        _ = self.sess.post(self.client_url + 'more.php?%s' % method, data=self._buildAPIcall(method, parameters))
        return _.content
    def _getResultsFromSearch(self, searchStr):
        params = '{"query":"%s","type":["Songs","Playlists","Albums"],"guts":0,"ppOverride":""}'
        return json.loads(self._doAPIcall('getResultsFromSearch', params % searchStr))
    def _getStreamKeyFromSongIDEx(self, songDict):
        params = '{"prefetch":false,"mobile":true,"songID":%s,"country":%s}'
        return json.loads(self._doAPIcall('getStreamKeyFromSongIDEx', params % (songDict['SongID'], self.country)))['result']
    def _markSongDownloadedEx(self, streamDict):
        # streamKey, streamServerID, songID
        params = '{"streamKey":"%s","streamServerID":%s,"songID":%s}'
        return json.loads(self._doAPIcall('markSongDownloadedEx', params % (streamDict['streamKey'],streamDict['streamServerID'],streamDict['SongID'])))['result']
    def _markStreamKeyOver30Seconds(self, streamDict):
        params = '{"streamKey":"%s","streamServerID":%s,"songID":%s}'
        return json.loads(self._doAPIcall('markStreamKeyOver30Seconds', params % (streamDict['streamKey'],streamDict['streamServerID'],streamDict['SongID'])))['result']

# iDownloads

def sanitize(filename):
    safe = string.letters + string.digits + "()-.,_+{}'"
    return ''.join([['_',x][x in safe] for x in filename])

def do_search_and_download(gsClient):
    print("\nEnter your search:")
    searchStr = raw_input('> ').strip()
    if not searchStr:
        print("* Cancelled.")
        return
    print("* Searching ...")
    results = gsClient.search(searchStr)
    top8 = results[:8]
    if not top8:
        print("! No results found for:", searchStr)
        return
    print("* Found, enter the number for download:")
    for i,x in enumerate(top8):
        print("%s) %s - %s - %s" % (i+1, x['SongName'], x['ArtistName'], x['AlbumName']))
    print('0) Cancel')
    choice = ''.join([x for x in raw_input('> ').strip() if x in '0123456789'])
    if (choice in ['0','']):
        print("* Cancelled.")
        return
    else:
        nChoice = int(choice) - 1
    cDict = top8[nChoice]
    print("*Downloading: %s" % cDict['SongName'])
    fname = "gs_dl/" + sanitize("%s - %s - %s.mp3" % (cDict['ArtistName'], cDict['AlbumName'],cDict['SongName']))
    if not os.path.exists('gs_dl'):
        os.makedirs('gs_dl')
    if gsClient.download(cDict, fname) == False:
        print("* Song not available (removed or not for mobile).")
        return
    # Prep webserver
    global ready_to_stop, did_download
    ready_to_stop = False
    did_download = False
    port = 8000
    handler = SmarterHTTPRequestHandler
    # Configure transfer settings
    handler.file_name   = fname
    httpd = SmarterHTTPD(("", port), handler, False)
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    download_url = 'http://127.0.0.1:8000/transfer'
    download_url = download_url.replace('http://', 'iDownloads://')
    print('* Transferring to browser ...')
    webbrowser.open(download_url)
    # print download_url
    httpd.serve_limited(timeout=3,max_requests=8)
    httpd.release()
    if did_download:
        print('* Transfer complete, deleting local copy.')
    else:
        print('* Transfer did not complete, deleting local copy.')
    try:
        os.remove(fname)
    except:
        _ = False
    return

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

def main():
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
        return
    try:
        gsc = pyGroovClient()
    except Exception:
        sys.exc_clear()
        print("* Error initializing GS client, make sure you're online.")
        return
    console.clear()
    print("* Client successfully initialized")
    loop = True
    while loop:
        print("Enter a menu number choice:")
        print("--------------------------")
        print("1) Search and download")
        print("0) Quit")
        choice = ''.join([x for x in raw_input('> ').strip() if x in '0123456789'])
        if (choice in ['0','']):
            print("* Quit.")
            loop = False
        elif (choice in ['1']):
            do_search_and_download(gsc)
        else:
            print("* Unknown choice number, try again.")
        print("")

if __name__ == "__main__":
    main()