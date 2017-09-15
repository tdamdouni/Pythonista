# https://forum.omz-software.com/topic/4350/repeat-views/3

def snapshot(view):
  with ui.ImageContext(view.width, view.height) as ctx:
    view.draw_snapshot()
    return ctx.get_image()
