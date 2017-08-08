# Drafts-Rezepte II: Kurzlinks mit is.gd

_Captured: 2015-09-28 at 23:10 from [kulturproktologie.de](http://kulturproktologie.de/?p=4602)_

Es ist ja durchaus sinnvoll, Links ab und an mal zu verkurzen, jedoch dafur extra eine App zu installieren erscheint mir etwas ubertrieben. Das lasst sich zwar auch im Browser erledigen, artet aber in eine Klickorgie aus, auf die ich auch keine Lust habe. Mit _Pythonista_ und _Drafts_ ist das im Handumdrehen erledigt.

Dieses kleine Script habe ich als _isgd.py_ im Dokumentenverzeichnis von _Pythonista_ angelegt:

```
# @Drafts
# http://kulturproktologie.de/?p=4602
# https://gist.github.com/kultprok/f4f62e4e9bc59e575726

import clipboard
from console import alert
from sys import argv, exit
from urllib import urlopen
import webbrowser

def error_dialog(title, message):
  '''A diaolog box for error messages.'''
	try:
		alert(title, message)
	except KeyboardInterrupt:
		pass
	webbrowser.open('drafts4://')
	exit(message)

def shorten_with_isgd(long_url):
	'''basic link-shortening via is.gd.'''
	api_url_base = 'http://is.gd/create.php?format=simple&url='
	try:
		response = urlopen(api_url_base + long_url)
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() == 200:
		short_link = response.read()
		clipboard.set(short_link)
	else:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
	webbrowser.open('drafts4://')

if __name__ == '__main__':
	shorten_with_isgd(argv[1])
```

Es ist alles recht simpel gehalten, die Fehler werden nur rudimentar behandelt, aber es sollte ganz gut aufgehen. _is.gd_ habe ich fur den Anfang als Dienst gewahlt, weil dort nicht großartig Registrierungen notwendig sind, um mit der API Links zu kurzen.

In _Drafts_ muss dann nur die folgende Action angelegt werden, um das Script auszufuhren.

[Import](drafts4://x-callback-url/import_action?type=URL&name=Shorten%20Link%20%28is.gd%29&url=pythonista%3A%2F%2Fisgd%3Faction%3Drun%26argv%3D%5B%5Bdraft%5D%5D)

Die Handhabung ist nun denkbar einfach: In _Drafts_ in einer neuen Notiz die lange URL eingeben, danach die Action auslosen. Es wird sich _Pythonista_ offnen. Sofern keine Fehlermeldung aufpoppt, ist der Kurzlink in die Zwischenablage kopiert worden. Auf jeden Fall wird aber wieder _Drafts_ geoffnet.
