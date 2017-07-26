# coding: utf-8

# https://gist.github.com/KainokiKaede/ee9445de409a1a34968b

import ui
import time

tapped_time = []

def calc_bpm():
    # I decided not to use the first and the last time measurement.
    # So the list must have at least 4 items to calculate BPM.
    if len(tapped_time) < 4:
        return 0.0
    else:
        interval = [x-y for x, y in zip(tapped_time[2:-1], tapped_time[1:-2])]
        return 60.0 * float(len(interval))/float(sum(interval))

def button_tapped(sender):
    tapped_time.append(time.time())
    sender.superview['label'].text = str(int(round(calc_bpm())))

view = ui.load_view('Heartbeat')
view.present('sheet')

