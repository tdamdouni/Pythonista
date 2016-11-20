# https://onetapless.com/compare-documents-in-your-iphone-with-pythonista
# -*- coding: utf-8 -*-
import difflib
import re
import BaseHTTPServer
import webbrowser

header = '''<!DOCTYPE html>
<html>
<head>
<title>Text Comparison</title>
<meta name="viewport" content="initial-scale=1.0, width=device-width">
</head>
<body>
'''

footer = '''
</body>
</html>'''

default_css = '''\
<style type="text/css">
   body {
         overflow-x: hidden;}
    #diff {
        border: 1px solid #cccccc;
        background: none repeat scroll 0 0 #f8f8f8;
        font-family: Menlo-Regular,"Courier",monospace;
        font-size: 16px;
        line-height: 1.4;
        white-space: pre-wrap;
        word-wrap: break-word;
        word-break: break-word;
        color: #000;
    }
    #diff .control {
        background-color: #eaf2f5;
        color: #999;
    }
    #diff ins {
        background-color: #ddffdd;
        display: block;
    }
    #diff ins mark {
        background-color: #aaffaa;
    }
    #diff del {
        background-color: #ffdddd;
        display: block;
    }
    #diff del mark {
        background-color: #ffaaaa;
    }
</style>
'''

def diff(a, b, n=3, css=True):
	if isinstance(a, basestring):
		a = a.splitlines()
	if isinstance(b, basestring):
		b = b.splitlines()
	return colorize(list(difflib.unified_diff(a, b, n=n)), css=css)
	
def colorize(diff, css=True):
	css = default_css if css else ""
	return header + css + "\n".join(_colorize(diff)) + footer
	
def _colorize(diff):
	if isinstance(diff, basestring):
		lines = diff.splitlines()
	else:
		lines = diff
	lines.reverse()
	while lines and not lines[-1].startswith("@@"):
		lines.pop()
	yield '<section id="diff">'
	while lines:
		line = lines.pop()
		if line.startswith("@@"):
			yield '<div class="control">%s</div>' % line
		elif line.startswith("-"):
			if lines:
				_next = []
				while lines and len(_next) < 2:
					_next.append(lines.pop())
				if _next[0].startswith("+") and (len(_next) == 1
				or _next[1][0] not in ("+", "-")):
					aline, bline = _line_diff(line[1:], _next.pop(0)[1:])
					yield '<del>-%s</del>' % (aline,)
					yield '<ins>+%s</ins>' % (bline,)
					if _next:
						lines.append(_next.pop())
					continue
				lines.extend(reversed(_next))
			yield '<del>%s</del>' % line
		elif line.startswith("+"):
			yield '<ins>%s</ins>' % line
		else:
			yield '<p>%s</p>' % line
	yield "</section>"
	
def _line_diff(a, b):
	aline = []
	bline = []
	for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
		if tag == "equal":
			aline.append(a[i1:i2])
			bline.append(b[j1:j2])
			continue
		aline.append('<mark>%s</mark>' % a[i1:i2])
		bline.append('<mark>%s</mark>' % b[j1:j2])
	return "".join(aline), "".join(bline)
	
if __name__ == "__main__":

	a = sys.argv[1]
	b = sys.argv[2]
	
	html = re.sub("<(p|mark)>\s??</(p|mark)>","",diff(a,b))
	
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write(html)
server = BaseHTTPServer.HTTPServer(('', 8888), MyHandler)
webbrowser.open('http://localhost:8888')
server.handle_request()
server.server_close()

