# https://forum.omz-software.com/topic/3834/is-there-a-command-for-matching-letters-in-a-word/6

word = 'catatonic'
guess = 'cat'

def matching_letters(word, guess):
	return ''.join(c if i < len(guess) and c == guess[i] else '*'
	for i, c in enumerate(word))
	
print(matching_letters(word, guess))
print(matching_letters(guess, word))

