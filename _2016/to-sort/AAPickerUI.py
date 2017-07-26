# coding: utf-8

# https://gist.github.com/KainokiKaede/ac96eed08d55ea20e364

import ui
import clipboard
from console import hud_alert


aa_list = ["٩( 'ω' )و",
             '₍₍⁽⁽(ી(◔‿ゝ◔)ʃ)₎₎⁾⁾',
             '(◔‸◔ )',
             '☝( ◠‿◠ )☝',
             '（ ・ワ・）',
             '（◞‸◟）',
             '_(:3 」∠)_',
             ]


def button_tapped(sender):
    '@type sender: ui.Button'
    clipboard.set(sender.title)
    hud_alert('Copied')

view = ui.load_view('AAPickerUI')
view.present('sheet')

for i, aa in enumerate(aa_list):
    view['button{0:d}'.format(i+1)].title = aa

