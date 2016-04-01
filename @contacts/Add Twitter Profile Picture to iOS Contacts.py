# coding: utf-8

# https://gist.github.com/lukaskollmer/962625208f872c242706

# Load Twitter profile pictures and set them as image to your iOS contacts

# https://forum.omz-software.com/topic/2736/share-code-update-ios-contact-images-with-twitter-profile-pictures

import twitter
import json
import urllib
import contacts
import console
from objc_util import *
import ui
import os
from PIL import Image
import webbrowser

console.clear()

CNContactStore = ObjCClass('CNContactStore')
CNContact = ObjCClass('CNContact')
CNSaveRequest = ObjCClass('CNSaveRequest')
UIActivityIndicatorView = ObjCClass('UIActivityIndicatorView')

activity_indicator = None
twitter_contacts = []
current_contact_index = -1
did_present = False
store = CNContactStore.alloc().init()

view = ui.load_view()
all_view_element_names = [
	'contact_name_label',
	'old_image_title_label',
	'new_image_title_label',
	'left_image_view',
	'right_image_view',
	'keep_image_button',
	'use_new_image_button',
	'progress_view_container'
]


def setup_view():
	view['left_image_view'].content_mode = ui.CONTENT_SCALE_ASPECT_FIT
	view['right_image_view'].content_mode = ui.CONTENT_SCALE_ASPECT_FIT
	
	view['keep_image_button'].action = keep_current_image
	view['use_new_image_button'].action = use_twitter_image
class NoTwitterAccountSetUpError(Exception):
	pass

class LoadTwitterProfilePictureError(Exception):
	def __init__(self, status_code):
		self.status_code = status_code
		
		def __str__():
			return 'Could not retrieve profile image (status: %i)' % (self.status_code,)

class Contact(object):
	def __init__(self, name, twitter_username, has_image, current_image, twitter_image):
		self.name = name
		self.twitter_username = twitter_username
		self.has_image = has_image
		self.current_image = current_image
		self.twitter_image = twitter_image
		
	def __str__(self):
		return 'Contact {} (@{})'.format(self.name, self.twitter_username)
		
def show_message_in_image_view(message, image_view):
	if len(image_view.subviews) > 0: # already a message subview
		for subview in image_view.subviews:
			if type(subview) is ui.Label:
				subview.text = message
	else:
		label = ui.Label()
		label.frame = image_view.frame
		label.text = message
		label.text_color = 0.4
		label.center = ((image_view.width / 2), (image_view.height / 2))
		label.alignment = ui.ALIGN_CENTER
		image_view.add_subview(label)

def profile_picture_for_account(username):
	all_accounts = twitter.get_all_accounts()
	if len(all_accounts) >= 1:
		account = all_accounts[0]
		parameters = {'screen_name': username}
		status, data = twitter.request(account, 'https://api.twitter.com/1.1/users/show.json', 'GET', parameters)
		if status == 200:
			user_info = json.loads(data)
			avatar_url = user_info['profile_image_url']
			# Get the URL for the original size:
			avatar_url = avatar_url.replace('_normal', '')
			filename, headers = urllib.urlretrieve(avatar_url)
			img = Image.open(filename)
			format = img.format.lower()
			path = os.path.expanduser('~/Documents/{}.{}'.format(username, format))
			img.save(path, format=format)
			image = ui.Image.named(path)
			os.remove(path)
			return image
		else:
			raise LoadTwitterProfilePictureError(status)
	else:
		raise NoTwitterAccountSetUpError('You don\'t have any Twitter accounts (or haven\'t given permission to access them).')

def addressBook_account_with_name(name):
	predicate = CNContact.predicateForContactsMatchingName_(name)
	keys_to_fetch = ['identifier', 'givenName', 'familyName', 'imageDataAvailable', 'imageData']
	
	result = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys_to_fetch, None)[0]
	
	return result

def load_contacts_with_twitter():
	contacts_with_twitter = []
	all_people = contacts.get_all_people()
	for person in all_people:
		view['currently_loading_info_label'].text = 'Loading image for {}'.format(person.full_name)
		social = person.social_profile
		if social:
			for service in social:
				if service[1]['service'] == 'twitter':
					twitter_username = service[1]['username']
					should_dismiss_view_because_no_account_error = False
					try:
						twitter_image = profile_picture_for_account(twitter_username)
					except LoadTwitterProfilePictureError as error:
						twitter_image = None
					except NoTwitterAccountSetUpError as error:
						twitter_image = None
						should_dismiss_view_because_no_account_error = True
						if console.alert(error.message, button1='open settings') == 1:
							webbrowser.open('app-settings://')
						view.close()
					finally:
						if should_dismiss_view_because_no_account_error == True:
							view.close()
					image = None
					result = addressBook_account_with_name(person.full_name)
					has_image = result.imageDataAvailable()
					if has_image == True:
						data = NSData.dataWithData_(result.imageData())
						image = UIImage.imageWithData_(data)
					contacts_with_twitter.append(Contact(person.full_name, twitter_username, has_image, image, twitter_image))
	return contacts_with_twitter

def update_contact_with_name_set_new_image(name, image):
	contact = addressBook_account_with_name(name).mutableCopy()
	image_data = bytearray(image.to_png())
	contact.imageData = image_data
	save_resuest = CNSaveRequest.new()
	save_resuest.updateContact_(contact)
	store.executeSaveRequest_error_(save_resuest, None)
	
def current_contact():
	if current_contact_index <= len(twitter_contacts):
		return twitter_contacts[current_contact_index]
	else:
		return None
	
def show_next_contact():
	global current_contact_index
	current_contact_index = current_contact_index + 1
	if current_contact_index >= len(twitter_contacts):
		view.close()
		return
	contact = current_contact()
	view['contact_name_label'].text = contact.name
	if contact.current_image is None:
		left_message = 'No image set'
	else:
		left_message = ''
	show_message_in_image_view(left_message, view['left_image_view'])
	ObjCInstance(view['left_image_view']).image = contact.current_image
	if contact.twitter_image is None:
		right_message = 'Unable to load image'
	else:
		right_message = ''
	show_message_in_image_view(right_message, view['right_image_view'])
	view['right_image_view'].image = contact.twitter_image
	view['use_new_image_button'].enabled = not contact.twitter_image == None

	
def keep_current_image(sender):
	show_next_contact()

def use_twitter_image(sender):
	contact = current_contact()
	name = contact.name
	new_image = view['right_image_view'].image
	update_contact_with_name_set_new_image(name, new_image)
	show_next_contact()
	
def set_all_views_hidden(hidden):
	for element in all_view_element_names:
		view[element].hidden = hidden

@on_main_thread
def show_ui(loading):
	global did_present
	global activity_indicator
	if did_present == False:
		try:
			view.present('sheet')
			did_present = True
		except:
			pass
	set_all_views_hidden(loading)
	if loading:
		activity_indicator = UIActivityIndicatorView.alloc().initWithActivityIndicatorStyle_(2) #2= grey style
		activity_indicator.startAnimating()
		activity_indicator_container = ObjCInstance(view['progress_view_container'])
		activity_indicator.center = activity_indicator_container.convertPoint_fromView_(activity_indicator_container.center(), activity_indicator_container.superview())
		activity_indicator_container.addSubview_(activity_indicator)
	else:
		activity_indicator.stopAnimating()
		show_next_contact()
	view['progress_view_container'].hidden = not loading
	view['currently_loading_info_label'].hidden = not loading

if __name__ == '__main__':
	setup_view()
	show_ui(loading=True)
	twitter_contacts = load_contacts_with_twitter()
	show_ui(loading=False)