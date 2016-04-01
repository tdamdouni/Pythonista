import webbrowser

import clipboard
import dropbox


# Initialize Dropbox.
app_key = 'Aaaaaaa'
app_secret = 'bbbbbbbbb'
access_key = 'ccccccccc'
access_secret = 'ddddddddd'
sess = dropbox.session.DropboxSession(app_key, app_secret, 'dropbox')
sess.set_token(access_key, access_secret)
client = dropbox.client.DropboxClient(sess)


# Append to ifttt.txt

text=clipboard.get()
print(text)
filename = '/Apps/Editorial/Todo/ifttt.txt'
f=client.get_file(filename)
log=f.read()
f.close()

log+= text + '\n'
client.put_file(filename,log,overwrite=True )
 
webbrowser.open('workflow://')


