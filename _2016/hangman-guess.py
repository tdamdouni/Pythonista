# https://forum.omz-software.com/topic/3834/is-there-a-command-for-matching-letters-in-a-word

word = 'cat'
guess = 'car'

match = ''

for index in range(len(word)):
  match += word[index] if word[index] == guess[index] else '*'

print(match)
