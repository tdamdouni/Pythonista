# coding: utf-8
import ui, time

view_main = ui.load_view()
lbl = view_main["lbl_time"]
view_main.present("sheet")
time = 4
#the action is this because it takes a function, what this does is calls it with a delay. 
view_main["btn_start"].action = lambda sender: ui.delay(decrement, 1)
#This is still here because ui.delay takes a function. 
def decrement():
    global time
    if time > 0:
        time -= 1
        lbl.text = str(time)
        ui.delay(decrement, 1)