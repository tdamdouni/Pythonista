import console, contacts, feedparser, sys, urllib, webbrowser
console.clear()
outp = ['**{}**\n{}'.format(p.full_name, p.note)
           for p in contacts.get_all_people() if p.note]
if not outp:
    sys.exit('No output!!')
dayone_entry = 'Address Book Notes\n{}\n\n#people'.format('\n\n'.join(outp))
print(dayone_entry)
if not raw_input('-- Press enter to import'):
    dayone_entry = urllib.quote(dayone_entry.encode('utf-8'))
    webbrowser.open('dayone://post?entry=' + dayone_entry)
