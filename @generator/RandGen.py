import random
import sys
import clipboard
import console
import webbrowser

numArgs = len(sys.argv)

# Accepts input from Drafts; if none present, or if script is run directly in Pythonista, prompts user to input the upper limit of the desired numeric range
if numArgs == 2:
	digit = sys.argv[1]
else:
	digit = console.input_alert('Input the upper limit of your range...', '(as an integer)')

digit = digit.replace(",", "")
digit = int(digit)

# Selects a random digit in the specified range.
num = random.randint(1, digit)

# Sets the output to the clipboard.
num = str(num)
clipboard.set(num)

# Sends output to Drafts, if the script was launched from there; otherwise sends output to an iOS alert.
if numArgs == 2:
	url = 'drafts://x-callback-url/create?text='
	text = 'Your%20random%20number%20is%3A%20'
	webbrowser.open(url + text + num)
else:
	console.alert('Your number' + ' (' + num + ') ' + 'has been sent to the clipboard.', 'Tap CANCEL to dismiss.')
