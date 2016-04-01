 # coding: utf-8
import editor, ui
import Find_and_replace
import Tabs
INDENTSTR='    ' #4 spaces, pep8 preference

class editmenuclass(ui.View):
    _lastinstance=None
            
    def handlebutton(self,sender):
        """handler for generic button tap.
            calls function that matches button name
        """
        try:
            func=getattr(self,sender.name)
            func()
        except AttributeError():
            console.hud_alert('bad button name')
    def did_load(self):
        for s in self['scrollview1'].subviews:
            if isinstance(s,ui.Button):
                #pass
                s.action = self.handlebutton
        type(self)._lastinstance=self
    def show(self):
        """show the sidebar. """
        self.present('sidebar')

    # ###################################################
    #  the following are all button actions, 

    def indent(self):
        """indent selected lines by one tab"""
        import editor
        import re

        i=editor.get_line_selection()
        t=editor.get_text()
        # replace every occurance of newline with  newline plus indent, except last newline
        editor.replace_text(i[0],i[1]-1,INDENTSTR+re.sub(r'\n',r'\n'+INDENTSTR,t[i[0]:i[1]-1]))

        editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

    def unindent(self):
        """unindent selected lines all the way"""
        import editor
        import textwrap

        i=editor.get_line_selection()
        t=editor.get_text()

        editor.replace_text(i[0],i[1], textwrap.dedent(t[i[0]:i[1]]))

        editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

    def comment(self):
        """" comment out selected lines"""
        import editor
        import re
        COMMENT='#'
        i=editor.get_line_selection()
        t=editor.get_text()
        # replace every occurance of newline with  ewline plus COMMENT, except last newline
        editor.replace_text(i[0],i[1]-1,COMMENT+re.sub(r'\n',r'\n'+COMMENT,t[i[0]:i[1]-1]))

        editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

    def uncomment(self):
        """" uncomment selected lines"""
        import editor
        import re
        COMMENT='#'
        i=editor.get_line_selection()
        t=editor.get_text()
    # replace every occurance of newline # with newline, except last newline

        if all( [x.startswith('#') for x in t[i[0]:i[1]-1].split(r'\n')]):
            editor.replace_text(i[0],i[1]-1,re.sub(r'^'+COMMENT,r'',t[i[0]:i[1]-1],flags=re.MULTILINE))

        editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

    def execlines(self):
        """execute selected lines in console.   """
        import editor
        import textwrap

        a=editor.get_text()[editor.get_line_selection()[0]:editor.get_line_selection()[1]]

        exec(textwrap.dedent(a))

    def selectstart(self):
        import editor
        i=editor.get_selection()
        editor.set_selection(i[0],i[1]+1)

    def finddocstring(self):
        ''' find the docstring at current cursor location
        '''
        import StringIO
        from jedi import Script

        i=editor.get_selection()
        t=editor.get_text()
        (line,txt)=[(line,n) for (line,n) in enumerate(StringIO.StringIO(editor.get_text()[:i[1]]))][-1]
        script = Script(t, line+1, len(txt))

        dfn = script.goto_definitions()
        if dfn:
            doc=dfn[0].doc
            import ui
            v=ui.TextView()
            v.width=100
            v.height=50
            v.text=doc
            editor._set_toolbar(v)

    def copy(self):
        import clipboard
        i=editor.get_selection()
        t=editor.get_text()
        clipboard.set(t[i[0]:i[1]])

    def paste(self):
        import clipboard
        i=editor.get_selection()
        t=editor.get_text()
        editor.replace_text(i[0],i[1], clipboard.get())
        editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))
    def cut(self):
        import clipboard
        i=editor.get_selection()
        t=editor.get_text()
        clipboard.set(t[i[0]:i[1]])
        editor.replace_text(i[0],i[1], '')
        editor.set_selection(i[0],i[0])

    def tabs(self):
        #import webbrowser

        Tabs.tabs()
        #webbrowser.open('pythonista://site-packages%2Feditmenu%2Tabs.py?action=run')

    def find_and_replace(self):
        #import webbrowser
        Find_and_replace.showfindbar()
        #webbrowser.open('pythonista://site-packages%2Feditmenu%2FFind_and_replace.py?action=run')

    ##################
    #  classmethods to load/show 
    @classmethod
    def load(cls):
        import os, inspect
        pyui= os.path.abspath(inspect.getfile(inspect.currentframe()))+'ui'
        
        if cls._lastinstance is None:
            cls._lastinstance = ui.load_view(pyui)
        return cls._lastinstance
    
    @classmethod
    def load_and_show(cls):
        editmenuview=cls.load()
        editmenuview.show()

            
            
if __name__=='__main__':
    editmenuclass.load_and_show()
 
