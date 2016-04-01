# https://gist.github.com/rjames86/79f857f427599f6e145c
import contacts
import sys, os
import console
sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')]
from dropboxlogin import get_client
from datetime import datetime

# Update this path here for the backup
# location in your Dropbox account. 
BACKUP_PATH = '/Backups/Contacts'

TODAY = datetime.today().strftime('%Y-%m-%d')

dropbox_client = get_client()

VCARD = "".join(person.vcard for person in contacts.get_all_people())

console.clear()

dropbox_client.put_file(BACKUP_PATH + '/contacts {}.vcf'.format(TODAY), VCARD)
print 'Backup complete!'
