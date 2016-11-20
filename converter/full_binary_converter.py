# coding: utf-8

# https://github.com/philipkalinda

# binary_converter: This converts your text (without punctuation - except ',' and '.') into binary code and the binary output back to text

#dictionaries

#letter dictionary
letter_dict = {
        'a':'0100001',
        'b':'0100010',
        'c':'0100011',
        'd':'0100100',
        'e':'0100101',
        'f':'0100110',
        'g':'0100111',
        'h':'0101000',
        'i':'0101001',
        'j':'0101010',
        'k':'0101011',
        'l':'0101100',
        'm':'0101101',
        'n':'0101110',
        'o':'0101111',
        'p':'0110000',
        'q':'0110001',
        'r':'0110010',
        's':'0110011',
        't':'0110100',
        'u':'0110101',
        'v':'0110110',
        'w':'0110111',
        'x':'0111000',
        'y':'0111001',
        'z':'0111010',
        ' ':'0100000',
        '0':'1000000',
        '1':'1000001',
        '2':'1000010',
        '3':'1000011',
        '4':'1000100',
        '5':'1000101',
        '6':'1000110',
        '7':'1000111',
        '8':'1001000',
        '9':'1001001',
        '.':'1001010',
        ',':'1001011',
}
#binary dictionary
binary_dict = {
        '0100001':'a',
        '0100010':'b',
        '0100011':'c',
        '0100100':'d',
        '0100101':'e',
        '0100110':'f',
        '0100111':'g',
        '0101000':'h',
        '0101001':'i',
        '0101010':'j',
        '0101011':'k',
        '0101100':'l',
        '0101101':'m',
        '0101110':'n',
        '0101111':'o',
        '0110000':'p',
        '0110001':'q',
        '0110010':'r',
        '0110011':'s',
        '0110100':'t',
        '0110101':'u',
        '0110110':'v',
        '0110111':'w',
        '0111000':'x',
        '0111001':'y',
        '0111010':'z',
        '0100000':' ',
        '1000000':'0',
        '1000001':'1',
        '1000010':'2',
        '1000011':'3',
        '1000100':'4',
        '1000101':'5',
        '1000110':'6',
        '1000111':'7',
        '1001000':'8',
        '1001001':'9',
        '1001010':'.',
        '1001011':',',
}


#functions

def text_to_binary(message):

	'''This converts an alpha-numeric string into a binary output equivalent based on the letter dictionary within the dictionaries.py document'''
	bin_sentence = list(message)
	bin_temp = []
	
	for each_letter in bin_sentence:
		each_letter = each_letter.lower()
		bin_temp.append(letter_dict[each_letter])
		
	converted_bin = ''.join(bin_temp)
	
	return converted_bin
	
def binary_to_text(message):

	'''This converts a binary output into the alpha-numeric string equivalent based on the binary dictionary within the dictionaries.py document'''
	temp_build = []
	message_list = list(message)
	temp = []
	temp_converted = []
	
	while len(message_list) > 0:
		while len(temp) < 7:
			temp.append(message_list.pop(0))
		temp_build.append(''.join(temp))
		temp.clear()
		
	for each_binary in temp_build:
		temp_converted.append(binary_dict[each_binary])
		
	converted_text = ''.join(temp_converted)
	
	return converted_text
	
def converter():
	'''This is the main converter where you can either convert from text to binary (by entering '1') or from binary to text (by entering '2').'''
	
	print('\nWelcome to the binary converter. This converts your text(without punctuation) into binary code and the binary output back to text.\n')
	
	confirm = input('Would you like to:\n1.Convert text to binary (Enter -> 1 or \'text\')\tor\n2.Convert binary to text (Enter -> 2 or \'binary\')\n> ')
	
	if confirm == '1' or confirm == 'text':
		message = input('Enter the text message you would like to convert to binary?\n>')
		converted_text = text_to_binary(message)
		print(converted_text)
		
	elif confirm == '2' or confirm == 'binary':
		message = input('enter the binary message you would like to convert to text\n>')
		converted_bin = binary_to_text(message)
		print(converted_bin)
		
	else:
		print('Please enter 1 to convert to binary\tor\n2')
		converter()
		
		
#converter run
converter()

