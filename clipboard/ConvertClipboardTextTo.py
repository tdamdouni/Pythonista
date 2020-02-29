from __future__ import print_function
import sys
import re
import urllib
import clipboard

def titleCase(s):
	newText = re.sub(r"[A-Za-z]+('[A-Za-z]+)?",lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),s)
	return newText
	
print("Convert to:")
print("[1] Title Case")
print("[2] lowercase")
print("[3] UPPERCASE")
print("[4] Capital case")
print("[5] Strip Leading")
print("[6] Strip Trailing")
print("[7] Strip All")
print("[8] URL Quote")
print("[x] Exit")

formatType = raw_input("Select Conversion: ")
if formatType == "x":
	print("Exited")
else:

	#userInput = getClipboardData()
	userInput = clipboard.get()
	
	#userInput = raw_input("Input String: ")
	print("\n\n")
	
if formatType == "1":
	outString =  titleCase(userInput)
elif formatType == "2":
	outString = userInput.lower()
elif formatType == "3":
	outString = userInput.upper()
elif formatType == "4":
	outString = userInput.capitalize()
elif formatType == "5":
	outString = userInput.lstrip()
elif formatType == "7":
	outString = userInput.strip()
elif formatType == "8":
	outString = urllib.quote(userInput)
print (outString)
print("\nThe text was copied to the clipboard")
clipboard.set(outString)

