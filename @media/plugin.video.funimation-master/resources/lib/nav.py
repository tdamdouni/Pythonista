# -*- coding: utf-8 -*-
import xbmcgui
import xbmcplugin
from sys import modules, argv

from .models import Show, Video

common = modules['__main__'].common
api = modules['__main__'].api
handle = int(argv[1])

_ = common.get_string

# static menu items
menus = (
    {'label': _('browse_shows'),      'get': 'shows'},
    {'label': _('browse_latest'),     'get': 'shows', '_filter': 'latest'},
    {'label': _('browse_simulcasts'), 'get': 'shows', '_filter': 'simulcast'},
    {'label': _('browse_featured'),   'get': 'shows', '_filter': 'featured'},
    {'label': _('browse_genre'),      'get': 'genres'},
    {'label': _('browse_alpha'),      'get': 'alpha'},
    {'label': _('search'),            'get': 'search'},
)


def list_menu():
    params = common.get_params()
    if params.get('get'):
        generate_menu(params)
    else:
        for menu in menus:
            add_list_item(menu)
    if handle > -1:
        xbmcplugin.endOfDirectory(handle)


def generate_menu(query):
    action = query['get']
    if action == 'shows':
        xbmcplugin.setContent(handle, 'tvshows')
        if query.get('_filter') == 'genre':
            results = api.get_shows_by_genre(query['label'])
        elif query.get('_filter') == 'latest':
            results = api.get_latest()
        elif query.get('_filter') == 'simulcast':
            results = api.get_simulcast()
        elif query.get('_filter') == 'featured':
            results = api.get_featured()
        else:
            results = api.get_shows(first_letter=query.get('alpha'))
        add_shows(results)

    elif action == 'videos':
        xbmcplugin.setContent(handle, 'episodes')
        results = api.get_videos(query['show_id'])
        add_videos(results)

    elif action == 'search':
        results = api.search(common.get_user_input('Search'))
        add_shows(results)
        add_videos(results)

    elif action == 'genres':
        for genre in api.get_genres():
            add_list_item({'label': genre, 'get': 'shows', '_filter': 'genre'})

    elif action == 'alpha':
        for i in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            add_list_item({'label': i, 'get': 'shows', 'alpha': i})
        add_list_item({'label': '#', 'get': 'shows', 'alpha': 'non-alpha'})


def add_videos(results):
    if results.get('episodes'):
        results = results.get('episodes')
    if results.get('videos') is not None:
        total = len(results.get('videos'))
        for item in results.get('videos'):
            video = Video(**item)
            add_list_item(video.query, video, total)


def add_shows(results):
    if isinstance(results, dict):
        results = results.get('shows')
    if results is not None:
        total = len(results)
        for item in results:
            show = Show(**item)
            add_list_item(show.query, show, total)
    else:
        add_list_item(_('no_results'))


def add_list_item(query, item=None, total=0):
    if item is None:
        item = query

    li = new_list_item(item)
    is_folder = True
    if item.get('video_url'):
        url = item.get('video_url')
        is_folder = False
        li.setProperty('Is_playable', 'true')
        li.addStreamInfo('video', item.stream_info)
    else:
        url = common.build_url(query)
    xbmcplugin.addDirectoryItem(handle, url, li, is_folder, total)


def new_list_item(item):
    get = item.get
    li = xbmcgui.ListItem(get('label'), get('label2'), get('icon'),
                          get('thumbnail'))
    if get('info'):
        li.setInfo('video', get('info'))

    return li
