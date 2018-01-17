import sys,os
# if you place objc_hacks in site packages, this line is not needed
sys.path.append(os.path.expanduser('~/Documents'))

from objc_hacks import apphack
#alternatively, just place apphack.py in site_packages, and import apphack

#little workaround to persistent button locations. needs fixing in apphack
if hasattr(apphack,'__persistent_views'):
   __builtins__.__persistent_views=apphack.__persistent_views
elif not hasattr(__builtins__,'__persistent_views'):
   __builtins__.__persistent_views={}


def example(sender):
		'''Functions must be of form that take single, sender argument, which is the ui.Button
		Also note that the function gets stored so it survives 
		global clears, but the globals() still is cleared.  meaning
		the function must be completely standalone.  all imports 
		needed by the function must happen within the function, not 
		outside
		'''
		import editor,console

		console.hud_alert(editor.get_path())
		#for kicks, toggle tint
		sender.tint_color=tuple(1-x for x in sender.tint_color[0:3])


def search_apple(sender):
   import editor,webbrowser, urllib3.request
   _sel=editor.get_selection()
   _txt=editor.get_text()[_sel[0]:_sel[1]]
   webbrowser.open('https://google.com/search?{}'.format(urllib3.request.urlencode({'q':'reference '+_txt,'as_sitesearch':'developer.apple.com','btnI':'I'})))

def comment(sender):
  """" comment out selected lines"""
  import editor
  import re
  COMMENT='#'
  i=editor.get_line_selection()
  t=editor.get_text()
  # replace every occurance of newline with  ewline plus COMMENT, except last newline
  editor.replace_text(i[0],i[1]-1,COMMENT+re.sub(r'\n',r'\n'+COMMENT,t[i[0]:i[1]-1]))

  editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

def uncomment(sender):
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


# now... create buttons
apphack.create_toolbar_button(example,'iow:information_circled_32',0)
apphack.create_toolbar_button(search_apple,'iob:social_apple_outline_32',1)
apphack.create_toolbar_button(comment,'iow:code_working_32',2)
apphack.create_toolbar_button(uncomment,'iow:ios7_more_32',3)


