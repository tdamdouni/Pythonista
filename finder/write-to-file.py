# https://forum.omz-software.com/topic/3291/writing-to-a-file-with-python-in-editorial/3

# In Python, you can always create a new file by writing:

with open('my_cool_file.txt', 'w') as out_file:
	out_file.write('My cool message...')

