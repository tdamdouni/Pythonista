# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2734/contacts-module-access-profile-picture/4

from __future__ import print_function
from objc_util import *
from ctypes import string_at
import contacts
import ui
import photos

# CHANGE THIS:
CONTACT_NAME = 'John Doe'

# Easier to do the authorization with the contacts module (this also authorizes the Contacts.framework):
if not contacts.is_authorized():
	# This implicitly shows the permission dialog, if necessary:
	contacts.get_all_groups()
	
# Load classes we need from Contacts.framework:
NSBundle.bundleWithPath_('/System/Library/Frameworks/Contacts.framework').load()
CNContactStore = ObjCClass('CNContactStore')
CNContact = ObjCClass('CNContact')
CNSaveRequest = ObjCClass('CNSaveRequest')

def main():
	store = CNContactStore.alloc().init().autorelease()
	# Find the first contact that matches the name.
	pred = CNContact.predicateForContactsMatchingName_(CONTACT_NAME)
	fetch_keys = ['imageDataAvailable', 'imageData']
	people = store.unifiedContactsMatchingPredicate_keysToFetch_error_(pred, fetch_keys, None)
	if not people:
		print('No person found with the name "%s"' % (CONTACT_NAME,))
		return
	p = people[0]
	has_image = p.imageDataAvailable()
	if has_image:
		# Show the existing picture of the contact:
		img_data = p.imageData()
		img_data_str = string_at(img_data.bytes(), img_data.length())
		img = ui.Image.from_data(img_data_str)
		img.show()
	# Pick a new image from photos:
	new_img_data = photos.pick_image(raw_data=True)
	if new_img_data:
		# Note: objc_util automatically converts bytearray to NSData
		new_img_bytes = bytearray(new_img_data)
		# Create a mutable copy of the fetched contact...
		mutable_contact = p.mutableCopy().autorelease()
		# Assign new image data...
		mutable_contact.imageData = new_img_bytes
		contacts.save()
		# Create a save request for he contact, and execute it...
		save_req = CNSaveRequest.new().autorelease()
		save_req.updateContact_(mutable_contact)
		store.executeSaveRequest_error_(save_req, None)
		
if __name__ == '__main__':
	main()
