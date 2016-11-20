import clipboard, console, speech, ui

lang = 'en-GB'
speed = 0.1

lang_dict = {
	'American'   : 'en-US',
	'British'    : 'en-GB',
	'Italian'    : 'it-IT',
	'Spanish'    : 'es-MX',
	'Australian' : 'en-AU',
	'Japanese'   : 'ja-JP',
	'German'     : 'de-DE' }

def table_action(sender):
	global lang
	prev_lang = lang
	selected_lang = sender.items[sender.selected_row]
	lang = lang_dict.get(selected_lang, lang)
	if lang not in ('en-US', prev_lang):  # workaround for bug
		speech.say('workaround', lang, speed)

def slider_action(sender):
	global speed
	speed = v['slider1'].value

def button_speak_action(sender):
	global speed
	text = v['user_text'].text
	if text == 'Enter your text here':
		text = 'Please tell me something to say.'
	speech.say(text, lang, speed)

def copy_action(sender):
	text = v['user_text'].text
	if text == 'Enter your text here':
		console.hud_alert('No text entered to copy.', 'error', 1.0)
	else:
		clipboard.set(text)
		console.hud_alert('Copied', 'success', 1.0)
		
def paste_action(sender):
	text = clipboard.get()
	if text:
		console.hud_alert('Pasted', 'success', 1.0)
		v['user_text'].text = text

def make_button_item(image_name, action):
	button_item = ui.ButtonItem()
	button_item.image = ui.Image.named(image_name)
	button_item.action = action
	return button_item

v = ui.load_view('speech')

speak = make_button_item('ionicons-ios7-volume-high-32', button_speak_action)
copy  = make_button_item('ionicons-ios7-copy-32',        copy_action)
paste = make_button_item('ionicons-clipboard-32',        paste_action)

speech.say('Greetings.', lang, 0.1)
v['languages'].data_source.items = sorted([x for x in lang_dict])
v['languages'].scroll_enabled = False
v.right_button_items = [speak, copy, paste]
v.present(orientations=['landscape'])
