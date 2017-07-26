# https://github.com/markhamilton1/Synchronator

"""
A module to write or read a Dropbox Access Token file.
Based heavily on a module of the same name by Michelle
Gill (mlgill).

The Dropbox API v2 now uses an Access Token insteaad of the
previous App Token and App Secret. To get an Access Token
you must go to the Dropbox API v2 website at

https://www.dropbox.com/developers

If you are doing this for use by Synchronator in Pythonista
then follow these steps. (It is recommended that you do them
on the iOS device where you will be running Pythonista so that
you can easily copy the Access Token and paste it into the
Pythonista prompt when needed.)

1. Create an app that uses the Dropbox API.
2. Select the App Folder option.
3. Give your app a name. I recommend Synchronator-<your name>.
    The app name you choose MUST be unique.

If the previous steps were successful then you have created
an app and are now on a page where you can edit the properties
for your app.

4. Find the property "Generated Access Token" and select
the Generate button.
5. Select and copy the Access Token to the clipboard.
6. Execute Synchronator in Pythonista on your iOS device.
7. Enter the Access Token at the prompt. (Copy and paste is
ideal so you do not make a mistake. )

If everything was done properly then Synchronator will attempt
to synchronize your Pythonista files to Dropbox.

There are many different applications that can take advantage
of Dropbox, that is why this module has been kept seperate
from any applications.

Usage:
To read an existing token:

import DropboxSetup
dbx = DropboxSetup.init('<TOKEN_FILENAME>')

To write a new token:

import DropboxSetup
dbx = DropboxSetup.init('<TOKEN_FILENAME>', '<ACCESS_TOKEN>')
"""


import dropbox
import os

try:
    raw_input          # Python 2
except NameError:
    raw_input = input  # Python 3


def __read_token(token_directory, token_filename):
    with open(token_directory + token_filename) as in_file:
        return in_file.read()


def __write_token(token_directory, token_filename, access_token):
    with open(token_directory + token_filename, 'w') as out_file:
        out_file.write(access_token)


def init(token_filename, access_token=None, token_directory='.Tokens'):
    """
    Configure and open a Dropbox connection.

    string -- token_filename
    string -- access_token (default None)
    string -- token_directory (default 'Tokens')
    """
    token_directory = token_directory or ''
    if token_directory and (token_directory[-1] != os.sep):
        token_directory += os.sep
    if token_directory not in ('', '.'):
        if not os.path.exists(token_directory):
            os.mkdir(token_directory)
    if not access_token:
        if os.path.exists(token_directory + token_filename):
            access_token = __read_token(token_directory, token_filename)
        else:
            return None
    else:
        if os.path.exists(token_directory + token_filename):
            os.remove(token_directory + token_filename)
        __write_token(token_directory, token_filename, access_token)
    dbx = dropbox.Dropbox(access_token)
    return dbx


def get_access_token():
    """
    Prompt for and get the access token.
    This method is provided so that a consistent prompt is always used.
    """
    return raw_input('Enter access token:').strip()


def get_token_filename():
    """
    Prompt for and get the token filename.
    This method is provided so that a consistent prompt is always used.
    """
    return raw_input('Enter token filename:').strip()


if __name__ == '__main__':
    dbx = init(get_token_filename(), get_access_token())
