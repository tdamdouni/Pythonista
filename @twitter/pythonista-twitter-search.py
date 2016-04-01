import urllib2
import json
from scene import *

class TwitterSearch (Scene):
  def __init__(self, query):
    self.searchResults = []
    self.query = query
    self.searchTwitter(self.query)
    
  # Perform Twitter search and parse JSON response
  def searchTwitter(self, query):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + query
    response = urllib2.urlopen(url).read()
    data = json.loads(response)
    results = data['results']
    self.searchResults = results
  
  # This gets called 60 times a second  
  def draw(self):
    background(0.9, 0.9, 0.9)
    textX = 40
    textY = self.size.h - 40
    
    # Draw heading
    headingText = 'Twitter Search Results for "' + self.query + '"'
    text(headingText, font_name='GillSans-Bold', font_size=24, x=textX, y=textY, alignment=3)
    
    # Draw tweets
    imageX = textX
    imageSize = 40
    textX += 50
    textY -= 50
    for tweet in self.searchResults:
      tint(1.0, 1.0, 1.0)
      image('Alien', imageX, textY - imageSize, imageSize, imageSize)
      tweetAuthor = tweet['from_user_name'] + '(@' + tweet['from_user'] + ') on ' + tweet['created_at']
      tint(0.3, 0.3, 0.3)
      text(tweetAuthor, font_name='GillSans', font_size=14.0, x=textX, y=textY, alignment=3)
      textY -= 20
      tint(0.1, 0.1, 0.1)
      text(tweet['text'], font_name='GillSans', font_size=16.0, x=textX, y=textY, alignment=3)
      textY -= 50

# Run the scene that we just defined
run(TwitterSearch('%40tdamdouni'))