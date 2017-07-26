#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://gist.github.com/SpotlightKid/be9bc4c08a9e1531287c89182f7931d8

# https://forum.omz-software.com/topic/3781/script-remote-controllable-digital-image-frame

"""Upload image to the digital image frame."""

from __future__ import print_function, unicode_literals

import argparse
import logging
import os
import sys

from urllib.parse import quote

import requests

log = logging.getLogger('send-image')
HOST = 'ipad2-chris'
PORT = 8080


def upload(host, port, path, show=True):
    ext = os.path.splitext(path)[1][1:]

    try:
        with open(path, 'rb') as fp:
            res = requests.put("http://%s:%s/assets/" % (host, port),
                               data=fp.read(), params=dict(type=ext))

        res = res.json()
        if res.get('status') != 'OK':
            raise IOError(res.get('msg', 'unknown error'))
    except Exception as exc:
        log.error("Upload failed: %s", exc)
    else:
        log.info("Image asset '%s' added.", res['id'])
        if show:
            log.debug("Requesting display of asset '%s'.", res['id'])
            requests.get("http://%s:%s/assets/%s" % (host, port, res['id']))


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('-H', '--host', metavar="HOST", default=HOST,
        help="Host name of image frame device (default: %(default)s)")
    ap.add_argument('-n', '--dont-show', action="store_true",
        help="Don't show image after upload")
    ap.add_argument('-p', '--port', metavar="PORT", default=PORT, type=int,
        help="Port of image frame device server (default: %(default)s)")
    ap.add_argument('-v', '--verbose', action="store_true",
        help="Be verbose")
    ap.add_argument('image', help="Path of image to upload")

    args = ap.parse_args(args if args is not None else sys.argv[1:])

    logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s",
        level=logging.DEBUG if args.verbose else logging.WARNING)

    upload(args.host, args.port, args.image, show=not args.dont_show)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
