# Compare text documents in your iPhone with Pythonista

_Captured: 2015-09-28 at 23:34 from [onetapless.com](https://onetapless.com/compare-documents-in-your-iphone-with-pythonista)_

If you have a Mac, you may have heard of [Kaleidoscope](https://itunes.apple.com/us/app/kaleidoscope/id587512244?mt=12&uo=4&at=10l4KL), an amazing application to compare documents, folders, images, anything. It is certainly the cream of the crop in the category, which justifies its price tag. I wanted some sort of the functionality from Kaleidoscope in my iOS devices to compare my drafts before publishing here.

[Editorial](https://itunes.apple.com/us/app/editorial/id673907758?mt=8&uo=4&at=10l4KL) has a nice workflow to show the differences between the current document and the clipboard, it honestly wouldn't take long to allow file selection, still, I was seeking for a workflow I could use on my iPhone as well, also, the looks of the output never caught my eye. Considering the screen from mobile devices, the side-by-side table was not the best pick, I was searching for an result similar to GitHub's.

If you don't know what I'm talking about, you can check the revisions of any gist, [this is an example](https://gist.github.com/philgruneich/6859485/revisions). Github tints the line red for text replaced, followed by the replacement as a green line. While we are talking about GitHub, I [found a repository](https://github.com/kilink/ghdiff) with most of the work done. All I had to do was adapt it for [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=10l4KL).

    
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
    

First step was cutting down the modules unavailable on iOS, `six` and `chardet`, the first is a compatibility library between Python 2 and 3, the latter detects the encoding of the string. I honestly thought that I could live without both. The `xml.sax.saxutils` module also served the single purpose to substitute spaces for their encoded counterpart, so I also decided to skip it as well, ending up with the `difflib` module only, responsible to compare our documents, thus essential for our workflow.

I changed `six.string_types` for its Python 2 variant, `basestring`, removed the other two modules, `optparse` and `sys`, specially since Pythonista doesn't request the latter to collect arguments with `sys.argv`. I also hoped for a prettier outcome, so instead of a collection of div elements, I aimed for a better markup using `ins`, `del` and `mark` and made the output look great on your iPhone. This demanded some extra tweaking though.

Everything set, even a regex to remove empty paragraphs and highlights, I needed a way to display this HTML output, as Pythonista's console can't read the format. First I thought of interacting with [Textastic](https://itunes.apple.com/us/app/textastic-code-editor-for/id550156166?mt=8&uo=4&at=10l4KL) somehow, but this idea fell ashore. Then I was greeted by Dr. Drang's script to [display weather information using a local server](http://www.leancrew.com/all-this/2014/02/weather-underground-in-pythonista/) created by the `BaseHTTPServer` module, which is a pain in the ass, but was my finest asset.

The snippet I used is pretty much the same as Drang's, with a single fix to avoid the _Address already in use_ error reported by the Doc, `server.server_close()`.

Now all I needed was two objects to compare. So I went for [Launch Center Pro](https://itunes.apple.com/us/app/launch-center-pro/id532016360?mt=8&uo=4&at=10l4KL) for its `[dropbox-text]` parameter, however, I met a strange behavior where I couldn't use it twice, it would download the first text and trigger Pythonista. I found a way around by making LCP launch itself:

    
    launchpro://?url=pythonista%3A%2F%2FDiff%2Fdiff_dropbox%3Faction%3Drun%26argv%3D{{[dropbox-text]}}%26argv%3D%5Bdropbox-text%5D

We used this trick before to manually encode the parameters and cheat the way LCP interprets the variables. You may want to replace the `Diff%2Fdiff_dropbox` part because it is the location and name of my script. It reads: script _diff_dropbox_ within the folder _Diff_, `%2F` is the slash separating both. If you leave it in your root folder, use only the name of the script.

I won't be naive and tell you this script is perfect, however, it brings a cool new functionality to your phone. The best part? Since the script uses just `sys.argv` to receive text, you can change the trigger to send clipboard, current document in [Drafts](https://itunes.apple.com/us/app/drafts/id502385074?mt=8&uo=4&at=10l4KL) or [1Writer](https://itunes.apple.com/us/app/1writer/id680469088?mt=8&uo=4&at=10l4KL) and many other possibilities. And you thinking we had boundaries.
