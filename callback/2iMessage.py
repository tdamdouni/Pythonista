import clipboard, webbrowser
msg = 'This is an important message!!'
tel = ''  # can be a phone number or Apple ID
clipboard.set(msg)       # once iMessage opens, do a Paste into the message body
webbrowser.open('sms:' + tel)
