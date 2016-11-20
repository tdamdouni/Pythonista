# https://gist.github.com/lukf/8982812

import console, datetime, feedparser, sys, urllib, webbrowser
username = 'USERNAME'  # Your username
console.clear()
fmt='{published}\n> [{title}][{i}]\n[{i}]: {link}\n\n'
i = 0
outp = ''
todayString = datetime.date.today().strftime("%Y-%m-%d")
feedURL = 'http://www.rssitfor.me/getrss?name=' + username
for post in feedparser.parse(feedURL).entries:
    if todayString in post.published:
        i += 1
        post['i'] = i
        outp += fmt.format(**post)
if not outp:
    sys.exit('No output!')
dayone_entry = 'Tweets from today\n{}\n#tweeted'.format(outp)
# User confirmation
print(dayone_entry)
if not raw_input('-- Press enter to import'):
    # encode final entry
    dayone_entry = urllib.quote(dayone_entry.encode('utf-8'))
    webbrowser.open('dayone://post?entry=' + dayone_entry)
