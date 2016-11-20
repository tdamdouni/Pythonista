# https://forum.omz-software.com/topic/3291/writing-to-a-file-with-python-in-editorial/6

with open('my_cool_file.txt', 'w') as out_file:
	out_file.write('My cool message...')
# --------------------
import os
print(os.getcwd())  # https://docs.python.org/2/search.html?highlight=os.getcwd#os.getcwd
print(os.listdir(os.curdir))  # https://docs.python.org/2/library/os.html?highlight=os.listdir#os.listdir
print(os.listdir(os.pardir))  # https://docs.python.org/2/library/os.html?highlight=os.curdir#os.curdir
# --------------------

