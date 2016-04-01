#coding: utf-8
import ui
import os
import json
import console

def save(fn, data):
    with open(fn, "w") as fp:
        json.dump(data, fp)

def load(fn):
    with open(fn, "r") as fp:
        data = json.load(fp)
    final = {}
    for appname, exts in data.items():
        final[appname] = [i for i in exts]

    return final

appsfn  = "apps.json"
appsdir = "apps"

if not os.path.exists(appsfn):
    save(appsfn, {})

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

apps = load(appsfn)

# Functions
@ui.in_background
def error(msg):
    console.alert("Error", msg)

def makeView(name):
    view = ui.View()
    view.name = name
    view.bg_color = 0.89

    return view

def makeButton(title, frame):
    button = ui.Button()
    button.frame = frame
    button.title = title
    button.border_width = 1
    button.corner_radius = 5
    button.border_color = 0.9
    button.bg_color = 1
    button.tint_color = 0
    button.font = ("Courier", 15)

    return button

def makeLabel(name, frame):
    label = ui.Label()
    label.text = name
    label.frame = frame
    label.font = ("Courier", 18)

    return label

def makeExtTable(appname, exts, y):
    lst = ExtList(appname, [i for i in exts])
        
    table = ui.TableView()
    table.name = "extview"
    table.frame = (10, y, table.frame[2] - 5, 200)
    table.flex = "W"
    table.corner_radius = 10
    table.data_source = lst

    return table

def makeTable():
    lst = ListDataSource(apps.keys())
    delegate = Delegate()

    table = ui.TableView()
    table.y = 55
    table.flex = "WH"
    table.data_source = lst
    table.delegate = delegate

    return table

def getInfo(mod, appname):
    version = getattr(mod, "__version__", "Unknown")
    author  = getattr(mod, "__author__", "Unknown")
    appname = appname
    exts    = apps[appname]

    return version, author, appname, exts

def showInfo(appname):
    appname = str(appname)
    try:
        mod  = getattr(__import__("apps", fromlist=[appname]), appname)
    except AttributeError:
        return error("App {} not found".format(appname))
    version, author, appname, exts = getInfo(mod, appname)

    view = makeView(appname)

    verlabel = makeLabel("Version: {}".format(version),
                             (10, 10, 500, 32))
    autlabel = makeLabel("Author:  {}".format(author),
                             (10, 52, 500, 32))
    extlabel = makeLabel("Supported file formats: ",
                             (10, 94, 500, 32))
    table    = makeExtTable(appname, exts, 136)
    
    nbutton  = makeButton("Add", (10, 368, 80, 32))
    nbutton.action = newExt(table, appname)

    view.add_subview(verlabel)
    view.add_subview(autlabel)
    view.add_subview(extlabel)
    view.add_subview(table)
    view.add_subview(nbutton)
    view.present("sheet")

def newApp(table):
    @ui.in_background
    def wrapper(sender):
        appname = console.input_alert("Enter application's name")
        if appname:
            if appname in table.data_source.items:
                return error("App already in list")
            apps[appname] = []
            table.data_source.items.append(appname)

    return wrapper

def newExt(table, appname):
    @ui.in_background
    def wrapper(sender):
        ext = console.input_alert("Enter extension")
        if ext:
            if not ext.startswith("."):
                ext = "." + ext
            if ext in table.data_source.items:
                return error("Extensions already in list")
            apps[appname].append(ext)
            table.data_source.items.append(ext)

    return wrapper

@ui.in_background
def saveData(sender):
    save(appsfn, apps)

# Classes
class Delegate (object):
    def tableview_did_select(self, tableview, section, row):
        name = tableview.data_source.items[row]
        showInfo(name)

class ListDataSource (ui.ListDataSource):
    def tableview_delete(self, tv, section, row):
        self.reload_disabled = True
        name = self.items[row]
        del self.items[row]
        self.reload_disabled = False
        tv.delete_rows([row])
        del apps[name]

class ExtList (ui.ListDataSource):
    def __init__(self, appname, items=None):
        ui.ListDataSource.__init__(self, items)
        self.appname = appname
    
    def tableview_delete(self, tv, section, row):
        self.reload_disabled = True
        name = self.items[row]
        del self.items[row]
        self.reload_disabled = False
        tv.delete_rows([row])
        apps[self.appname].remove(name)

# Main frame
view = makeView("App Manager")

nbutton = makeButton("Add", (10, 10, 80, 32))
dbutton = makeButton("Download", (100, 10, 111, 32))
sbutton = makeButton("Save", (221, 10, 80, 32))
table   = makeTable()

nbutton.action = newApp(table)
sbutton.action = saveData

view.add_subview(nbutton)
view.add_subview(dbutton)
view.add_subview(sbutton)
view.add_subview(table)
view.present("sheet")
