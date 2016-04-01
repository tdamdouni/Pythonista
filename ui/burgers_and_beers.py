# https://github.com/cclauss/Pythonista_ui/blob/master/burgers_and_beers.py

#!/usr/bin/env python
# coding: utf-8

# See: https://github.com/ChamGeeks/ChamonixHackathon2015

import console, requests, ui

url_root = 'https://chamonix-hackathon-2015.herokuapp.com/'
#map_url_fmt = 'http://maps.apple.com/?q={name}&sll={location[lat]},{location[long]}'
#map_url_fmt = 'http://maps.google.com/?daddr={location[lat]},{location[long]}'
map_url_fmt = 'http://maps.google.com/?q={location[lat]},{location[long]}'
offers_fmt = '{extra_info}: {type} on {day}s from {starts} til {ends}'

def get_dataset(dataset='offers'):
    try:
        return requests.get(url_root + dataset).json()
    except requests.ConnectionError as err:
        console.hud_alert('No Internet access!!')
        exit(err)

def get_bars_dict():
    return {x['name']: x for x in get_dataset('bars')}

def get_offers_for_bar(bar_name='Bard Up'):
    return (x for x in get_dataset('offers') if x['bar']['name'] == bar_name)

def get_ui_image(image_url):
    img = ui.Image.from_data(requests.get(image_url).content)
    return img.with_rendering_mode(ui.RENDERING_MODE_ORIGINAL) if img else None

def make_web_view_from_url(url):
    web_view = ui.WebView()
    web_view.load_url(url)
    return web_view

class BarView(ui.View):
    def __init__(self, bar_dict):
        self.name = bar_dict['name']
        self.add_subview(make_web_view_from_url(bar_dict['image_url']))
        self.add_subview(make_web_view_from_url(map_url_fmt.format(**bar_dict)))
        self.add_subview(self.make_offers_view(self.name))

    def layout(self):
        x, y, w, h = self.bounds
        half_w, half_h = w / 2, h / 2
        self.subviews[0].frame = x, y, half_w, half_h       # image
        self.subviews[1].frame = half_w, y, half_w, h       # map
        self.subviews[2].frame = x, half_h, half_w, half_h  # offers

    def make_offers_view(self, bar_name):
        table_view = ui.TableView()
        table_list = (offers_fmt.format(**x).replace('None: ', '') for x in
            get_offers_for_bar(bar_name))
        table_view.data_source = lds = ui.ListDataSource(table_list)
        lds.font = ('<system-bold>', 10)
        table_view.row_height = 20
        table_view.delegate = self
        return table_view

    def tableview_did_select(self, tableview, section, row):
        console.hud_alert(tableview.data_source.items[row])

class BarsView(ui.View):
    def __init__(self):
        self.name = 'Chamonix Bars'
        self.bars_dict = get_bars_dict()
        for bar_name in sorted(self.bars_dict):
            self.add_subview(self.make_bar_button(bar_name))
        ui.NavigationView(self).present(orientations=['landscape'])
        self.navigation_view.name = 'Chamonix Hackathon 2015'

    def button_pressed(self, sender):
        self.navigation_view.push_view(BarView(self.bars_dict[sender.name]))

    def layout(self):
        w, h = self.bounds[2] / 4, self.bounds[3] / 2
        for i, subview in enumerate(self.subviews):
            subview.frame = i % 4 * w, i / 4 * h, w, h

    def make_bar_button(self, bar_name='Bard Up'):
        button = ui.Button()
        button.action = self.button_pressed
        button.font = ('<system-bold>', 24)
        button.name = button.title = bar_name
        button.background_image = get_ui_image(self.bars_dict[bar_name]['image_url'])
        return button

BarsView()