#!/usr/bin/env python
#coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

# Python imports
from datetime import datetime
from sys import argv
import io
import os
import shutil

# Pythonista modules
import webbrowser
import clipboard

# Blok modules
import template

STATIC_DIR = 'static/'
POSTS_DIR = 'posts/'
OUTPUT_DIR = 'output/'

class blog_post():
  def __init__(self, title, slug, content, date=None):
    self.title = title
    self.content = content
    self.slug = slug
    self.has_hour = False
    if date is not None:
      self.date = self._parse_date(date)
    else:
      self.date = datetime.today()

  def _parse_date(self, date):
    # Parse a date like '30/04/2015 15:22', with or without the hour
    # If the post had a time, set has_hour; otherwise, don't use the time
    if ' ' in date:
      self.has_hour = True
      fmt = '%d-%m-%Y %H:%M'
    else:
      self.has_hour = False
      fmt = '%d-%m-%Y'
    return datetime.strptime(date, fmt)

  def get_filename(self):
    return '{:%d-%m-%Y}-{}.markdown'.format(self.date, self.slug)

  def prepare_post(self):
    date = self.get_date()
    return """title: {}
date: {}
slug: {}
====
{}
""".format(self.title, date, self.slug, self.content)
    
def read_file(file_path):
  with io.open(file_path, mode='r', encoding='utf_8') as in_file:
    return in_file.read().decode('utf8')

def write_file(path, filename, content):
  make_dirs(path)
  with io.open(os.path.join(path, filename), mode='w', encoding='utf_8') as out_file:
    out_file.write(content)
      
def make_dirs(path):
  # If the destination dir(s) don't already exist, create them
  if not os.path.isdir(path):
    os.makedirs(path)
  return True
  
def get_all_files(path):
  files = []
  for filename in os.listdir(path):
    # Without this check, we try to 'read' directories
    if os.path.isfile(os.path.join(path, filename)):
      file = read_file(os.path.join(path, filename))
      files.append(file)
  return files

def get_metadata(line, prefix):
  if line.startswith(prefix):
    # title: Long title here! -> ['Long', 'title', ... ] -> 'Long title ...'
    line = ' '.join(line.split()[1:])
    # We don't want an empty string
    if line:
      return line
  return False

def get_post_dict(post):
  """Reads an existing post and returns a dictionary.
  { title, date, slug, post }"""
  post_dict = dict()
  prefixes = ['title', 'date', 'slug']
  
  for line in post.split('\n'):
    for prefix in prefixes:
      data = get_metadata(line, prefix)
      
      if data:
        post_dict[prefix] = data
        # We got what we came for
        break

    if line.startswith('===='):
      post_start = post.index('====') + 5
      post_dict['content'] = post[post_start:]
      break

  # We need at least a title, slug, and post. We can make the date.
  if 'title' in post_dict and 'slug' in post_dict and 'content' in post_dict:
    return post_dict
  else:
    return False

def get_post(post_text):
  p = get_post_dict(post_text)
  if p:
    return blog_post(title=p['title'], content=p['content'], date=p['date'], slug=p['slug'])
  else:
    return False

def create_post(post_text):
  """Takes a post from Editorial and writes it to the posts dir as a .md file.
  Format:
    tite:
    date:
    slug:
    ====
    (content here)
  """
  post = get_post(post_text)
  if post:
    filename = post.get_filename()
    prepared_post = post.prepare_post()
    write(POSTS_DIR, filename, prepared_post)
    return True  
  else:
    print('Failed to parse the post.')
    return False
  
def build_site():
  # Load and write each post to the output dir
  files = get_all_files(POSTS_DIR)
  posts = []
  for file in files:
    post = get_post(file)
    post_html = template.make_post(post)
    path = os.path.join(OUTPUT_DIR, '{}/'.format(post.slug))
    filename = 'index.html'
    write_file(path, filename, post_html)
    # We need to pass the post objects to get_index
    posts.append(post)
  
  # Get and write index.html
  index = template.get_index(posts).decode('utf8')
  # print repr(index)
  # print 'in build site, type of index: {}'.format(type(index))
  write_file(OUTPUT_DIR, 'index.html', index)
  
  # Copy static resources
  css_dir = os.path.join(STATIC_DIR, 'css/')
  css_files = os.listdir(css_dir)
  dest = os.path.join(OUTPUT_DIR, 'css/')
  for file in css_files:
    source = os.path.join(css_dir, file)
    # Make sure we're working on a file
    if os.path.isfile(source):
      # Make all the dirs up to '/output/css' if needed
      if not os.path.isdir(dest):
        os.makedirs(dest)
      shutil.copy(source, dest)

def clean_site():
  print('TODO')

def main(command, *args):
  if command == 'build':
    build_site()
  elif command == 'clean':
    clean_site()
  elif command == 'add':
    post = clipboard.get()
    if post:
      # It's already unicode, so no need to decode
      success = create_post(post)
      webbrowser.open('editorial://workflow-callback/?success={}'.format(success))
    else:
      print('Nothing on clipboard')
      webbrowser.open('editorial://workflow-callback/?success=False')
  elif command == 'help':
    print("""Blok is a small static site generator.

    Arguments:
      help    - this help.
      add     - add a blog post. Input is the text of a blog post in markdown on the clipboard
      build   - write all posts in posts/ dir to site/ as html files, and create index.html
      clean   - deletes all files and directories from the output dir""")

if __name__ == '__main__':
  # if we have at least a command
  main(argv[1:] or 'add')