# coding: utf-8

# https://forum.omz-software.com/topic/2480/encryption-list-ranges-and-python

#char_dict = ["a","A","b","B","c","C","d","D","e","E","f","F","g","G","h","H","i","I","j","J","k","K","l","L","m","M","n","N","o","O","p","P","q","Q","r","R","s","S","t","T","u","U","v","V","w","W","x","X","y","Y","z","Z","?","!",".",",","_"," "]

#def encrypt(message,key):
#    end_msg = ""
#    through = 0
#    for char in message:
#        end_msg = end_msg + char_dict[char_dict.index(char) + key]
#        through = through + 1
#    return end_msg

#==============================

#import complexx
#print(complexx.encrypt("zebra",15))

#==============================

char_list = ["a","A","b","B","c","C","d","D","e","E","f","F","g","G","h","H","i","I","j","J","k","K","l","L","m","M","n","N","o","O","p","P","q","Q","r","R","s","S","t","T","u","U","v","V","w","W","x","X","y","Y","z","Z","?","!",".",",","_"," "]

def encrypt(message,key):
	end_msg = ""
	through = 0
	for char in message:
		size = (char_list.index(char) + key) % len(char_list)
		end_msg = end_msg + char_list[size]
		through = through + 1
	return end_msg

