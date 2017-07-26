# https://stackoverflow.com/questions/13459856/how-can-i-create-a-simple-python-brute-force-function

gen = itertools.combinations_with_replacement(characters,password_length) #1
for password in gen:                                                      #2 
    check_password(password)                                              #3

import random
a_z = "abcdefghijklmnopqrstuvwxyz_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
while password != curtry:
    currenttry = random.choice(a_z)+random.choice(a_z)+random.choice(a_z)+random.choice(a_z)
