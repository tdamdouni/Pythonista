# coding: utf-8

# http://pastebin.com/iqbP4Rsd
# https://doc-0g-bk-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/2oddn3ejvopfaffts9s68seehpcde3c6/1456862400000/07368093497126647940/*/0ByA_-5jq6vEYR0R4QXdoNWhRREU?e=download

# https://forum.omz-software.com/topic/2852/sending-touch-events-to-multiple-widgets/5

# autoscroll
 
import ui
import threading
from datetime import datetime
 
nick = 'Leva7'[:15]
smMode = 1
kbrd_up = False
prev_sz = 0
 
class CloseView(ui.View):
    def __init__(self):
        self.touches = 0
        self.prev_touch = None
        self.curr_touch = None
    def count_drop(self):
        self.touches = 0
    def allow_scroll(self):
        self.touch_enabled = False
    def touch_began(self,touch):
        pass
    def touch_ended(self,touch):
        v['tx1'].end_editing()
        self.touch_enabled = True
 
class tx1dlg(object):
    def textview_did_begin_editing(self, tx1):
        global kbrd_up
        def mv_up():
            txMain.height = v['kbrd_view'].height = 197
            v['tx1'].y = v['btSm'].y = 275
            v['smiles'].y -= 216
            v['btS'].y = 311
        ui.animate(mv_up, 0.26)
        kbrd_up = True
   
    def textview_did_end_editing(self, tx1):
        global kbrd_up
        def mv_dw():
            txMain.height = v['kbrd_view'].height = 413
            v['tx1'].y = v['btSm'].y = 491
            v['smiles'].y += 216
            v['btS'].y = 527
        ui.animate(mv_dw, 0.26)
        kbrd_up = False
       
class txMdlg(object):
    def textview_did_change(self, txMain):
        pass
 
def close_app(sender):
    v.close()
 
def auto_scroll():
    def do_scroll():
        tx = txMain.content_offset[1]
        sz = txMain.content_size[1]
        hg = txMain.height
        txMain.content_offset = (0, sz - hg)
    ui.animate(do_scroll, 0.00001)
 
def msg_in(sender):
    msg = v['tx1'].text
    if msg != '' and msg != '\n':
        time = datetime.now()
        if txMain.text != '':
            txMain.text += '\n'
        txMain.text += '[{}] {}: '.format(time.strftime('%H:%M'),nick)
        txMain.text += msg
        txMain.text += ''
        v['tx1'].text = ''
        ui.delay(auto_scroll, 0.001)
 
def smile(sender):
    global smMode, kbrd_up
    if not kbrd_up:
        if smMode == 1:
            def sm_pop():
                v['smiles'].hidden = False
                v['smiles'].y = 420
            ui.animate(sm_pop, 0.1)
        else:
            def sm_fade():
                v['smiles'].y = 491
            ui.animate(sm_fade, 0.1)
            v['smiles'].hidden = True
    else:
        if smMode == 1:
            def sm_pop1():
                v['smiles'].y = 204
            v['smiles'].hidden = False
            ui.animate(sm_pop1, 0.1)
        else:
            def sm_fade1():
                v['smiles'].y = 275
            ui.animate(sm_fade1, 0.1)
            v['smiles'].hidden = True
    smMode = -smMode
 
def smile_add(sender):
    v['tx1'].text += sender.title
   
def kbrd_dismiss(sender):
    v['tx1'].end_editing()
v = ui.load_view('Chat')
txMain = v['txMain']
v.name = 'Chat with {0}'.format(nick)
v['smiles'].hidden = True
v['tx1'].delegate = tx1dlg()
txMain.selectable = False
txMain.delegate = txMdlg()
 
v['btPrs'].title = ' ' + nick
v['btPrs'].width = 38 + 9*len(nick)
 
v.present(orientations=['portrait'], hide_title_bar=True)
