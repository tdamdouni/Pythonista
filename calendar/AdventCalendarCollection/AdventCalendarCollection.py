# https://github.com/Omega014/AdventCalendarCollection

import json
import os
from datetime import datetime

import ui

import scraper


class AdventCalendarCollection (object):
    def __init__(self):
        self.view = ui.load_view('AdventCalendarCollection')
        self.view.background_color = "#ffebd5"
        self.view.present('fullscreen')
        self.view.name = 'AdventCalendarCollection'
        self.reload_data(None)
        self.change_today_bg_color()
        
    def refresh(self, sender):
        scraper.main()
        self.reload_data(None)

    def reload_data(self, sender):
        filepath = os.path.join(os.path.realpath('./'), 'registrations.json')
        with open(filepath, 'r') as f:
            registrations = json.load(f)
        # jsonに保存する時点でdayだけ保存しても良いかもなぁ...
        for data in registrations:
            day = data['date'].split('-')[-1]
            if day[0] == '0':
                day = day[1]
            title = data['title']
            self.view['textview'+day].text = title
    
    def change_today_bg_color(self):
        # 今日の日だけカレンダーの背景に色をつける
        today_datetime = datetime.now()
        if today_datetime.month == 12:
            today = str(today_datetime.day)
            self.view['textview'+today].background_color = '#ffd9d9'


AdventCalendarCollection()
