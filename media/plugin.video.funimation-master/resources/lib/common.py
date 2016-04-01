# -*- coding: utf-8 -*-
from sys import modules, argv
from urllib import urlencode
from urlparse import parse_qsl
from inspect import stack


STRINGMAP = {
    'browse_shows': 30010,
    'browse_latest': 30011,
    'browse_simulcasts': 30012,
    'browse_featured': 30013,
    'browse_genre': 30014,
    'browse_alpha': 30015,
    'search': 30016,

    # messages
    'error':            30600,
    'unknown_error':    30601,
    'no_results':       30603,
}

xbmc = modules['__main__'].xbmc
addon = modules['__main__'].addon

ERROR = 0
WARN = 1
INFO = 2
DEBUG = 3
TRACE = 4

loglevel = int(addon.getSetting('loglvl'))


def show_message(msg, title=None, icon=None):
    if title is None:
        title = addon.getAddonInfo('name')
    if icon is None:
        icon = addon.getAddonInfo('icon')

    xbmc.executebuiltin(
        'Notification({title}, {msg}, 3000, {icon})'.format(**locals()))


def show_error_message(result=None, title=None):
    if title is None:
        title = get_string('error')
    if result is None:
        result = get_string('unknown_error')
    show_message(result, title)


def get_string(string_key):
    if string_key in STRINGMAP:
        string_id = STRINGMAP[string_key]
        string = addon.getLocalizedString(string_id).encode('utf8')
        log('%d translates to %s' % (string_id, string), DEBUG)
        return string
    else:
        log('String is missing: ' + string_key, DEBUG)
        return string_key


def get_user_input(title, default=None, hidden=False):
    if default is None:
        default = u''

    result = None
    keyboard = xbmc.Keyboard(default, title)
    keyboard.setHiddenInput(hidden)
    keyboard.doModal()

    if keyboard.isConfirmed():
        result = keyboard.getText()

    return result


def build_url(d):
    return argv[0] + '?' + urlencode(d)


def get_params():
    return dict(parse_qsl(argv[2][1:]))


def log(msg, lvl=0):
    if loglevel >= lvl:
        log_msg = u'[{0}] {1} : {2}'.format(
            addon.getAddonInfo('id'), stack()[1][3], msg)
        xbmc.log(log_msg.decode('utf8'), xbmc.LOGNOTICE)
