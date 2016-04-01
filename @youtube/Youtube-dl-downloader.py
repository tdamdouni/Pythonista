# coding: utf-8
# author: Shaun Hevey
# youtube-dl downloader is used to download youtube_dl and patch it to work in Pythonista.
# Replace function came from http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
# Download file was adapted from Python file downloader (https://gist.github.com/89edf288a15fde45682a)

import console
import os
import requests
import shutil
import tempfile
import time
import ui
import zipfile

youtubedl_dir = 'youtube_dl'
youtubedl_location = './site-packages/'
backup_location = './backup/youtube_dl/'
youtubedl_downloadurl = 'https://github.com/rg3/youtube-dl/archive/master.zip'
youtubedl_unarchive_location = './youtube-dl-master/'
files_to_change = [('utils.py','import ctypes','#import ctypes'),
                   ('utils.py','import pipes','#import pipes'),
                   ('YoutubeDL.py','self._err_file.isatty() and ',''),
                   ('downloader/common.py','(\'\r\x1b[K\' if sys.stderr.isatty() else \'\r\')','\'r\''),
                   ('downloader/common.py','(\'\r\x1b[K\' if sys.stderr.isatty() else \'\r\')','\r'),
                   ('extractor/common.py',' and sys.stderr.isatty()','')]

def backup_youtubedl(sender):
    console.show_activity('Checking for youtube-dl')
    if os.path.isdir(youtubedl_location+youtubedl_dir):
        console.show_activity('Backing up youtube-dl')
        if not os.path.exists(backup_location):
            os.makedirs(backup_location)
        shutil.move(youtubedl_location+youtubedl_dir,backup_location+youtubedl_dir+ time.strftime('%Y%m%d%H%M%S'))
    console.hide_activity()

@ui.in_background
def restore_youtubedl_backup(sender):
    if not os.path.isdir(backup_location) or not os.listdir(backup_location):
        console.alert('Nothing to do', 'No backups found to restore')
    else:
        folders = os.listdir(backup_location)
        folder = folders[len(folders)-1]
        shutil.move(backup_location+folder,youtubedl_location+youtubedl_dir)
        console.alert('Success','Successfully restored '+folder)

def downloadfile(url):
    localFilename = url.split('/')[-1] or 'download'
    with open(localFilename, 'wb') as f:
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        if total_length:
            dl = 0
            total_length = float(total_length)
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                #.setprogress(dl/total_length*100.0)
        else:
            f.write(r.content)
    return localFilename

def process_file(path):
    if zipfile.is_zipfile(path):
        zipfile.ZipFile(path).extractall()

@ui.in_background
def update_youtubedl(sender):
    if os.path.exists(youtubedl_location+youtubedl_dir):
        msg = 'Are you sure you want to update youtubedl exists in site-packages and will be overwritten'
        if not console.alert('Continue',msg,'OK'):
            return
    console.show_activity('Downloading')
    file = downloadfile(youtubedl_downloadurl)
    console.show_activity('Extracting')
    process_file(file)
    console.show_activity('Moving')
    if os.path.exists(youtubedl_location+youtubedl_dir):
        shutil.rmtree(youtubedl_location+youtubedl_dir)
    shutil.move(youtubedl_unarchive_location+youtubedl_dir, youtubedl_location)
    console.show_activity('Cleaning Up Download Files')
    shutil.rmtree(youtubedl_unarchive_location)
    os.remove(file)
    console.show_activity('Making youtube-dl friendly')
    process_youtubedl_for_pythonista()
    console.hide_activity()

def process_youtubedl_for_pythonista():
    for patch in files_to_change:
        filename, old_str, new_str = patch
        replace_in_file(youtubedl_location+youtubedl_dir+'/'+filename, old_str, new_str)

def replace_in_file(file_path, old_str, new_str):
    with open(file_path) as old_file:
        #Create temp file
        fh, abs_path = tempfile.mkstemp()
        os.close(fh)  # close low level and reopen high level
        with open(abs_path,'w') as new_file:
            for line in old_file:
                new_file.write(line.replace(old_str, new_str))
    #Remove original file
    os.remove(file_path)
    #Move new file
    shutil.move(abs_path, file_path)

def make_button(title, action):
    button = ui.Button(title=title)
    button.action = action
    button.background_color ='lightgrey'
    button.border_color = 'black'
    button.border_width = 1
    button.flex = 'WB'
    return button

view = ui.View(frame=(0,0,172,132))
view.background_color = 'white'

backup_button = make_button(title='Backup YoutubeDL', action=backup_youtubedl)
backup_button.center = (view.width * 0.5, view.y+backup_button.height)
view.add_subview(backup_button)

restore_button = make_button(title='Restore YoutubeDL', action=restore_youtubedl_backup)
restore_button.center = (view.width * 0.5, backup_button.y+restore_button.height*1.75)
view.add_subview(restore_button)

download_button = make_button(title='Download YoutubeDL', action=update_youtubedl)
download_button.center = (view.width * 0.5, restore_button.y+download_button.height*1.75)
view.add_subview(download_button)

view.present('sheet')
