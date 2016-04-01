# coding: utf-8

# browsepy: Extendable file browser for Pythonista<br>
# [browsepy apps]: https://github.com/Vik2015/browsepy/apps/

import ui
import os
import sys
import json
import shutil
import console
import warnings
import bz2, base64

appsfn  = "apps.json"
appsdir = "apps"

if not os.path.exists(appsfn):
    with open(appsfn, "w") as fp:
        fp.write('{"text_viewer": [".py", ".txt", ".md"]}')

with open(appsfn) as fp:
    appnames = json.load(fp)

if not os.path.exists(appsdir):
    os.mkdir(appsdir)
    with open(os.path.join(appsdir, "__init__.py"), "w"):
        pass

import apps
def reload_all(mod, name):
    reload(mod)
    for mod in sys.modules:
        if mod.startswith("{}.".format(name)):
            rmod = sys.modules[mod]
            if rmod:
                reload(rmod)

reload_all(apps, "apps")

apps = {}
_apps = __import__("apps", fromlist=[str(i) for i in appnames.keys()])
for name, exts in appnames.items():
    app = getattr(_apps, name, None)
    if not app:
        warnings.warn("App {} not found".format(name))
        continue 
    apps[app.App] = exts

def decompress(str):
    return bz2.decompress(base64.decodestring(str))
TEMPLATES = {
    "ui": "#coding: utf-8\n\nimport ui\n\n",
    "pyui": decompress('QlpoOTFBWSZTWQvBkE0AAFbfgBAAUGVm0DCAEQq/r57KIACSEKankm2hqajTGiaYmJtMoMUp+qNl\nGaJpp6jQYINMkxI3CjN41Wn053q9PAhqkiHRkYmNDb0HIMCyCrKKSKAMFyr4JDYSRKwkWMDt5s9p\nNB05A6DAcB7AFmXnKEsOvqYkG1HKEbj8q7ylMqmg5qUhNcaegfJw+Hmxz1iYk4hWxDZ0RUBsM6b1\nMJqwVbpsUOEY6/xdyRThQkAvBkE0\n'),
    "bscene": decompress('QlpoOTFBWSZTWXu8LqUAAMnfgERQSHdjEAQCDAC/79/gMAFa2tWhKQnqNT9U2hGjQeoBoA0GgKn6\nmUxGjIGmIAAEihTBAaGIAANDSSQeqWUuVbocomVwZBkidAk0g3nvDDQKshdJxl4OjDutP0ior64d\n3U9fUI+2fCmcLgVGU3JU+Vc7fljhoeouLtSLCbfEFgYzEahpQHqUZRAEkyEyMkVKdhAjaOBjT8+l\nhcX6wsomMStpV7Pn4+WsfiIPl1nfBlsMGPBCAnO4WamZZLIzdTuxUyFAcJ7rv1hhsYssvc1wyFom\nyAOg83v05WIHZHGRdiYvMIgphWrCsRgxnBHgV4U/YNsUD7TFq1OKGRCFqJvGkFtqILg2sNHShpEh\n2c/cRaI2UzVeeYmhKAxlBW+qGWI0k8IgxhJounjUkWUQsmhMRIjqCqoyI/xdyRThQkHu8LqU\n'),
    "lscene": decompress('QlpoOTFBWSZTWejaA3sAAYrfgEQQSPd1UikGHgC/79/gQAJaxzNS7u4SKRoJp6k9E2phqPSGmmho\nZpNBKaTQmk9RtVPUeUzU8UyaGRk0ejUGIVA9RoDIAAAADQSp6Uyj1NB6mhoAA0AABySenmwEonRZ\nraEM70oMQrLBpTKRBJCJJ8OHSs7GgR3hHjioOjSVlrM7mUelFMz51wshdCmeflZLT2fKr3m/7e8u\ntz21xFK51J5SrjZPNF/eLWmnaqlDatCDHEal18+Q58L4kiksKt30ynQjJUVuctkuPgpzUQmr02iK\n7KnetVbHg0d5kTzbnRZhbGHuIKmHZIdcEDFYWiIXWTDohUDBUEgroU7wJICItQzUIhCkZFNCdM+B\n5CWOh/rZIPbxh1cjeeWawHkUqkRDkMFXkz4e0xiRIb1o54MdVGum5BwDjZO3rH75ZmmxkrtRXH6R\nVATJMgQe3ZfsvZOHHUcF1l1pBRJ1M5dDlw2zTFyQwb6sHcalrcGhMfjKmQajU1mEGmGWGENvpHZc\nGdBVag6v14aBNob87pCzsGBZaUE7juySeNYwdatFDaNRATYmE6yIXdPZBvhoEZuM45Cb7WS/xQgL\nS9yVtNpiMoW4atUZhU9WjTvLRUYSQbqwZGHVQKBSziU5SDswSSKRISmArkcb5FSBAygqDBA1zm0e\nk6wRMtkcykkA0zr0VGca5jITwCo3MLM0lWGcGeVkwWTNG7EtRD5UHcMgh6ScnO3r7FAgm/xdyRTh\nQkOjaA3s\n')
}

class Delegate(object):
    def __init__(self):
        self.curpath = os.getcwd()
    
    def tableview_did_select(self, tableview, section, row):
        # Called when a row was selected.
        if tableview.editing: return
        name = tableview.data_source.items[row]
        abspath = os.path.abspath(os.path.join(self.curpath, name))
        if name.endswith("/"):
            _name = name[:-1]
            if os.path.isdir(abspath):
                self.update(tableview, abspath)
        else:
            if os.path.isfile(abspath):
                _, ext = os.path.splitext(abspath)
                for App, exts in apps.items():
                    if ext in exts:
                        return App(view, abspath)
    
    def update(self, tableview, abspath):
        lst = self.getDirListing(abspath)
        if lst:
            self.curpath = abspath
            tableview.data_source.items = lst.items
            tableview.superview.name = os.path.split(self.curpath)[-1]

    def getDirListing(self, curpath, folders_only=False):
        try:
            all = os.listdir(curpath)
        except OSError:
            return
        folders = [i + "/" for i in all if os.path.isdir(
                                        os.path.join(curpath, i)
                                        )]
        files   = [i for i in all if os.path.isfile(
                                        os.path.join(curpath, i)
                                        )]
        if folders_only:
            all = ["../"] + folders
        else:
            all = ["../"] + folders + files
        lst = ui.ListDataSource(all)
        lst.font = ('Courier', 18)
        return lst

class MDelegate(Delegate):
    def getDirListing(self, curpath):
        return Delegate.getDirListing(self, curpath, True)

class NDelegate (object):
    def __init__(self, pview):
        self.pview = pview
    
    def getname(self):
        return console.input_alert("Enter name")
    
    @ui.in_background
    def tableview_did_select(self, tableview, section, row):
        fname = self.getname()
        path = os.path.join(table.delegate.curpath, fname)
        pypath = path if path.endswith(".py") else path + ".py"
        if os.path.exists(path): return error("Name already taken")
        if row == 0:
            # New folder
            os.mkdir(path)
            ui.delay(self.pview.close, 0.1)
        elif row == 1:
            # New file
            with open(path, "w"): pass
        elif row == 2:
            # File with ui
            with open(pypath, "w") as fp:
                fp.write(TEMPLATES["ui"])
            uifn = pypath + "ui"
            with open(uifn, "w") as fp:
                fp.write(TEMPLATES["pyui"])
        elif row == 3:
            # Scene with layers
            with open(pypath, "w") as fp:
                fp.write(TEMPLATES["lscene"])
        elif row == 4:
            # Basic scene
            with open(pypath, "w") as fp:
                fp.write(TEMPLATES["bscene"])
        
        table.delegate.update(table, table.delegate.curpath)

def toggleEditMode(table):
    def wrapper(sender):
        editing = not table.editing
        table.editing = editing
        sender.title = ["Edit", "Done"][int(editing)]
        enableButtons(editing)
    
    return wrapper

def enableButtons(enabled):
    view["rbutton"].enabled = enabled
    view["dbutton"].enabled = enabled
    view["mbutton"].enabled = enabled

def error(msg):
    console.alert(msg, button1="Ok", hide_cancel_button=True)

@ui.in_background
def moveFiles(sender):
    rows = table.selected_rows
    if "../" in rows:
        return error("Can't move current folder")
    elif not rows:
        return error("Select items to move")
    mview = ui.View()
    mview.name = "Choose location"
    mtable = ui.TableView()
    mtable.flex = "WH"
    mtable.delegate = MDelegate()
    mtable.data_source = mtable.delegate.getDirListing(
                                mtable.delegate.curpath)
    
    def ask_rename(name):
        answer = console.alert("File named %s already exists." % name,
                               "Do you want to replace it?",
                               "Yes",
                               "No",
                               "Rename",
                               True)
        return answer
    
    @ui.in_background
    def choose_location(sender):
        root = mtable.delegate.curpath
        fns = [table.data_source.items[i[1]] for i in rows]
        cpaths = [os.path.join(table.delegate.curpath, i) for i in fns]
        npaths = [os.path.join(root, i) for i in fns]
        for path, cpath in zip(npaths, cpaths):
            if os.path.exists(path):
                rename = ask_rename(os.path.split(path)[-1])
                if rename == 2:
                    while os.path.exists(path):
                        root, fn = os.path.split(path)
                        path = os.path.join(root, "-" + fn)
                elif rename == 1:
                    continue
                if os.path.exists(path):
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        shutil.rmtree(path)
            shutil.move(cpath, path)
        ui.delay(mview.close, 0.1)
        table.delegate.update(table, table.delegate.curpath)
        toggleEditMode(table)(view.right_button_items[0])
    
    mview.add_subview(mtable)
    mview.right_button_items = [
        ui.ButtonItem("Select", action=choose_location)
    ]
    mview.present("sheet")

@ui.in_background
def deleteFiles(sender):
    rows = table.selected_rows
    if not rows:
        error("Select files to remove")
    else:
        names = [table.data_source.items[i[1]] for i in rows]
        if "../" in names:
            return error("Can't remove current folder")
        answer = console.alert("Are you sure want to remove selected items?",
                               button1="Yes",
                               button2="No",
                               hide_cancel_button=True)
        if answer == 1: return
        cpath = table.delegate.curpath
        for name in names:
            fpath = os.path.join(cpath, name)
            if os.path.isdir(fpath):
                shutil.rmtree(fpath)
            else:
                os.remove(fpath)
        table.delegate.update(table, cpath)
        toggleEditMode(table)(view.right_button_items[0])

@ui.in_background
def renameFile(sender):
    rows = table.selected_rows
    if not rows:
        return error("Select a file")
    elif len(rows) > 1:
        return error("You can rename only one file at a time")
    else:
        cname = table.data_source.items[rows[0][1]]
        if cname == "../":
            return error("Can't rename current folder")
        name = console.input_alert("Enter new name")
        if name:
            cpath = table.delegate.curpath
            aname = os.path.join(cpath, name)
            if os.path.exists(aname):
                return error("Name already taken")
            acname = os.path.join(cpath, cname)
            shutil.move(acname, aname)
            table.delegate.update(table, cpath)
            toggleEditMode(table)(view.right_button_items[0])

def newItem(sender):
    pview = ui.View()
    ptable = ui.TableView()
    ptable.flex = "WH"
    ptable.data_source = ui.ListDataSource(["New folder",
                                            "New file",
                                            "Script with ui",
                                            "Scene with layers",
                                            "Basic scene"])
    ptable.delegate = NDelegate(table)
    
    sx, sy = ui.get_screen_size()
    x, y, w, h = view["nbutton"].frame
    pos = (x + (sx/2 - view.width/2) + w/2,
           y + (sy/2 - view.height/2) + h)
    pview.add_subview(ptable)
    pview.width, pview.height = 300, 150
    pview.present("popover", True, pos, True)

view = ui.load_view()

table = view["filetable"]
table.delegate = Delegate()
table.data_source = table.delegate.getDirListing(table.delegate.curpath)
table.allows_multiple_selection_during_editing = 1
enableButtons(False)

view.right_button_items = [
    ui.ButtonItem("Edit", action=toggleEditMode(table))
]
view.name = os.path.split(table.delegate.curpath)[-1]

view.present("sheet")