# coding: utf-8

# https://forum.omz-software.com/topic/2717/pythonista-module/44

"""Methods relating to extensions."""

import appex, os, shutil, dialogs

__all__ = [
    "save",
]

def save():
    """Save an attachment"""
    if appex.is_running_extension():
        sFp = appex.get_file_path()
        if sFp:
            dialogs.hud_alert('Saving...')
            comps = __file__.split(os.sep)
            doc_path = os.sep.join(comps[:comps.index('Documents')+1])
            with open(sFp, 'rb') as f1:
                with open(doc_path + '/' + os.path.basename(sFp), 'wb') as f2:
                    shutil.copyfileobj(f1, f2, length=512*1024)
            dialogs.hud_alert('Saved')
            appex.finish()
