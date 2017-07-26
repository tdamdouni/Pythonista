# https://forum.omz-software.com/topic/3736/has-somebody-already-used-pydrive-to-access-google-drive-files/9

# https://pythonhosted.org/PyDrive/oauth.html#sample-settings-yaml

# see https://pythonhosted.org/PyDrive/quickstart.html
# see https://pythonhosted.org/PyDrive/oauth.html#sample-settings-yaml
# see https://github.com/googledrive/PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import webbrowser

# Create local webserver and auto handles authentication.
# Standard webbrowser gave an error, JonB found the solution
if not hasattr(webbrowser,'_open'):
    webbrowser._open=webbrowser.open
def wbopen(url, *args,**kwargs):
    return webbrowser._open(url)
webbrowser.open=wbopen

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

# upload 
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello World!') # Set content of the file from given string.
file1.Upload()

file1 = drive.CreateFile({'title': 'quickstart.py'})  # Create GoogleDriveFile instance with title ...
file1.SetContentFile('quickstart.py') # Set content of the file from given file
file1.Upload()
