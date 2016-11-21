# Gist.py
 
Gist.py is a simple script that makes it super easy to create a Gist on your iOS device by combining the powers of [Drafts](http://agiletortoise.com/drafts) and [Pythonista](http://omz-software.com/pythonista/).

# How to install

Copy and paste the code in Gist.py into a Pythonista file called "Gist". If you only use Pythonista and don't want to use Drafts, put in default values for the variables defined by `sys.argv`. E.g., change these lines:

```python
username = sys.argv[1]
filename = sys.argv[2]
try:
    content = sys.argv[3]
except IndexError:
    content = clipboard.get()
try:
    public = sys.argv[4] == "public"
except:
    public = False
```

to something like this:

```python
username = "dlo"
filename = "content.txt"
content = clipboard.get()
public = False
```

If you want to integrate with Drafts, use the following URL scheme with the name "Create Gist":

    pythonista://Gist?action=run&argv=YOUR_USERNAME&argv=[[title]]&argv=[[body]]

After installing this, the first line of your Draft will be the filename, and the body will be the file contents.

The first time Gist.py runs, it will prompt you for your GitHub username and password. This is so that it can create an access token. Gist.py saves your access token in your Pythonista keychain after the first successful authentication, so you'll only be prompted once.

After it creates the gist, Gist.py copies the URL to your clipboard so you can do whatever you want with it.

Enjoy!
