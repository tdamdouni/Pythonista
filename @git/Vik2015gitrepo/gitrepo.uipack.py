# -*- coding: utf-8 -*-
###############################################################################
# This is a self-extracting UI application package for gitrepo.
# Run this script once to extract the packaged application.
# The files will be extracted to gitrepo.py and gitrepo.pyui.
# Make sure that these files do not exist yet.
# To update from an older version, move or delete the old files first.
# After extracting, the application can be found at gitrepo.py.
# This bundle can be deleted after extraction.
###############################################################################
# Packaged using PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
###############################################################################

import console, os.path

NAME     = "gitrepo"
PYFILE   = """# coding: utf-8

import clipboard, console, requests, ui, urlparse, zipfile, re, os, string
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO  import StringIO

class Delegate (object):
    def __init__(self):
        self.selected_item = None
    
    def tableview_did_select(self, tableview, section, row):
        self.selected_item = tableview.data_source.items[row]
        tableview.superview.close()

repolink     = "https://github.com/{}/{}/archive/{}.zip"
gistslink    = "https://api.github.com/users/{}/gists"
browselink   = "https://api.github.com/users/{}/repos"
releaselink  = "https://api.github.com/repos/{}/{}/releases"
parselink    = re.compile(r'<[\\S]*?page=(\\d+)>; rel="last"').search

def error_alert(msg="General error"):
    console.alert("Error", msg, "OK", hide_cancel_button=True)

def get_page_num(link_header):
    return int(parselink(link_header).group(1))

@ui.in_background
def save_zip(data, name, unzip):
    if unzip:
        io = StringIO(data)
        with zipfile.ZipFile(io) as zp:
            zp.extractall()
    else:
        with open(name + ".zip", "wb") as zp:
            zp.write(data)

@ui.in_background
def download_repo(username, repo, branch, unzip):
    url = repolink.format(username, repo, branch)
    data = requests.get(url)
    if isinstance(data, dict) and data["message"] == "Not Found":
        return error_alert("User '{}' not found".format(username))
    elif not data:
        return error_alert("Repo '{}' not found".format(repo))
    try:
        save_zip(data.content, repo, unzip)
    except Exception as err:
        return error_alert("Error downloading repo: {}".format(err))
    console.hud_alert("Done!")

@ui.in_background
def download_release(username, repo, unzip):
    url = releaselink.format(username, repo)
    data = requests.get(url).json()
    if not data:
        return error_alert("Repo '{}' has no releases".format(repo))
    elif "message" in data and data["message"] == "Not Found":
        return error_alert("Repo '{}' not found".format(repo))
    vers = sorted([i["tag_name"] for i in data])
    rview = data_view("release", vers)
    rview.present("sheet")
    rview.wait_modal()
    tapped_text = rview["rtable"].delegate.selected_item
    if tapped_text:
        for d in data:
            if d["tag_name"] == tapped_text:
                zipurl = d["zipball_url"]
                save_zip(requests.get(zipurl).content, tapped_text, unzip)
                return console.hud_alert("Done!")

@ui.in_background
def download_gist(username, gist):
    url = gistslink.format(username, gist)
    req = requests.get(url)
    data = req.json()
    req.close()
    
    info = [i for i in data if i["id"] == gist]
    if not info:
        return error_alert("Gist '{}' not found".format(gist))
    info = info[0]
    files = info["files"]
    try:
        os.mkdir(gist)
    except:
        pass
    for fpinfo in files.values():
        data = requests.get(fpinfo["raw_url"]).content
        with open(os.path.join(gist,
                  fpinfo["filename"]), "wb") as fp:
            fp.write(data)
    return console.hud_alert("Done!")

@ui.in_background
def gitdownload(button):
    index    = view["sgcontrol"].selected_index
    username = view["username"].text = view["username"].text.strip()
    reponame = view["reponame"].text = view["reponame"].text.strip()
    if '/' in reponame:
        reponame, branch = string.split(reponame, '/', maxsplit=1)
        if not branch: branch = 'master'
    else:
        branch = 'master'
    unzip    = view["dounzip"].value
    if not username:
        return error_alert("Please enter username")
    if not reponame:
        return error_alert("Please enter repo name")
    console.show_activity()
    if index == 0:
        download_repo(username, reponame, branch, unzip)
    elif index == 1:
        download_release(username, reponame, unzip)
    elif index == 2:
        download_gist(username, reponame)
    console.hide_activity()

@ui.in_background
def gitbrowse(sender):
    username = view["username"].text = view["username"].text.strip()
    if not username:
        return error_alert("Please enter username")
    index = view["sgcontrol"].selected_index
    if index == 2:
        url = gistslink.format(username)
    else:
        url = browselink.format(username)
    try:
        req  = requests.get(url)
        data = req.json()  # normally returns a list of dicts
    except requests.HTTPError as err:
        return error_alert("User '{}' not found".format(username))
    except Exception as err:
        return error_alert("Error downloading metadata: {}".format(err))
    if isinstance(data, dict) and data["message"] == "Not Found":
        return error_alert("User '{}' not found".format(username))
    finaldata = data
    if "link" in req.headers:
        pages = get_page_num(req.headers["link"])
        for lnk in range(2, pages + 1):
            link = browselink.format(username) + "?page=%d" % lnk
            req = requests.get(link)
            finaldata += req.json()
    
    if index == 2:
        nameid_dict = {}
        for fpinfo in finaldata:
            nameid_dict[", ".join(fpinfo["files"].keys())] = fpinfo["id"]
        names = nameid_dict.keys()
    else:
        names = sorted([i["name"] for i in finaldata])
        
    name  = {0: "repos", 1: "repos", 2: "gists"}[index]
    if not names:
        return error_alert("User '{}' has no {}".format(username, name))
    rview = data_view(name[:-1], names)
    rview.present("sheet")
    rview.wait_modal()
    tapped_text = rview["rtable"].delegate.selected_item
    if tapped_text:
        if index == 2:
            view["reponame"].text = nameid_dict[tapped_text]
        else:
            view["reponame"].text = tapped_text

def data_view(name, data):
    rview = ui.View(name="Choose a " + name)
    table = ui.TableView()
    table.name = "rtable"
    table.flex = "WH"
    table.data_source = ui.ListDataSource(data)
    table.data_source.delete_enabled = False
    table.delegate = Delegate()
    rview.add_subview(table)
    return rview

def segchange(sender):
    index = sender.selected_index
    if index == 2: # Gist
        view["repolabel"].text = "Gist ID:"
        view["bbutton"].title  = "Browse gists"
    else:
        view["repolabel"].text = "Repo:"
        view["bbutton"].title  = "Browse repos"

view = ui.load_view('gitrepo')
for name in 'username reponame'.split():
    view[name].autocapitalization_type = ui.AUTOCAPITALIZE_NONE
parse = urlparse.urlparse(clipboard.get().strip())
if parse.netloc in "www.github.com github.com".split():
    path = [i for i in parse.path.split("/") if i]
    if len(path) >= 2:
        view["username"].text, view["reponame"].text = path[:2]
    if len(path) >= 4:
        view["reponame"].text += '/' + path[3]

view["sgcontrol"].action = segchange
view.present('popover')
"""
PYUIFILE = """[{"class":"View","attributes":{"name":"gitrepo","background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","tint_color":"RGBA(0.000000,0.478000,1.000000,1.000000)","enabled":true,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","flex":""},"frame":"{{0, 0}, {341, 250}}","nodes":[{"class":"SegmentedControl","attributes":{"name":"sgcontrol","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","uuid":"308A3491-ABAA-43BC-8D2C-1319469FF3C9","enabled":true,"segments":"Repo|Release|Gist","flex":"LR"},"frame":"{{16, 6}, {196.5, 29}}","nodes":[]},{"class":"Label","attributes":{"font_size":20,"enabled":true,"text":"Username:","flex":"","name":"label1","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"7C45FE1B-8084-4257-A1D1-DE573BC8299A"},"frame":"{{16.5, 57.5}, {96, 35.5}}","nodes":[]},{"class":"TextField","attributes":{"uuid":"18AD549C-48DF-40CF-B008-5E2C283AD3EA","alignment":"left","autocorrection_type":"no","font_size":17,"font_name":"Avenir-Book","enabled":true,"flex":"","border_color":"RGBA(0.571429,0.571429,0.571429,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","corner_radius":2,"secure":false,"border_width":1,"border_style":3,"name":"username","spellchecking_type":"no"},"frame":"{{120.5, 57.5}, {200, 36}}","nodes":[]},{"class":"Label","attributes":{"font_size":20,"enabled":true,"text":"Repo:","flex":"","name":"repolabel","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"97359D8F-3BD5-4D8F-8711-14B4565F9601"},"frame":"{{16.5, 102}, {96, 35}}","nodes":[]},{"class":"TextField","attributes":{"name":"reponame","alignment":"left","autocorrection_type":"no","font_size":17,"font_name":"Avenir-Book","enabled":true,"flex":"","border_color":"RGBA(0.571429,0.571429,0.571429,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","corner_radius":2,"secure":false,"uuid":"7BFD908D-CA67-4976-94DD-5CF0DB5EC360","border_style":3,"border_width":1,"spellchecking_type":"no"},"frame":"{{120, 101.5}, {200, 36}}","nodes":[]},{"class":"Button","attributes":{"font_size":16,"enabled":true,"flex":"","font_bold":false,"name":"dbutton","corner_radius":9,"border_color":"RGBA(0.244898,0.520408,0.857143,1.000000)","border_width":1,"action":"gitdownload","uuid":"7C58793E-E2CA-4724-B2FC-3E779FD71890","title":"Download"},"frame":"{{16.5, 201}, {96, 31}}","nodes":[]},{"class":"Label","attributes":{"font_size":20,"enabled":true,"text":"Unzip archive:","flex":"","name":"label3","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"3A801AA2-D086-48E9-9262-E9880135E8EA"},"frame":"{{16.5, 145}, {137, 35}}","nodes":[]},{"class":"Switch","attributes":{"enabled":true,"flex":"","name":"dounzip","value":true,"alpha":1,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","uuid":"40756EA8-214B-4247-9A47-F7D519C0BE88"},"frame":"{{161.5, 147}, {51, 31}}","nodes":[]},{"class":"Button","attributes":{"font_size":16,"enabled":true,"flex":"","font_bold":false,"name":"bbutton","corner_radius":9,"border_color":"RGBA(0.244898,0.520408,0.857143,1.000000)","border_width":1,"action":"gitbrowse","uuid":"127F82F8-97A9-4835-AD60-DF5FCDC942E3","title":"Browse repos"},"frame":"{{139, 201}, {119.5, 31}}","nodes":[]}]}]
"""

def fix_quotes_out(s):
    return s.replace("\\\"\\\"\\\"", "\"\"\"").replace("\\\\", "\\")

def main():
    if os.path.exists(NAME + ".py"):
        console.alert("Failed to Extract", NAME + ".py already exists.")
        return
    
    if os.path.exists(NAME + ".pyui"):
        console.alert("Failed to Extract", NAME + ".pyui already exists.")
        return
    
    with open(NAME + ".py", "w") as f:
        f.write(fix_quotes_out(PYFILE))
    
    with open(NAME + ".pyui", "w") as f:
        f.write(fix_quotes_out(PYUIFILE))
    
    msg = NAME + ".py and " + NAME + ".pyui were successfully extracted!"
    console.alert("Extraction Successful", msg, "OK", hide_cancel_button=True)
    
if __name__ == "__main__":
    main()
