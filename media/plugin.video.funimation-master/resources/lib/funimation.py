# -*- coding: utf-8 -*-
from urllib2 import HTTPError

from .httpclient import HTTPClient


class Funimation(object):

    def __init__(self, username=None, password=None, cookiefile=None):
        super(Funimation, self).__init__()
        self.http = HTTPClient('https://www.funimation.com/', cookiefile,
                               [('User-Agent', 'Sony-PS3')])
        # defaults to the free account user
        # hmm... the API doesn't appear to validate the users subscription
        # level so if this was changed you might be able to watch
        # the paid videos ;)
        self.user_type = 'FunimationUser'
        self.logged_in = self.login(username, password)

    def get_shows(self, limit=1000, offset=0, sort=None, first_letter=None,
                  filter=None):
        query = self._build_query(locals())
        return self.http.get('feeds/ps/shows', query)

    def get_latest(self, limit=1000, offset=0):
        if self.user_type == 'FunimationSubscriptionUser':
            sort = 'SortOptionLatestSubscription'
        else:
            sort = 'SortOptionLatestFree'
        return self.get_shows(limit, offset, sort)

    def get_simulcast(self, limit=1000, offset=0):
        return self.get_shows(limit, offset, filter='FilterOptionSimulcast')

    def get_featured(self, limit=1000, offset=0):
        query = self._build_query(locals())
        return self.http.get('feeds/ps/featured', query)

    def get_videos(self, show_id, limit=1000, offset=0):
        query = self._build_query(locals())
        return self.http.get('feeds/ps/videos', query)

    def search(self, search):
        query = self._build_query(locals())
        return self.http.get('feeds/ps/search', query)

    def get_genres(self):
        # we have to loop over all the shows to be sure to get all the genres.
        # use a set so duplicates are ignored.
        genres = set()
        for show in self.get_shows():
            if show.get('genres'):
                [genres.add(g) for g in show.get('genres').split(',')]
        return sorted(genres)

    def get_shows_by_genre(self, genre):
        shows = []
        for show in self.get_shows():
            if show.get('genres') and genre in show.get('genres').split(','):
                shows.append(show)
        return shows

    def login(self, username, password):
        if not username and not password:
            return False
        cookie = self.http.get_cookie('ci_session')
        # get cookie, if it exists and cookie has a comment
        if cookie is not None and cookie.comment is not None:
            try:
                # try to get the original name and user type
                uname, self.user_type = cookie.comment.split('|')
                if uname == username:
                    self.logged_in = True
                    return True
            except ValueError:
                return False

        payload = {'username': username, 'password': password,
                   'playstation_id': ''}
        try:
            resp = self.http.post('feeds/ps/login.json?v=2', payload)
            utype = resp.get('user_type')
            if utype is not None:
                self.user_type = ''.join([x.title() for x in utype.split('_')])
            # add username as comment so we can check if the user has
            # changed later
            self.http.get_cookie('ci_session').comment = '%s|%s' % (
                username, self.user_type)
            self.logged_in = True
            self.http.save_cookies()
            return True
        except HTTPError:
            # throws a 400 error when login is wrong
            return False

    def _build_query(self, params):
        if params is None:
            params = {}
        params['first-letter'] = params.pop('first_letter', None)
        # since we pass `local()` we need to remove self
        params.pop('self', None)
        params.setdefault('ut', self.user_type)
        return params
