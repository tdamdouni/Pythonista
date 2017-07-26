# https://gist.github.com/jsbain/07984932d22c10bf097103345c8910c7

'''Grab the currently selected keyword in the editor, then go to the apple developer docs page that describes that word'''
import editor,webbrowser, urllib3.request
_sel=editor.get_selection()
_txt=editor.get_text()[_sel[0]:_sel[1]]
webbrowser.open('https://google.com/search?{}'.format(urllib3.request.urlencode({'q':'reference '+_txt,'as_sitesearch':'developer.apple.com','btnI':'I'})))
