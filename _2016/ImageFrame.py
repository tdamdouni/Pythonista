#!python2
# -*- coding: utf-8 -*-

# https://gist.github.com/SpotlightKid/be9bc4c08a9e1531287c89182f7931d8

# https://forum.omz-software.com/topic/3781/script-remote-controllable-digital-image-frame

"""Remote-controllable digital image frame with built-in web server."""

import logging
import os
import re
import sys
import threading
import time
import tempfile

from operator import attrgetter
from os.path import join, splitext
try:
    from queue import Empty, Queue
except ImportError:
    from Queue import Empty, Queue
from wsgiref.simple_server import make_server, WSGIRequestHandler

import photos
import ui

import bottle

m = re.match('(?P<maj>\d+)\.(?P<min>\d+)(\.(?P<patch>\d+))?', bottle.__version__)
bottle_version = tuple(int(g) for g in m.group('maj', 'min', 'patch') if g)
if sys.version_info[0] >= 3 and bottle_version < (0, 12, 7):
    import warnings
    warnings.warn("Bottle version (%s) too old. Browser upload may not work reliably." %
                  bottle.__version__)


log = logging.getLogger('ImageFrame')
ALBUM_TITLE = 'Image Frame'
HTML_HEADER = """\
<html>
<head>
<title>{{title if defined('title') else 'Image Frame Upload'}}</title>
</head>
<body>
"""
HTML_FOOTER = """\
</body>
</html>
"""
TMPL_UPLOAD = HTML_HEADER + """\
<h1>Upload Image</h1>
<form action="/upload" method="post" enctype="multipart/form-data" accept="image/*">
  Select a file: <input type="file" name="file" />
  <br />
  <input type="checkbox" id="show" name="show" value="1" checked="checked">
  <label for="show">Show image after upload?</label><br />
  <input type="submit" value="{{submit if defined('submit') else 'Upload'}}" />
</form>
% if defined('url'):
<p>Asset <a href="{{url}}">{{id}}</a> successfully created.</p>
% end
""" + HTML_FOOTER


class ImageFrameView(ui.View):
    def __init__(self, queue, server, check_interval=0.2):
        self.queue = queue
        self.img = None
        self.server = server
        self.check_interval = check_interval
        self.background_color = 'black'
        ui.delay(self.check_queue, .1)

    def check_queue(self, *args, **kw):
        try:
            event = self.queue.get_nowait()
        except Empty:
            pass
        else:
            if event is None:
                self.quit()
            else:
                type, image = event
                if type == 'file':
                    self.load_image_file(image)
                elif type == 'asset':
                    self.load_image_asset(image)

        ui.delay(self.check_queue, self.check_interval)

    def load_image_asset(self, image):
        try:
            asset = photos.get_asset_with_local_id(image)
        except ValueError:
            log.error("Invalid asset: %s" % image)
        else:
            self.img = asset.get_ui_image()
            self.set_needs_display()

    def load_image_file(self, image):
        try:
            img = ui.Image.named(image)
            if not img:
                raise IOError("Image not loaded.")
        except:
            log.error("Invalid image: %s" % image)
        else:
            self.img = img
            self.set_needs_display()

    def quit(self, close=True):
        self.server.stop()
        self.server.join(timeout=3)
        if self.server.is_alive():
            log.warning("Server thread not terminated after 3 seconds!")

        ui.cancel_delays()
        if close:
            self.close()

    def will_close(self):
        self.quit(False)

    def draw(self):
        if self.img:
            wi, hi = self.img.size
            ws, hs = self.width, self.height
            if wi > hi:
                h1 = hi * (ws / wi)
                self.img.draw(0, hs / 2 - h1 / 2, ws, h1)
            else:
                w1 = wi * (hs / hi)
                self.img.draw(ws / 2 - w1 / 2, 0, w1, hs)

#    def touch_ended(self, touch):
#        # Called when a touch ends.
#        self.quit()


class QuietServer(bottle.WSGIRefServer):
    def run(self, handler):
        if self.quiet:
            base = self.options.get('handler_class', WSGIRequestHandler)

            class QuietHandler(base):
                def log_request(*args, **kw):
                    pass

            self.options['handler_class'] = QuietHandler

        self.srv = make_server(self.host, self.port, handler, **self.options)
        self.srv.serve_forever(poll_interval=0.1)


class ServerThread(threading.Thread):
    def __init__(self, app, host='0.0.0.0', port=8080, **kw):
        super(ServerThread, self).__init__()
        self.app = app
        self.host = host
        self.port = port
        self.daemon = False
        self.finished = threading.Event()
        self.server = QuietServer(host=self.host, port=self.port, **kw)

    def run(self, *args, **kw):
        try:
            bottle.run(self.app, server=self.server, quiet=True)
        finally:
            self.finished.set()

    def stop(self):
        if not self.finished.is_set():
            self.server.srv.shutdown()
            for tries in range(1, 4):
                log.debug("Waiting for server thread to shut down (tries: %i)..." % tries)
                if self.finished.wait(timeout=1):
                    log.debug("Server shut down.")
                    break
            else:
                log.warning("Server has not shut down after 3 seconds!")
            self.server.srv.server_close()


webapp = bottle.Bottle()
queue = Queue()

@webapp.error(404)
def error404(error):
    return dict(status='ERR', msg="Nothing here, sorry.")


@webapp.get('/')
@bottle.view(TMPL_UPLOAD)
def index(**kwargs):
    return kwargs


@webapp.get('/show/<name>')
def show(name):
    queue.put(('file', name))
    log.debug("Queued named image '%s' for display.", name)
    return dict(status='OK', msg="Image file queued.")


@webapp.get('/assets')
@webapp.get('/assets/')
def get_assets():
    assets = []
    coll = get_album(ALBUM_TITLE)
    for asset in sorted(coll.assets, key=attrgetter('modification_date'), reverse=True):
        assets.append(dict(
            local_id=asset.local_id,
            width=asset.pixel_width,
            height=asset.pixel_height,
            modified=asset.modification_date.strftime('%Y%m%dT%H%M%S')
        ))
    return dict(status='OK', assets=assets)


@webapp.put('/assets')
@webapp.put('/assets/')
def put_asset():
    tmpdir = tempfile.mkdtemp()
    filepath = join(tmpdir, 'asset.%s' % bottle.request.query.get('type', 'jpg'))

    with open(filepath, 'wb') as fp:
        fp.write(bottle.request.body.read())
    try:
        asset = add_asset(filepath)
    finally:
        os.remove(filepath)
        os.rmdir(tmpdir)

    scheme, host = bottle.request.urlparts[:2]
    url = "%s://%s/assets/%s" % (scheme, host, asset.local_id)
    log.debug("Asset url: %s", url)
    return dict(status='OK', msg="Image asset added.", id=asset.local_id, url=url)


@webapp.get('/assets/<local_id:path>')
def set_asset(local_id):
    queue.put(('asset', local_id))
    log.debug("Queued asset %s for display.", local_id)
    return dict(status='OK', msg="Image asset queued.")


@webapp.get('/shutdown')
@webapp.get('/shutdown/')
def shutdown():
    queue.put(None)
    return dict(status='OK', msg="Shutdown initiated.")


@webapp.post('/upload')
def upload():
    file = bottle.request.files.get('file')

    if not file:
        return dict(status='ERR', msg="No file upload found in request data.")

    name, ext = splitext(file.filename)
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.gif'):
        return dict(status='ERR', msg="Filetype not allowed.")

    tmpdir = tempfile.mkdtemp()
    filepath = join(tmpdir, file.filename)
    file.save(tmpdir)
    log.debug("Saved file upload to '%s'.", filepath)
    try:
        asset = add_asset(filepath)
    finally:
        os.remove(filepath)
        os.rmdir(tmpdir)

    if bottle.request.forms.get('show'):
        queue.put(('asset', asset.local_id))
        log.debug("Queued asset %s for display.", asset.local_id)

    scheme, host = bottle.request.urlparts[:2]
    url = "%s://%s/assets/%s" % (scheme, host, asset.local_id)
    log.debug("Asset url: %s", url)

    return index(id=asset.local_id, url=url)


@webapp.route('/upload', method='ANY')
def upload_redirect():
    bottle.redirect('/')


def add_asset(path, title=ALBUM_TITLE):
    """Add image to photo album 'Image Frame'."""
    try:
        coll = get_album(title)
        if not coll.can_add_assets:
            raise OSError
    except OSError:
        msg = "Sorry, album '%s' does not allow adding images." % title
        log.error(msg)
        abort(401, msg)
    else:
        asset = photos.create_image_asset(path)
        coll.add_assets([asset])
        log.debug("Added asset %s.", asset.local_id)
        return asset


def get_album(title):
    for coll in photos.get_albums():
        if coll.title == title:
            break
    else:
        coll = photos.create_album(title)
    return coll


def main(args=[]):
    logging.basicConfig(level=logging.DEBUG if '-v' in args else logging.INFO)
    server = ServerThread(webapp)
    view = ImageFrameView(queue, server)
    server.start()
    time.sleep(0.1)

    if server.finished.is_set():
        log.error("Could not start web server.")
        server.join(timeout=3)
    else:
        queue.put(('file', 'test:Lenna'))
        view.present('fullscreen', hide_title_bar=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
