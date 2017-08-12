# Mobile Blogging with Pythonista, Jekyll and Github

_Captured: 2015-11-19 at 13:52 from [codenugget.co](http://codenugget.co/2015/11/18/mobile-blogging-with-pythonista-jekyll-and-github.html)_

I've been beta-testing [Ole Zorns](https://twitter.com/olemoritz) new version of his app [Pythonista](http://omz-software.com/pythonista/) for over three weeks now, and it quickly became one of my most favorite iOS apps ever. Pythonista basically started as an app which lets you run Python code on your iPhone or iPad, but since then, evolved into something more much poweful than just a REPL or stripped down IDE: Pythonista ships with some custom modules as wrappers around iOS APIs, which let you script your very own automations and even add custom UI, if you want. Pythonista 1.6 now is in its final beta phase and, at least for me, feels more like a 2.x release than just a minor update. It adds editor tabs, so you can have multiple files open at once, new modules and even a bridge for writing your own Objective-C wrappers (fingers crossed that this ever gets past App Review). But my most favorite new feature is the Pythonista app extension, which a way to run your Python scripts from within every app that supports the native iOS share sheet. When I read about this the first time, I immediately knew that I wanted to use it for optimizing my "on the go" blogging workflow.

## The old workflow

To give you a little bit of context: My blog [codenugget.co](http://codenugget.co) is powered by [Jekyll](https://jekyllrb.com/), an engine written in Ruby for creating static pages from Markdown files, and was originally hosted on [Heroku](https://www.heroku.com/). Here's what I did:

  1. Whenever I started working on a new post, I created a draft inside a special folder inside my [Dropbox](https://www.dropbox.com/), so I would be able to access and edit it from any device I own
  2. Built a custom Docker image containing everything for running the Jekyll development server. I would then run a [Docker](https://www.docker.com/) container based on that image with a volume linked to a directory on my local machine containing the code, which I host on Github.
  3. Created a [Hazel](https://www.noodlesoft.com/hazel.php) action to run on my host machine that monitors my blog code and Dropbox folders and sync new drafts and / or postings back and forth
  4. Whenever I was ready to publish, I'd `git` commit the new post and pushed everything to the `master` branch on [Github](https://github.com/b00giZm/b00gizm.github.io)
  5. Finally, I would then push everything to the `heroku` branch, which would then trigger a rebuild and reload of my Heroku app

Last year, when I started working on this setup, it was a fun and exciting little side project. It took me two days to bring it to a working state -- well, kind of. The Hazel script seemed to only work, when it felt like it. Most of the time, it simply wouldn't trigger automatically. I don't know this was a bug inside Hazel, some weird conditions regarding file events and Dropbox hosted files, or just me not understanding how to correctly use the file creation / modification time attributes for Hazel actions.

But, more importantly, I couldn't publish new posts from my iPhone or iPad, because I would always need Git as my ultimate requirement.

## The new and shiny Pythonista way

First of all, I migrated my blog from Heroku to Github pages, which elimates step 5 from above, because I now just have to push to `master` and Github will pick up all changes and update the contents of my blog. Github pages are free to use and bring a custom `<username>.github.io` subdomain for every user. If you want to use your own domain, just include a `CNAME` file in your repository [and point your domain to Github's servers](https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/). So, in my case, <http://codenugget.co> is now pointing to <http://b00gizm.github.io>.

I then wrote a little script called `MobileBlogger.py`, which can be accessed through the Pythonista app extension. I takes a blob of text, does some magic to determine meta data like the title or the file name, prompts a `dialogs.form_input()` sheets for confirmation, and then uses the `pygithub3` [Python module](https://pygithub3.readthedocs.org/en/latest/) to push everything to Github over their official API.

In my first tests, it worked pretty well and Github picked up the changes almost instantly, which means, that I can now publish new posts from almost every iOS app that supports native text sharing (even the iOS Notes app, if you're really hardcore).

```Python
# http://codenugget.co/2015/11/18/mobile-blogging-with-pythonista-jekyll-and-github.html

# https://gist.github.com/b00giZm/cc704ba2a96e4a319e9e#file-mobileblogger-py

# coding: utf-8

import appex
import console
import keychain
import dialogs
import re

from pygithub3 import Github

from string import Template
from datetime import date
from time import strftime
from unicodedata import normalize

def slug(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)

    return ''.join(strict_text)

def extract_title(text):
    lines = re.split('\n+', text, 2)

    title = re.sub('^#+\s+', '', lines[0])
    if (len(lines) < 2):
        return (title, None)

    index = 1
    if re.search('^(=|-)+$', lines[1]):
        index = 2

    return (title, '\n'.join(lines[index:]))

class MobileBlogger:
    def __init__(self, github_user, github_password, github_repo):
        self.github_user = github_user
        self.github_password = github_password
        self.github_repo = github_repo

        self._latest_commit = None

        self._initialize_client()

    def _initialize_client(self):
        self._gh = Github(
            login=self.github_user,
            user=self.github_user,
            password=self.github_password,
            repo=self.github_repo
        )

    def _get_latest_commit(self, reload=False):
        if self._latest_commit is None or reload:
            self._latest_commit = self._gh.repos.commits.list().next().next()

        return self._latest_commit

    def _prepend_meta_data(self, text, metas):
        template ='''---
layout:     ${layout}
title:      ${title}
author:     ${author}
date:       ${date}
tags:       ${tags}
---

'''
        return Template(template).substitute(metas) + text

    def create_new_post(self, title, text, metas):
        default_metas = {
            'layout': 'post',
            'date': strftime("%Y-%m-%d %H:%M:%S"),
            'title': title
        }

        default_metas.update(metas)
        branch = default_metas['branch']
        filename = default_metas['filename']
        del default_metas['branch']
        del default_metas['filename']

        text = self._prepend_meta_data(text, default_metas)

        latest_commit = self._get_latest_commit()

        # Create blob
        blob = self._gh.git_data.blobs.create(dict(
            content=text, encoding='utf-8'))

        # Create tree
        tree = self._gh.git_data.trees.create(dict(
            base_tree=latest_commit.commit.tree['sha'], tree=[dict(
                path='_posts/' + filename, mode='100644', type='blob', sha=blob.sha)]))

        # Create commit
        commit = self._gh.git_data.commits.create(dict(
            message=('New post: ' + title), tree=tree.sha, parents=[
                latest_commit.sha]))

        #Update reference
        ref = 'heads/%s' % branch
        self._gh.git_data.references.update(ref, dict(
            sha=commit.sha))

    def undo_last_post(self, branch='master'):
        if self._latest_commit is None:
            return

        ref = 'heads/%s' % branch
        self._gh.git_data.references.update(ref, dict(
            sha=self._latest_commit.sha, force=True))

def main():
    if not appex.is_running_extension():
        print 'Running in Pythonista app, using test data...\n'
        text = '''## Daring Fireball

John thanking Makerbase.

> My thanks to Makerbase for sponsoring last week’s DF RSS feed. Makerbase is like an IMDB for people who make apps, websites, and podcasts. New features include the ability to get notified — optionally! — when your friends make a new project, or when someone says you inspire them.


(Source: [http://daringfireball.net/](http://daringfireball.net/))'''
    else:
        text = appex.get_text()
    if text:
        author          = 'Taha Dhiaeddine Amdouni'

        github_repo     = 'tdamdouni.github.io'
        github_user     = 'tdamdouni'
        github_password = keychain.get_password('github', github_user) or ''

        (title, text)   = extract_title(text)
        filename        = '%s-%s.md' % (date.today(), slug(title))

        github_fields = (
            'Github Settings',
            [
                dict(title='Github Username', key='github_user', type='text', value=github_user, autocorrection=False, autocapitalization=False),
                dict(title='Github Password', key='github_password', type='password', value=github_password),
                dict(title='Repository', key='github_repo', type='text', value=github_repo, autocorrection=False, autocapitalization=False)
            ]
        )

        posting_fields = (
            'Post Settings',
            [
                dict(title='Title', key='title', type='text', value=title),
                dict(title='Author', key='author', type='text', value=author),
                dict(title='Layout', key='layout', type='text', value='post', autocorrection=False, autocapitalization=False),
                dict(title='Tags', key='tags', type='text', value=''),
                dict(title='Filename', key='filename', type='text', value=filename, autocorrection=False, autocapitalization=False)
            ],
            'Please seperate tags by spaces.'
        )

        results = dialogs.form_dialog(title='Publish new post', sections=[
            posting_fields,
            github_fields
        ])

        if results is None:
            console.hud_alert('Posting was cancelled', 'error')
            return

        metas = {
            'tags': results['tags'],
            'branch': 'master',
            'author': results['author'],
            'layout': results['layout'],
            'filename': results['filename']
        }

        if github_password != results['github_password']:
            keychain.set_password('github', results['github_user'], results['github_password'])

        console.show_activity()
        mb = MobileBlogger(results['github_user'], results['github_password'], results['github_repo'])
        mb.create_new_post(results['title'], text, metas)
        console.hud_alert('New post created!')
    else:
        print 'No input text found.'

if __name__ == '__main__':
    main()
```
In short:

  1. Prepare a draft for a new post in your favorite text app which supports native sharing
  2. When ready, launch the share sheets, choose the Pythonista action extension and run the `MobileBlogger.py` script
  3. Customize the default values in the then presented confirmation sheet
  4. Hit "Done"

You want see this as a GIF? Sure you do ;)

![mobile-blogger.gif](https://raw.githubusercontent.com/b00giZm/b00gizm.github.io/master/uploads/mobile-blogger.gif)

> _Feel free to fork, use and/or improve my script as you like._

To be honest, I'd really appreciate, if you would send suggestions on how to improve it. Since I have no real Python background, it currently might not be the most idiomatic Python code on the planet (and it's, by no means, anything near feature complete, since you currently can only create new posts and not push updates).

So, if you haven't already, head to the AppStore [and buy Pythonista](https://appsto.re/de/P0xGF.i). I guess it won't take that much longer until version 1.6 leaves its beta state and will be released to the public.
