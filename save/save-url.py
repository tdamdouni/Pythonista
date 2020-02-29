# coding: utf-8

# https://github.com/khilnani/pythonista-scripts/blob/master/extensions/save-url.py

from __future__ import print_function
import clipboard, datetime, console, appex
import json, re, os, sys, shutil, urllib2

###########################################

# share safe documents dir location
BASE_DIR = os.getcwd().split('Documents')[0] + 'Documents'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONF_FILE = os.path.join(SCRIPT_DIR, 'save.conf')

GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

###########################################

def get_save_dir():
    save_dir = ''
    with open(CONF_FILE, 'r') as conf_file:
        try:
            config = json.load(conf_file)
            save_dir = config['TEXT']
            return save_dir
        except Exception as e:
            print('Config load error:')
            print(e)
            sys.exit()
    return save_dir

###########################################

def main():
    
    # get text from app share or clipboard
    if appex.is_running_extension():
        text = appex.get_url()
    else:
        text = clipboard.get().strip()

    # get url
    url = ''
    try:
        url = [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(text) ][0]
    except:
        url = console.input_alert("URL", "", url)
    if url:
        if not 'http' in url:
            url = 'http://' + url
    else:
        console.hud_alert('No URL found.')
        sys.exit()

    sel = console.alert('Save: %s ?' % url, button1='File', button2='Clipboard')

    # get url info
    url_items = url.split("?")[0].split("/")
    # if url ends with /, last item is an empty string
    file_name = url_items[-1] if url_items[-1] else url_items[-2]
    try:
        content = urllib2.urlopen(url).read()
    except Exception as e:
        console.alert(e.message)
        sys.exit()

    if sel == 1:
        # get file save info
        save_dir_name = get_save_dir()
        save_dir = os.path.join(BASE_DIR, save_dir_name)
        file_path = os.path.join(save_dir, file_name)
        try:
            # check dirs and save
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            with open(file_path, 'w') as f:
                f.write(content)
                f.close()
            # wrapup
            console.alert('Saved to: %s' % file_path, hide_cancel_button=True, button1='OK')
        except Exception as e:
            console.alert(str(e), button1='OK',hide_cancel_button=True)
    elif sel == 2:
        clipboard.set(content)


    if appex.is_running_extension():
        appex.finish()

###########################################

if __name__ == '__main__':
    main()
