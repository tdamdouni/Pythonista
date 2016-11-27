# https://forum.omz-software.com/topic/2302/newbie-problem

# coding: utf-8

age = int(raw_input('How old are you?'))
if age < 13:
	print ("You're rather young. Is'nt it your bedtime.")
elif age < 20:
	print ("You are a teenager.")
elif age < 25:
	print ("Are you at university? I studied how to be a computer.")
elif age < 200:
	print ("You are so old. When do you retire?")
else:
	print ("I'm so sorry. I only understand numbers.")

