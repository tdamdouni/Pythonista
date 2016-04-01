#coding: utf-8

import markdown2
from string import Template
import os

CSS = u""".content { max-width: 90%; margin-left: auto; margin-right: auto; }
body { font-size: 100%; }
p li { font-size: 1em; }
"""

BASE = u"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
      $title
      $head
  </head>
  <body>
    <div class="flag">
      <div class="blog_title">
        <span class="title_text"><a style="color: inherit; text-decoration: none;" href="/">0x38b</a></span>
      </div>
    </div>
    <div class='content'>
      $content
    </div>
  </body>
</html>
"""

POST = u"""<h1 class='post_title'>$title</h2>
<article>
$post
</article>
"""

INDEX = u"""<div class='post_index'>
  <p class='index_header'>Posts:</p>
  <ul>
    $links
  </ul>
</div>
"""
  

def get_css_links():
  links = []
  for file in os.listdir('static/css'):
    link = '<link rel="stylesheet" href="/css/{file}">'.format(file=file)
    links.append(link)
  return '\n'.join(links)
  
def markdown_to_html(post_content):
  extras = ['code-friendly', 'fenced-code-blocks']
  return markdown2.markdown(post_content, extras)

def make_post(post):
  # Fill in the post template
  post_html = markdown_to_html(post.content)
  t = Template(POST)
  post_html = t.substitute(title=post.title, post=post_html)
  
  # Fill in base html template with post and head content
  title = u'<title>{}</title>'.format(post.title)
  css = get_css_links()
  t = Template(BASE)
  page = t.substitute(title=title, head=css, content=post_html)
  
  return page
  
def get_index(posts):
  links = []
  for post in posts:
    date = post.date
    link = u'<li>' + u'<a href="/{slug}/">{date:%d/%m/%Y} - {title}</a>'.format(slug=post.slug, date=date, title=post.title) + u'</li>'
    links.append(link)
  t = Template(INDEX)
  index = t.substitute(links='\n'.join(links))
  
  title = u'<title>Posts</title>'
  css = get_css_links()
  t = Template(BASE)
  page = t.substitute(title=title, head=css, content=index)
  return page
 
#test_posts = [{'date': '30/04/2015', 'post': 'This is a test', 'slug': 'test-post', 'title': 'Test'}, {'date': '05/05/2015', 'post': 'This is another test', 'slug': 'test-number-two', 'title': 'Test'}]
#test_post = 'title: Test\ndate: 30-04-2015\nslug: test-post\n====\nThis is a test'

# print 'got it, type: {}'.format(type(index))
#print index
#from blok import get_post
#post = get_post(test_post)
#index = get_index([post])
#print index
#print make_post(post)
