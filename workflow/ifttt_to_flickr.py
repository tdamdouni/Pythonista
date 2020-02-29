#!/usr/bin/python

# Download and docs found at
# http://stuvel.eu/flickrapi

from __future__ import print_function
import flickrapi
from xml.etree import ElementTree as ET
import urllib
import datetime
import os

HOME = os.path.expanduser('~')


def dt_to_str(dt):
    return datetime.datetime.strftime(dt, "%Y.%m.%d %H:%M")


class FlickrIFTTT():
    def __init__(self):
        self.LASTRUN_FILE = HOME + '/Dropbox/IFTTT/appletv/lastrun.txt'
        self.IFTTT_FILE = HOME + '/Dropbox/IFTTT/appletv/appletv.txt'
        self.LASTRUN = self.get_last_run()

        # Flickr Info
        self.API_KEY = ""
        self.API_SECRET = ""
        self.AUTH_TOKEN = ''
        # Apple TV album ID
        self.ALBUM_ID = 0

        self.flickr = self.login()

        self.ifttt_links = []

    def login(self):
        return flickrapi.FlickrAPI(
            self.API_KEY,
            self.API_SECRET,
            token=self.AUTH_TOKEN
        )

    def download_image(self, url, imagename):
        """
        download an image in the form of

        url = http://www.example.com
        image = '00000000.jpg'
        """

        print("Url {}".format(url))
        print("Downloading image {}...".format(imagename))
        BASEPATH = '/tmp/'
        image = urllib.URLopener()
        image.retrieve(url, BASEPATH + imagename)
        return BASEPATH + imagename

    def string_to_date(self, datestring):
        """
            Takes an IFTTT formated datestring
            and returns a datetime object.

            Example: September 08, 2014 at 01:33AM
        """
        return datetime.datetime.strptime(datestring, "%B %d, %Y at %I:%M%p")

    def get_ifttt_links(self):
        """
            Get images from IFTTT.
            Each line of the file should be formatted as
            "{{source_url}}|{{created_at}}"

            Only returns links that need to be updated
            based on the datetime

            returns a list of dicts {url: created_at}

        """

        f = open(self.IFTTT_FILE, 'r')
        readlines = [
            line.replace('\n', '').strip().split('|')
            for line in f.readlines()
            if line.replace('\n', '').strip() != ''
        ]
        self.ifttt_links = [
            dict(url=url, created_at=self.string_to_date(created_at))
            for url, created_at in readlines
            if self.string_to_date(created_at) > self.LASTRUN
        ]

    def move_to_album(self, photo_id, album_id):
        """
            Move a photo based on flickr photo id
            to an album
        """
        print("Moving photo id {} to album {}...".format(
            photo_id,
            album_id
        ))
        self.flickr.photosets_addPhoto(
            photo_id=photo_id,
            photoset_id=album_id
        )

    def upload_photo(self, url, created_at, progress=False):
        downloaded_image = self.download_image(url, created_at + '.jpg')
        print("Uploading Image")
        uploaded_file = self.flickr.upload(
            filename=downloaded_image,
            title=created_at,
            is_public=0,
            hidden=1,
            callback=self.upload_progress if progress else self.no_progress
        )
        photo_id = uploaded_file.find('photoid').text
        return photo_id

    def upload_and_move(self, url, created_at):
        upload = self.upload_photo(url, created_at)
        self.move_to_album(upload, self.ALBUM_ID)

    def ensure_lastrun(self):
        return os.path.exists(self.LASTRUN_FILE)

    def get_last_run(self):
        if self.ensure_lastrun():
            f = open(self.LASTRUN_FILE, 'r').read()
            return datetime.datetime.fromtimestamp(int(f))
        else:
            return datetime.datetime.now() - datetime.timedelta(days=100)

    def set_last_run(self):
        s = datetime.datetime.now().strftime("%s")
        with open(self.LASTRUN_FILE, 'w') as f:
            f.write(s)

    def upload_progress(self, progress, done):
        if done:
            print("Done uploading")
        else:
            print("At %s%%" % progress)

    def no_progress(self, progress, done):
        pass

if __name__ == '__main__':
    flickr = FlickrIFTTT()

    flickr.get_ifttt_links()

    if flickr.ifttt_links:
        print("Last run", flickr.LASTRUN)
        for entry in flickr.ifttt_links:
            created_at = dt_to_str(entry['created_at'])
            flickr.upload_and_move(
                entry['url'],
                created_at
            )
    flickr.set_last_run()
