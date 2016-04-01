# -*- coding: utf-8 -*-
class Structure(object):
    _fields = []

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k in self._fields:
                setattr(self, k, v)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __repr__(self):
        return repr(self.__dict__)


# noinspection PyUnresolvedReferences
class Show(Structure):
    _fields = [
        'asset_id',
        'pubDate',
        'series_name',
        'series_description',
        'episode_count',
        'genres',
        'show_rating',
        'thumbnail_large',
        'poster_art',
        'popularity',
    ]

    @property
    def label(self):
        return self.series_name

    @property
    def label2(self):
        return '[{0}]'.format(self.show_rating)

    @property
    def icon(self):
        return self.thumbnail_large

    @property
    def thumbnail(self):
        return self.poster_art

    @property
    def info(self):
        return {
            'genre': self.genres,
            'plot': self.series_description,
            'episode': self.episode_count,
            'year': self.pubDate.split('/')[2],
            'votes': str(self.popularity),
            'mpaa': self.show_rating,
            'aired': '{2}-{1}-{0}'.format(*self.pubDate.split('/')),
        }

    @property
    def query(self):
        return {'show_id': self.asset_id, 'get': 'videos'}

    @property
    def genre(self):
        if self.genres is not None:
            return self.genres.split(',')
        else:
            return ''


# noinspection PyUnresolvedReferences
class Video(Structure):
    _fields = [
        'asset_id',
        'releaseDate',
        'title',
        'video_url',
        'quality',
        'description',
        'number',
        'duration',
        'thumbnail_url',
        'rating',
        'releaseDate',
        'dub_sub',
    ]

    @property
    def label(self):
        if self.number:
            # self.number sometimes is a unicode str that's why we use repr()
            lbl = '%s. %s (%s)' % (repr(self.number), self.title, self.dub_sub)
        else:
            lbl = '%s (%s)' % (self.title, self.dub_sub)
        return lbl

    @property
    def sub(self):
        return self.dub_sub == 'Sub'

    @property
    def dub(self):
        return self.dub_sub == 'Dub'

    @property
    def label2(self):
        return '[{0}]'.format(self.rating)

    @property
    def icon(self):
        return self.thumbnail_url

    @property
    def thumbnail(self):
        return self.thumbnail_url

    @property
    def info(self):
        return {
            'plot': self.description,
            'episode': self.number,
            'year': self.releaseDate.split('/')[0],
            'mpaa': self.rating,
            'aired': self.releaseDate.replace('/', '-'),
        }

    @property
    def stream_info(self):
        if '1080' in self.quality:
            w, h = 1920, 1080
        elif '720' in self.quality:
            w, h = 1080, 720
        else:
            w, h = 640, 480
        return {
            'codec': 'mp4',
            'aspect': w / float(h),
            'width': w,
            'height': h,
            'duration': self.duration
        }

    @property
    def query(self):
        return {'videoid': self.asset_id}
