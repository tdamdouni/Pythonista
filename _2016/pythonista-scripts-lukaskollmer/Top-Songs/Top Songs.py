# coding: utf-8
from objc_util import *
import console
import ui
import sys

console.clear()


number_of_songs = 100
dismiss_after_selection = True


class Song(object):
	def __init__(self, title, albumTitle, playCount, persistentID, objcMediaItem):
		self.title = title
		self.albumTitle = albumTitle
		self.playCount = playCount
		self.persistentID = persistentID
		self.objcMediaItem = objcMediaItem
	
	def __str__(self):
		return '{0} | {1} ({2})'.format(self.playCount, self.title, self.albumTitle)

importFramework('MediaPlayer')

MPMediaQuery = ObjCClass('MPMediaQuery')
MPMediaItemCollection = ObjCClass('MPMediaItemCollection')
MPMediaPropertyPredicate = ObjCClass('MPMediaPropertyPredicate')
MPMusicPlayerController = ObjCClass('MPMusicPlayerController')
UITableViewController = ObjCClass('UITableViewController')
UIViewController = ObjCClass('UIViewController')
UIPopoverController = ObjCClass('UIPopoverController')
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')
UIColor = ObjCClass('UIColor')
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
NSNumber = ObjCClass('NSNumber')
UISwitch = ObjCClass('UISwitch')
UIImage = ObjCClass('UIImage')

songsQuery = MPMediaQuery.songsQuery()

systemPlayer = MPMusicPlayerController.systemMusicPlayer()

songs = []
repeat_switch = None

for collection in songsQuery.valueForKey_('collections'):
	for mediaItem in collection.valueForKey_('items'):
		title = mediaItem.valueForKey_('title')
		album = mediaItem.valueForKey_('albumTitle')
		playCount = int(str(mediaItem.valueForKey_('playCount')))
		persistentID = mediaItem.valueForKey_('persistentID')
		song = Song(title, album, playCount, persistentID, mediaItem)
		artwork_object = mediaItem.valueForKey_('artwork')
		if artwork_object:
			song.artwork = artwork_object.imageWithSize_(CGSize(200, 200))
		else:
			song.artwork = UIImage.alloc().init()
		songs.append(song)
			

songs.sort(key=lambda x: x.playCount, reverse=True)

songs = songs[:number_of_songs]


UITableView = ObjCClass('UITableView')
UIViewController = ObjCClass('UIViewController')
UITableViewCell = ObjCClass('UITableViewCell')


def tableView_numberOfRowsInSection_(_self, _cmd, _tv, section):
	return len(songs)

tableView_numberOfRowsInSection_.encoding = 'q0@0:0@0@0'
tableView_numberOfRowsInSection_.restype = c_long


def tableView_cellForRowAtIndexPath_(_self, _cmd, _tv, _ip):
	cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(1, 'Cell')
	row = ObjCInstance(_ip).row()
	song = songs[row]
	cell.textLabel().setText_('{0}'.format(song.title))
	cell.detailTextLabel().setText_('{0}'.format(song.playCount))
	cell.setAccessoryType_(4)
	try:
		cell.imageView().setImage_(song.artwork)
	except:
		pass
	return cell.ptr
	
tableView_cellForRowAtIndexPath_.encoding = '@0@0:0@0@0'


def tableView_didSelectRowAtIndexPath_(_self, _cmd, _tv, _ip):
	row = ObjCInstance(_ip).row()
	song = songs[row]
	play_song(song)
	
	if dismiss_after_selection:
		ObjCInstance(_self).dismissViewControllerAnimated_completion_(True, None)

		
tableView_didSelectRowAtIndexPath_.encoding = '@0@0:0@0@0'


def tableView_accessoryButtonTappedForRowWithIndexPath_(_self, _cmd, _tv, _ip):
	view = ObjCInstance(_self)
	row = ObjCInstance(_ip).row()
	
	cell = ObjCInstance(tableView_cellForRowAtIndexPath_(_self, None, _tv, _ip))
	
	accessory_view = ObjCInstance(cell.valueForKey_('_accessoryView'))
	
	song = songs[row]
	song_info_view = ui.load_view('SongInfo')
	ObjCInstance(song_info_view['artworkImageView']).setImage_(song.artwork)
	song_info_view['song_title_label'].text = str(song.title)
	song_info_view['song_album_label'].text = str(song.albumTitle)
	song_info_view['song_playcount_label'].text = str(song.playCount)
	
	song_info_view.present('popover')
	

tableView_accessoryButtonTappedForRowWithIndexPath_.encoding = '@0@0:0@0@0'


def dismiss(_self, _cmd):
	vc = ObjCInstance(_self)
	vc.dismissViewControllerAnimated_completion_(True, None)
	

def play_song(song):
	collection = MPMediaItemCollection.collectionWithItems_(ns([song.objcMediaItem]))
	systemPlayer.setQueueWithItemCollection_(collection)
	repeat = repeat_switch.isOn()
	systemPlayer.setRepeatMode_(2 if repeat else 0)
	systemPlayer.play()


@on_main_thread
def main():
	global repeat_switch
	
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	methods = [tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, tableView_didSelectRowAtIndexPath_, tableView_accessoryButtonTappedForRowWithIndexPath_, dismiss]
	protocols = ['UITableViewDataSource', 'UITableViewDelegate']
	CustomViewController = create_objc_class('CustomViewController', UIViewController, methods=methods, protocols=protocols)
	vc = CustomViewController.new().autorelease()
	vc.title = 'Top Songs'
	table_view = UITableView.alloc().initWithFrame_style_(((0, 0), (0, 0)), 0)
	table_view.setDataSource_(vc)
	table_view.setDelegate_(vc)
	vc.view = table_view
	repeat_message = UIBarButtonItem.alloc().initWithTitle_style_target_action_('Repeat', 0, None, None)
	repeat_message.setTintColor_(UIColor.blackColor())
	repeat_switch = UISwitch.alloc().init()
	repeat_switch.setOn_animated_(True, False)
	repeat_switch_bar_button_item = UIBarButtonItem.alloc().initWithCustomView_(repeat_switch)
	vc.navigationItem().setLeftBarButtonItems_([repeat_message, repeat_switch_bar_button_item])
	closeButton = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(0, vc, sel('dismiss'))
	navController = UINavigationController.alloc().initWithRootViewController_(vc)
	vc.navigationItem().setRightBarButtonItem_(closeButton)
	vc.setModalPresentationStyle_(0) #2 for form sheet
	navController.setModalPresentationStyle_(0)
	tabVC.presentViewController_animated_completion_(navController, True, None)
	#tabVC.addTabWithViewController_(vc)

if __name__ == '__main__':
	main()
