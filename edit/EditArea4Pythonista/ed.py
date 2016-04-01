# coding: utf-8
# ed  a proof of concept of using a javascript editor inside a webview
#  uses editarea to provide a capable editor
#  lightly wrapped in a webview
#
#TODO:   multiple file support, and custom callbacks to allow open/save buttons inside editarea to work
#        .git/config file support
#        improve clunky filename dialog interface.  open should pop up dialog, save should save, maybe need saveas which shows dialog again.  multiple file spupport miht fix that.  
#        fix starting path.. maybe set to whatever current file is being edited
#        debug why often have to minimize /maximize keyboard to get text entry working
#        shellista plugin
#        investigate alternate editors
#        auto resize on orientation change and keyboard show/hide
#__package__ = 'plugins.extensions'
import ui, os, uidir, json, sys, editor, inspect
from console import hud_alert
from functools import partial


class ed(object):
    def edopen(self,sender):
        '''open the file named in the textbox, load into editor'''
        w=sender.superview['webview1']
        f=sender.superview['filename']
        try:
            with open(f.text) as file:
                w.eval_js('editAreaLoader.setValue("code",{});'.format(json.dumps(file.read())))
                hud_alert('opened '+os.path.relpath(file.name))
                w.eval_js('editAreaLoader.execCommand("code","change_syntax","{}");'.format(self.determine_style(file.name)))
        except (IOError):
            hud_alert( 'file not found')

    def edsave(self,sender):
        '''save the editor content to file in filename textbox'''
        w=sender.superview['webview1']
        f=sender.superview['filename']
        try:
            with open(f.text,'w') as file:
                file.write(w.eval_js('editAreaLoader.getValue("code");'))
                hud_alert('saved '+os.path.relpath(file.name))
        except(IOError):
            hud_alert('could not save')

    def edselect(self,sender):
        '''display file selection dialog, and set filename textfield'''
        f=sender.superview['filename']
        def setter(s):
            f.text=os.path.relpath(s)
        uidir.getFile(setter)

    @classmethod
    def determine_style(self,filename):
        '''return style name used by change_syntax, based on file extension.  '''
        syntaxes={'css':'css',
                 'html':'html',
                 'js':'js',
                 'php':'php',
                 'py':'python',
                 'vb':'vb',
                 'xml':'xml',
                 'c':'c',
                 'cpp':'cpp',
                 'sql':'sql',
                 'bas':'basic',
                 'pas':'pas',
                 'pl':'perl'}
        try:
            ext=os.path.splitext(filename)[1][1:]
            syntax=syntaxes[ext]
        except(KeyError):
            #print ext
            syntax='robotstxt'
        return syntax

    def initView(self,filename=None):
        '''setup the View.  if filename is omitted, open current file in editor'''
        #print os.path.abspath(__file__)
        #shname=inspect.getfile(inspect.getouterframes(inspect.currentframe())[-1])

        p= os.path.dirname(inspect.stack()[-1][1])
        s=  os.path.join(p,os.path.splitext(__file__)[0])
        e=ui.load_view(s)
        # e=ui.load_view(os.path.splitext(__file__)[0])
        e['loadbutton'].action=self.edopen
        e['savebutton'].action=self.edsave
        e['selectbutton'].action=self.edselect

        srcname='editarea.html'
        w=e['webview1']
        w.load_url(os.path.abspath(srcname))

        e.present('panel')
        if filename is not None:
            f=e['filename']
            try:
                f.text=filename
                ui.delay(partial( self.edopen,w), 1)
            except:
                pass
        return e

    def __init__(self,filename=None):
    #if i change over to inheriting from View, this will need to change
        self.e=self.initView(filename)

if __name__=='__main__':
    #for some reason editor.get_path returns a path starting at /var, but os.curdir starts at /private/var
    e=ed(os.path.relpath('/private'+editor.get_path()))
