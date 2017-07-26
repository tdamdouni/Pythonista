# https://github.com/markhamilton1/Synchronator

"""
Synchronator.py
Version: 1.5.0
Created by: Mark Hamilton
Created: March 17, 2017
Synchronator is a module that synchronizes
the files between Pythonista and a Dropbox
app folder. This allows the files to be
synched to another device or backed up on
Dropbox.
Synchronator is implemented on the Dropbox
API v2.
The Dropbox API v2 now uses an Access Token
instead of the previous App Token and App
Secret. To get an Access Token you must go
to the Dropbox API v2 website at
https://www.dropbox.com/developers
If you are doing this for use by
Synchronator in Pythonista then follow
these steps. (It is recommended that you do
them on the iOS device where you will be
running Pythonista so that you can easily
copy the Access Token and paste it into the
Pythonista prompt when needed.)
1. Create an app that uses the "Dropbox API".
2. Select the "App Folder" option.
3. Give your app a name. I recommend
"Synchronator-<your name>". The app name you
choose MUST be unique.

If the previous steps were successful then
you have created an app and are now on a
page where you can edit the properties for
your app.
4. Find the property "Generated Access Token"
and select the Generate button.
5. Select and copy the Access Token to the
clipboard.
6. Execute Synchronator in Pythonista on your
iOS device.
7. Enter the Access Token at the prompt.
(Copy and paste is ideal so you do not make
a mistake.)
If everything was done properly then
Synchronator will attempt to synchronize
your Pythonista files to Dropbox.
"""

from __future__ import print_function
import DropboxSetup
import os
import pickle
import requests

DROPBOX_FILES = DropboxSetup.dropbox.files
STATE_FILENAME = '.dropbox_state'


class DropboxState:
    def __init__(self):
        self.local_files = {}       # local file metadata
        self.remote_files = {}      # remote file metadata

    def check_state(self, dbx, path):
        if path not in self.remote_files:
            self.upload(dbx, path, '-- Not Found Remotely')
        elif os.path.getmtime(path) > self.local_files[path]['modified']:
            self.upload(dbx, path, '-- Local File Changed')

    def delete_local(self, path):
        print('\tDeleting Locally: ', path, ' -- File No Longer On Dropbox')
        try:
            os.remove(path)
        except OSError:
            pass
        del self.local_files[path]
        del self.remote_files[path]

    def delete_remote(self, dbx, path):
        print('\tDeleting On Dropbox: ', path, ' -- File Deleted Locally')
        try:
            dbx.files_delete('/' + path)
            del self.local_files[path]
            del self.remote_files[path]
        except:
            print('\t!Remote Delete Failed!')

    def download_remote(self, dbx, path, because=None):
        print('\tDownloading: ', path, because or '')
        head, tail = os.path.split(path)
        if head and not os.path.exists(head):
            os.makedirs(head)
        result = dbx.files_download_to_file(path, os.path.join('/', path))
        meta = {
            'rev': result.rev,
            'modified': os.path.getmtime(path)
        }
        self.local_files[path] = meta
        self.remote_files[path] = meta

    def execute_delta(self, dbx):
        current_remote_file_paths = set()
        results = dbx.files_list_folder('', True)
        while True:
            cursor = results.cursor
            self.__process_remote_entries(results.entries, current_remote_file_paths)
            if not results.has_more:
                break
            results = dbx.files_list_folder_continue(cursor)
        # list of file paths that Synchronator thinks are on remote
        remote_files_keys = self.remote_files.keys()
        for path in remote_files_keys:
            # remote path was not in the current paths from remote
            if path not in current_remote_file_paths:
                # path exists locally
                if path in self.local_files:
                    # delete file locally
                    self.delete_local(path)

    def make_local_dir(self, path):
        if not os.path.exists(path):
            # the folder path does not exist
            os.makedirs(path)
        elif os.path.isfile(path):
            # there is a file in the place that a folder is to be put
            os.remove(path)
            del self.local_files[path]
            os.makedir(path)

    def upload(self, dbx, path, because=None):
        print('\tUploading: ', path, because or '')
        size = os.path.getsize(path)
        if size > 140000000:
            with open(path, 'r') as local_fr:
                data = local_fr.read(10000000)
                close = len(data) < 10000000
                session_id = None
                session_cursor = None
                offset = 0
                while not close:
                    if session_id is None:
                        result = dbx.files_upload_session_start(data, close)
                        session_id = result.session_id
                    else:
                        dbx.files_upload_session_append_v2(data,
                                                           session_cursor,
                                                           close)
                    offset += len(data)
                    if session_cursor is None:
                        print('\t.', end='')
                    elif offset % 100000000 == 0:
                        print('.: ', offset)
                        print('\t', end='')
                    else:
                        print('.', end='')
                    session_cursor = DROPBOX_FILES.UploadSessionCursor(session_id,
                                                                       offset)
                    data = local_fr.read(10000000)
                    close = len(data) < 10000000
                mode = DROPBOX_FILES.WriteMode.overwrite
                commit_info = DROPBOX_FILES.CommitInfo(os.path.join('/', path),
                                                       mode, mute=True)
                result = dbx.files_upload_session_finish(data, session_cursor,
                                                         commit_info)
                print('.')
        else:
            with open(path, 'r') as local_fr:
                data = local_fr.read()
                mode = DROPBOX_FILES.WriteMode.overwrite
                result = dbx.files_upload(data, os.path.join('/', path), mode,
                                          mute=True)
        meta = {'rev': result.rev,
                'modified': os.path.getmtime(path)}
        self.local_files[path] = meta
        self.remote_files[path] = meta

    def __process_remote_entries(self, entries, current_remote_file_paths):
        for entry in entries:
            path = entry.path_display[1:]
            if isinstance(entry, DROPBOX_FILES.FileMetadata):
                rev = entry.rev
                # remote file does not currently exist locally
                if path not in self.local_files:
                    # download remote file to local
                    self.download_remote(dbx, path, '-- Not Found Locally')
                # remote and local files have different revisions
                elif rev != self.local_files[path]['rev']:
                    # download remote file to local
                    self.download_remote(dbx, path, '-- Remote File Changed')
                # add remote path to list
                current_remote_file_paths.add(path)
            elif isinstance(entry, DROPBOX_FILES.FolderMetadata):
                if not os.path.exists(path):
                    print('\n\tMaking Directory: ', path)
                    self.make_local_dir(path)


def check_local(dbx, state):
    print('\nChecking For New Or Updated Local Files')
    filelist = []
    for root, dirnames, filenames in os.walk('.'):
        if valid_dir_for_upload(root):
            for filename in filenames:
                if valid_filename_for_upload(filename):
                    filelist.append(os.path.join(root, filename)[2:])
    for path in filelist:
        state.check_state(dbx, path)
    print('\nChecking For Deleted Local Files')
    oldlist = state.local_files.keys()
    for file in oldlist:
        if file not in filelist:
            state.delete_remote(dbx, file)


def check_remote(dbx, state):
    print('\nUpdating From Dropbox')
    state.execute_delta(dbx)


def download():
    print('\nGetting Synchronator.py From GIT')
    url = 'https://raw.githubusercontent.com/markhamilton1/Synchronator/master/Synchronator.py'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        with open('Synchronator.py', 'w') as script_fr:
            script_fr.write(r.text)
        print('Synchronator.py Downloaded Successfully')
    else:
        print('!Synchronator.py Download Failed!')


def init_dropbox():
    dbx = DropboxSetup.init('Synchronator_Token')
    if dbx is None:
        access_token = DropboxSetup.get_access_token()
        if access_token is not None and access_token != '':
            dbx = DropboxSetup.init('Synchronator_Token', access_token)
        if dbx is None:
            print('!Failed To Initialize Dropbox Session!')
    return dbx


def load_state():
    print('\nLoading Local State')
    try:
        with open(STATE_FILENAME, 'r') as state_fr:
            state = pickle.load(state_fr)
    except:
        print('\nCannot Find State File -- Creating New Local State')
        state = DropboxState()
    return state


def save_state(state):
    print('\nSaving Local State')
    with open(STATE_FILENAME, 'w') as state_fr:
        pickle.dump(state, state_fr)


def valid_dir_for_upload(dir):
    for i, part in enumerate(dir.split(os.path.sep)):
        if part != '.':
            # hidden directory
            if part.startswith('.'):
                return False
            # Pythonista directory
            if (i == 1) and part.startswith('site'):
                return False
            # temp directory
            if (i == 1) and (part == 'temp'):
                return False
    return True


def valid_filename_for_upload(filename):
    return not any((filename == STATE_FILENAME,  # Synchronator state file
                    filename.startswith('.'),    # hidden file
                    filename.startswith('@'),    # temporary file
                    filename.endswith('~'),      # temporary file
                    filename.endswith('.pyc'),   # generated Python file
                    filename.endswith('.pyo')))  # generated Python file


if __name__ == '__main__':
    print('****************************************')
    print('*     Dropbox File Syncronization      *')
    print('****************************************')

    # initialize the dropbox session
    dbx = init_dropbox()
    # make sure session creation succeeded
    if dbx:
        # load the sync state
        state = load_state()
        # check dropbox for sync
        check_remote(dbx, state)
        # save the sync state so far
        save_state(state)
        # check local for sync
        check_local(dbx, state)
        # save the sync state
        save_state(state)
        print('\nSync Complete')
