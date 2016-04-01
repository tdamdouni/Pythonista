# http://omz-forums.appspot.com/pythonista/post/5227475999129600
# coding: utf-8
import ui
import motion
import sys

main_view = None

def motion_color(): 
    if not main_view.on_screen : 
        motion.stop_updates()
        sys.exit(999)
    color=  motion.get_attitude()
    main_view.background_color = color
    ui.delay(motion_color, .1)

if __name__ == '__main__':
    v = ui.View()
    main_view = v
    motion.start_updates()
    ui.delay(motion_color, .1)
    v.present()