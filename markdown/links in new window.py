import clipboard
import re

myString = clipboard.get()
clipboard.set(re.sub(r'(?<!<a target="_blank") href="(?!http://(www\.)?n8henrie\.com)', ' target="_blank" href="', myString))
