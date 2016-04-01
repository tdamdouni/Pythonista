# https://gist.github.com/GuyCarver/4173534

from scene import *
import feedparser
from time import sleep
import random
import Queue
from threading import Thread, Event

fontsize = 25
coverw = fontsize   #The width of the rectangle used to cover the end of the scroll area.
scrollspeed = 100 #Pixels per second to scroll.

requests = Queue.Queue()    #Create a thread safe queue for the rss feed reading.

###Add request for rss read to queue.
def addrequest(req): requests.put(req)

###Thread function to process rss feed load requests.
def loadthread():
  while True:
    requests.get().load()   #Get next entry, blocks until data available, then load it.
    requests.task_done()    #Set the task as done, not really used by this system though.

ldthread = None  #Pointer to the loading thread.

###Rectangle containing a scrolling news feed.
class scrolltext(object):
  def __init__(self, rect, url):
    self.textarea = Rect(*rect) #The area for the scrolling text.
    self.random = True  #Randomize the feed entries.
    self.url = url  #URL to read rss feed from.
    self.scrollspeed = scrollspeed  #Speed to scroll text in pixels/second.
    self.textcolor = Color(1.00, 1.00, 0.00)    #Color of text.
    self.leftrect = Rect(self.textarea.x, self.textarea.y - 1, coverw, fontsize) #Rectangle for box to cover left side of box.
    self.rightrect = Rect(self.textarea.right() - coverw, self.leftrect.y, self.leftrect.w, self.leftrect.h) #Rectangle for box to cover right side of box.
    self.titlerect = Rect(self.textarea.x, self.textarea.y + fontsize + 4, 0, fontsize) #Box for the RSS feed title text.
    self.displaytextrect = Rect(self.textarea.right(), self.textarea.y, 0, fontsize)
    self.displaytext = ''   #Text from RSS feed to display in the visible area.
    self.displaytextimg = None  #Image if displaytext.
    self.lletter = 0    #Index of left letter.
    self.rletter = 0    #Index of right letter.
    self.lletterimg = -1    #Index of left letter used to generate displaytextimg.
    self.rletterimg = -1    #Index of right letter used to generate displaytextimg.
    self.text = ''
    self.title = None           #Title text.
    self.titleimg = None    #Image of title text.
    self.rend = 'White_Square'  #Left/right end image caps.
    self.lend = self.rend
    self.curmessage = 0 #Index of message in rss feed message array.
    self.uddone = Event()   #Event used to signal when URL update is done.
    self.uddone.clear()     #Start the event cleared.

    self.displaytextimg = render_text(' ', font_size=fontsize)  #Crate an empty image of the display text.
    self.getheadlines() #Start download of RSS feed.

  ###Start the RSS feed download.
  def getheadlines(self):
    self.state = self.waitfordata   #Update state to wait for data download
    self.title = 'queued'   #Set the display text for the title.
    addrequest(self)    #Queue the rss feed download request.

  ###Load the RSS feed data.  This is called from the loading thread.
  def load(self):
    self.title = 'loading'  #Set title text to loading.
    d = feedparser.parse(self.url)  #Parse the rss feed.
    self.title = d['feed']['title'].encode('utf-8') #Get the title text.
#this causes errors with 's in text which return nan for size returned by render_text()
#this manifests itself by causing the text to render as solid blocks of color that exceed the rectangle bounds.
#           self.headlines = [ row['summary'].encode('utf-8') for row in d.entries ]
    self.headlines = [ row['summary'] for row in d.entries ]    #Get text for each feed entry.
    self.curmessage = 0 #Start at message 0.
    if self.random: #If randomizing entries then shuffle the list.
      random.shuffle(self.headlines)
    self.setmsg(self.headlines[self.curmessage])    #Set the 1st message and start the scrolling.
    self.uddone.set()   #Tell the main thread we are done loading.

  ###Determine if text image needs updating.
  def updatedesplaytext(self):
    if self.lletter != self.lletterimg or self.rletter != self.rletterimg:
      self.lletterimg = self.lletter
      self.rletterimg = self.rletter
      self.displaytext = self.text[self.lletter : self.rletter]   #Get new substr.
      self.displaytextimg = render_text(self.displaytext, font_size=fontsize) #Create text image.
      self.displaytextrect.w = self.displaytextimg[1].w   #Set the text width.  Height doesn't change.

  ###Chop character from front of string if out of the display area.
  def chop(self):
    #Loop until the text is within the display area.
    while self.displaytextrect.x <= self.leftrect.x:
      #If there are any letters left in the text.
      if self.lletter < self.letters:
        lt = self.text[self.lletter] #Get the current leftmost letter.
        #Render it so we can adjust the rectangle by the width of the character.
        timg = render_text(lt, font_name='ArialMT' ,font_size=fontsize)
        self.displaytextrect.x += max(0,min(fontsize, timg[1].w))
        self.lletter += 1   #Next letter.

  ###Add character to end of string if a new character is needed.
  def add(self):
    r = self.displaytextrect.right()
    if r <= self.rightrect.left(): #If the right position is < the left side of the end cap add a letter.
      self.rletter += 1
      if self.rletter >= self.letters:    #If out of letters show next message.
        self.nextmessage()

  ###Add next message to current display text.
  def nextmessage(self):
    self.curmessage += 1    #Next message.
    if self.curmessage & 1: #Every other message is a ...
      self.setmsg('...   ')
    else:
      cm = self.curmessage / 2    #Since every other message is ... index into headlines list is curmessage / 2.
      #If out of messages queue up download.
      if cm >= len(self.headlines):
        self.getheadlines()
      else:
        self.setmsg(self.headlines[cm])

  ###Add the given text to display text.
  def setmsg(self, msg):
    self.text = self.text[self.lletter:] + msg  #Add the text but also shop unneeded text off of front.
    self.letters = len(self.text)   #Get # of letters in the string.
    self.rletter -= self.lletter    #Adjust the right letter index to be relative to new start of string.
    self.lletter = 0    #Reset string start.

  ###Update state waits for data download.
  def waitfordata(self, dt):
    if self.uddone.is_set():    #If the update done event is set.
      self.state = self.scrollstate   #Switch to scrolling state.
      ttl = render_text(self.title)   #Convert title to image.
      self.titleimg = ttl[0]
      self.titlerect.w = ttl[1].w
      self.titlerect.h = ttl[1].h
      self.uddone.clear() #Reset the update event for the next download.
    return False    #Return false to indicate we are waiting for a download.

  ###Update state scrolls text.
  def scrollstate(self, dt):
    self.displaytextrect.x -= dt * self.scrollspeed #Update scroll position.
    self.chop() #Chop letter from left if out of display area.
    self.add()  #Add letter to right if more data needed.
    self.updatedesplaytext()    #Make sure image of text is up to date.
    return True #Return true to indicate we are displaying.

  ###Update the rss feed system.
  def update(self, dt): return self.state(dt)

  ###Draw the RSS feed text.
  def draw(self):
#       fill(0,0,0)
#       rect(*self.textarea)    #This is usefull if the whole screen is not cleared each frame.

    #If display text exists render it.
    if self.displaytextimg[0]:
      tint(*self.textcolor)
      image(self.displaytextimg[0], *self.displaytextrect)

    tint(*self.textcolor)
    #Render left/right caps.
    image(self.lend, *self.leftrect)
    image(self.rend, *self.rightrect)

    #If we have title text image render it.
    if self.titleimg:
      image(self.titleimg, *self.titlerect)
    elif self.title:    #Otherwise display the title text.
      text(self.title, x=self.titlerect.x, y=self.titlerect.y, alignment=9)

class MyScene(Scene):
  ###The scene containing scrolling RSS feeds.
  def setup(self):
    global ldthread
    x = 100 #Start 100 units in from left.
    r = Rect(x, 100, self.size.w - x, fontsize)
    sp = Point(50, 0)   #Use Point to hold scroll speed so it is available in addfeed by reference.
    self.feeds = []

    #Start the loading thread.
    ldthread = Thread(target=loadthread)
    ldthread.start()

    #Local function to add an RSS feed to the feeds list.
    def addfeed(u, c, img, rand = True):
      f = scrolltext(r, u)    #Create scroll text instance.
      f.rend = img    #Set right end cap to given image.
      f.random = rand #Set message randomization.
      f.textcolor = c #Set color for text.
      f.scrollspeed = sp.x    #Set scroll speed using the sp.x value.
      self.feeds.append(f)    #Add object to feeds list.
      r.y += 75   #Move the rectangle up.
      r.x -= 25   #And to the left.
      r.w += 25   #Keep right side at same point.
      sp.x += 10  #Increase scroll speed.

    #Add the following RSS feeds.
    addfeed('http://feeds.bbci.co.uk/news/world/rss.xml', Color(0.00, 1.00, 0.00), 'Blue_Circle')
    addfeed('http://www.nytimes.com/services/xml/rss/nyt/US.xml', Color(1.00, 0.50, 0.00), 'Personal_Computer')
    addfeed('http://www.nytimes.com/services/xml/rss/nyt/Europe.xml', Color(1.00, 0.00, 0.00), 'Delivery_Truck')
    addfeed('http://www.kffl.com/printRSS.php/nfl-articles', Color(0.00, 1.00, 0.50), 'American_Football', False)

#http://www.nytimes.com/services/xml/rss/nyt/Science.xml

  ###Update all RSS feed displays.
  def update(self):
    ud = 0  #Keep count of how many are scrolling vs loading.
    for f in self.feeds:
      ud += f.update(self.dt)
    if ud < len(self.feeds):    #If any feeds are loading sleep for a bit to let the loading thread update.
      sleep(1.0 if ud == 0 else 0.02)

  ###Draw all RSS feeds.
  def draw(self):
    background(0, 0, 0) #Clear the frame. If you take this out put the rect() call back in in scrolltext.draw().
    self.update()   #Update the feeds.
    for f in self.feeds:    #Draw the feeds.
      f.draw()

run(MyScene())