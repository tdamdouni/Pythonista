# Pythonista Markdown Editor
# By: EJM Software ---- http://ejm.cloudvent.net
# Source: http://gist.github.com/02df085647247a815eff
# *****************************************
import ui, console, editor, markdown, webbrowser, urllib

@ui.in_background
def new_md(sender):
    filename = console.input_alert('', 'File Name')
    if filename.find('.')>-1:
        filename = filename[:filename.rfind('.')]
    filename += '.md'
    fh = open(filename, 'a')
    del fh
    editor.open_file(filename)
    
@ui.in_background
def view_md(sender):
    mdviewwin = ui.View()
    webview = ui.WebView(frame = (0, 0, mdviewwin.width, mdviewwin.height), flex="WH")
    webview.load_html(markdown.markdown(editor.get_text()))
    mdviewwin.add_subview(webview)
    mdviewwin.present('fullscreen')
    
@ui.in_background
def email_md(sender):
    subject = 'subject='+urllib.quote(editor.get_path().split('/')[-1])
    body = 'body='+urllib.quote(markdown.markdown(editor.get_text()))
    webbrowser.open('mailto:?'+subject+'&'+body)

if __name__=='__main__':
    view = ui.View()
    #Setup the ui elements
    b_new = ui.Button(frame=(2,30,0,0), title="New")
    b_new.action = new_md
    b_view = ui.Button(frame=(2, 60, 0, 0), title="View")
    b_view.action = view_md
    b_email = ui.Button(frame=(2,90,0,0), title="Email")
    b_email.action = email_md
    #Add subviews to main view and 'present' ui
    view.add_subview(b_new)
    view.add_subview(b_view)
    view.add_subview(b_email)
    view.present('sidebar')
