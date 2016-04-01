# This is a Pythonista script that will get all contacts, transfer that into Drafts,
# execute the DRAFTS_ACTION (which creates the vCard in the specified path in that action.
#
# This essentially creates a complete backup of your iOS contacts as a vCard.
#
# (c) 2014 Dexter Ang. MIT License.
#

import contacts
import urllib
import webbrowser

DRAFTS_ACTION = "Backup Contacts"

VCARD = ""
people = contacts.get_all_people()
for person in people:
  VCARD = VCARD + person.vcard

base = "drafts://x-callback-url/create?text="
text = urllib.quote(VCARD, safe='')
action = "&action=" + urllib.quote(DRAFTS_ACTION, safe='')
success = "&x-success="

webbrowser.open(base + text + action + success)
