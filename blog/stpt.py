# https://gist.github.com/Gerzer/347941cc813c1edc528b

# coding utf-8

# A simple blog post auto-upload script for Pythonista Tools

from stash import stash
import os
import console
import sys
import datetime
console.show_activity('Initializing StaSh...')
shell = stash.StaSh()
console.hide_activity()
console.show_activity('Pulling from GitHub...')
shell('cd Pythonista-Tools')
shell('git pull')
console.hide_activity()
console.show_activity('Switching to gh-pages...')
shell('git checkout gh-pages')
if not os.path.exists('_posts'):
  console.hide_activity()
  console.show_activity('Creating posts directory...')
  shell('mkdir _posts')
shell('cd _posts')
console.hide_activity()
console.show_activity('Writing data to file...')
now = datetime.datetime.now()
file_name = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + sys.argv[1]
file_obj = open(file_name, 'w')
file_obj.write(sys.argv[2])
file_obj.close()
console.hide_activity()
console.show_activity('Staging files...')
shell('cd ..')
shell('git add "_posts/' + file_name + '"')
console.hide_activity()
name = console.input_alert('Enter name to commit as')
email = console.input_alert('Enter email to commit as')
console.show_activity('Committing to gh-pages...')
shell('git commit "Post ' + sys.argv[1] + ' to blog" ' + name + ' "' + email + '"')
console.hide_activity()
username, password = console.login_alert('Sign in to GitHub', 'Your credentials will NOT be saved.')
console.show_activity('Pushing to GitHub...')
shell('git push -u ' + username + ':' + password)
console.hide_activity()
console.hud_alert('Post successful!', 'success')