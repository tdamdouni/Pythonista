# coding: utf-8
# @tdamdouni gists
# https://gist.github.com/a0e67a56b448163e90d7a05bb0d1f258

# https://gist.github.com/b00giZm/cc704ba2a96e4a319e9e

from __future__ import print_function
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
        print('Running in Pythonista app, using test data...\n')
        text = '''## Daring Fireball

John thanking Makerbase.

> My thanks to Makerbase for sponsoring last week’s DF RSS feed. Makerbase is like an IMDB for people who make apps, websites, and podcasts. New features include the ability to get notified — optionally! — when your friends make a new project, or when someone says you inspire them.


(Source: [http://daringfireball.net/](http://daringfireball.net/))'''
    else:
        text = appex.get_text()
    if text:
        author          = 'Pascal Cremer'

        github_repo     = 'b00gizm.github.io'
        github_user     = 'b00gizm'
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
        print('No input text found.')

if __name__ == '__main__':
    main()
