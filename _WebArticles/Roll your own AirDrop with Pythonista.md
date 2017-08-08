# Roll your own AirDrop with Pythonista

_Captured: 2015-11-07 at 00:48 from [mygeekdaddy.net](http://mygeekdaddy.net/2014/01/20/roll-your-own-airdrop-with-pythonista/)_

It's always fun when two, seemingly unrelated topics, slowly merge together to give me a new idea. The first one I've been working on for some time has been a simpler way to quickly share code snippets between my Mac and my iPad. Yes, I know that's what Dropbox is for, but I wanted something with less overhead for quick a cut/copy/paste workflow. So when Apple discussed the idea of AirDrop a lot of people thought it sounded too good to be true. Now that Mavericks and iOS 7 have shipped, it appears the pundits were right.

So while this was rattling through my head, I read [a post by Ole Zorn](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html) on how he could use Pythonista to run a local web server, [using SimpleHTTPServer](http://omz-software.com/pythonista/docs/library/simplehttpserver.html#module-SimpleHTTPServer), to install short cuts on an iOS device. Go ahead and read his post… I can wait.

So after seeing Ole's post, I started to play around with the ` SimpleHTTPServer` module and put this together:
    
    
    import SimpleHTTPServer
    import SocketServer
    import webbrowser
    
    PORT = 8000
    
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    
    print "serving at port", PORT
    httpd.serve_forever()

Running this script in Pythonista on my iPad will turn the it into a mini web server.

Taking a peak at my iPad IP address (192.168.1.127), I go over to my Mac and open the URL `<http://192.168.1.127:8000>` and I see the following: 

![](http://share.mygeekdaddy.me/ipad_list_on_mac_2014-01-19.png)

When the script is run in Pythonista, it treats the folder the script was started from as the root folder of the web server. So what I end up seeing is a list of the files in my Pythonista app. Here I can open one of the files, cut/copy portions of a script, and save it on my Mac. The iPad can even serve up proper HTML:

![](http://share.mygeekdaddy.me/ipad_html_page_2014-01-19.png)

Now using the same concept, I can reverse the process and run a mini web server on my Mac to get files onto my iOS device. Open Terminal and go to the folder you want to share and run the following command:
    
    
    python -m SimpleHTTPServer 8000
    

This basically tells Python to load the `SimpleHTTPServer` module as a script, passing the value `8000` as a parameter. Now open Safari, enter the URL `<http://127.0.0.1:8000>`, and you get the following:

![](http://share.mygeekdaddy.me/Running_on_Mac_2014-01-19.png)

Since the script was run from the `boxdrop` folder, it treats the `boxdrop` folder as the root folder for the web server. So in the Finder window you can see there are four files:

  * date_time.py
  * GTD & OmniFocus Guide.pdf
  * IMG_0010-1.png
  * REFX - Clear Websphere Cache.md

Now open Safari on my iPad and I can see the list includes the four files and the typically hidden `.DS_Store` file.

![](http://share.mygeekdaddy.me/_img_BLOGX_Roll_your_own_AirDrop_2014_01_19_222310.png)

> _From here I can open the date_time.py script from Mac on my iPad._

![](http://share.mygeekdaddy.me/_img_BLOGX_Roll_your_own_AirDrop_2014_01_19_223311.png)

So now if there is a code snippet on my iPad that I want to pull back to my Mac, I just run a modified version of the previous web server script. I use this one because now I can see what my IP address is inside of Pythonista.
    
    
    import SimpleHTTPServer
    import SocketServer
    import webbrowser
    import socket
    
    ip_addr = socket.gethostbyaddr(socket.getfqdn())[2]
    
    port = 8000
    
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    
    httpd = SocketServer.TCPServer(("", port), Handler)
    
    print "Serving on IP address: ", ip_addr
    print "Serving on port: ", port
    httpd.serve_forever()

From here I could use Ole's short cut technique and put this script as a short cut on my iPad.

> So where does this get me?

Frankly I'm not sure. While these _hacks_ allow for the simple snippet sharing I was looking for, there feels like there is quite a bit of potential still untapped. I'm hoping this opens the door to others to explore and develop more elegant tools.

Got any questions? Feel free to hit me up on Twitter at [@MyGeekDaddy](http://twitter.com/mygeekdaddy).
