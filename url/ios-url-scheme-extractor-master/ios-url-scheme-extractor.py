import zipfile
import os
import fnmatch
import shutil
from biplist import *
from sys import platform as _platform
from os.path import expanduser
import Tkinter,tkFileDialog

def extract_url_scheme(bytes):
    plist = readPlistFromString(bytes)
    schemes = []
    print plist
    if 'URL Types' in plist:
        for data in plist['URL Types']:
            for scheme in data.get('URL Schemes'):
                schemes.append(scheme)
    if 'CFBundleURLTypes' in plist:
        for data in plist['CFBundleURLTypes']:
            for scheme in data.get('CFBundleURLSchemes'):
                schemes.append(scheme)
    return schemes

def get_url_scheme(filename):
    with zipfile.ZipFile(filename) as zf:
        for filename in zf.namelist():
            if filename.endswith('Info.plist'):
                bytes = zf.read(filename)
                #print bytes
                schemes=extract_url_scheme(bytes)
                print schemes
                return schemes
        return ''

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.textbox = []

    def initialize(self):
        self.grid()

        button = Tkinter.Button(self,text=u"Open",
                                command=self.OnButtonClick)
        button.grid(column=0,row=0)

        self.entry_vars = []
        self.entries = []
        for i in xrange(10):
            entry_var = Tkinter.StringVar()
            entry = Tkinter.Entry(self,textvariable=entry_var)
            entry.grid(column=0,row=i + 1,sticky='EW')

            self.entry_vars.append(entry_var)
            self.entries.append(entry)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)

    def showFileOpen(self):
        initialdir = ''

        if _platform == "darwin":
            initialdir = expanduser("~") + '/Music/iTunes/iTunes Music/Mobile Applications' 
        elif _platform == "win32":
            initialdir = expanduser("~") + '\\My Documents\\My Music\\iTunes\\iTunes Media\Mobile Applications'

        if not os.path.exists(initialdir):
            initialdir = ''

        file = tkFileDialog.askopenfile(parent=self.parent,
                                        mode='rb',
                                        title='Choose a file',
                                        defaultextension='ipa',
                                        initialdir=initialdir)
        return file

    def OnButtonClick(self):
        file = self.showFileOpen()
        if file != None:
            for entry_var in self.entry_vars:
                entry_var.set('')
            path = os.path.abspath(file.name)
            # print u'input: {0}'.format(path)
            schemes = get_url_scheme(path)
            # print u'output: {0}'.format(schemes)

            for i, scheme in enumerate(schemes):
                self.entry_vars[i].set(scheme + '://')

            # import tkMessageBox
            # tkMessageBox.showinfo("Result", '\n'.join(schemes))

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('URL Scheme extractor')
    app.minsize(300, 200)
    app.mainloop()


