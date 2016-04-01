# https://gist.github.com/Gerzer/347941cc813c1edc528b

# coding: utf-8

# Some ideas on:
#- obtaining sys.args up front to fast fail if none are supplied and to make their purpose clear
#- using posts_dir variable to avoid hard coding the same string in four places
#- using with open to ensure that files are closed even if exceptions are thrown
#- using str.format() to speed up and simplify string concatenation
#- comments on the lack of clarity around the variable 'name'.
#- getting rid of the users GitHub password as soon as possible
#- Also, stpt is a weak name. It would be better to have a more understandable script name.

from stash import stash
import console
import datetime
import os
import sys
post_name, post_content = sys.argv[:2]
posts_dir = '_posts'
console.show_activity('Initializing StaSh...')
shell = stash.StaSh()
console.hide_activity()
console.show_activity('Pulling from GitHub...')
shell('cd Pythonista-Tools')
shell('git pull')
console.hide_activity()
console.show_activity('Switching to gh-pages...')
shell('git checkout gh-pages')
if not os.path.exists(posts_dir):
  console.hide_activity()
  console.show_activity('Creating posts directory...')
  shell('mkdir {}'.format(posts_dir))
shell('cd {}'.format(posts_dir))
console.hide_activity()
console.show_activity('Writing data to file...')
now = datetime.datetime.now()
file_name = '{}-{}-{}-{}'.format(now.year, now.month, now.day, post_name)
with open(file_name, 'w') as file_obj:
    file_obj.write(post_content)
console.hide_activity()
console.show_activity('Staging files...')
shell('cd ..')
shell('git add "{}/{}"'.format(posts_dir, file_name))
console.hide_activity()
name = console.input_alert('Enter name to commit as')  # unclear.  is it the git username, forum username, postname, other?
email = console.input_alert('Enter email to commit as')  # if git username then why not just use username below instead
console.show_activity('Committing to gh-pages...')
shell('git commit "Post {} to blog" {} "{}"'.format(post_name, name, email))  # why leave name out of double quotes?
console.hide_activity()
username, password = console.login_alert('Sign in to GitHub', 'Your credentials will NOT be saved.')
console.show_activity('Pushing to GitHub...')
shell('git push -u {}:{}'.format(username, password))
password = None
console.hide_activity()
console.hud_alert('Post successful!', 'success')