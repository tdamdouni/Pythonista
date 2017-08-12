# Hangman

_Captured: 2016-11-18 at 12:32 from [davidcorne.com](https://davidcorne.com/2012/06/17/hangman/#more-217)_

A short post this time. A few months ago I was looking for a little light distraction and I thought I'd learn Python. After doing all the usual stuff (Hello World, and a few problems from [Project Euler](http://projecteuler.net/problems)) I decided to make a short game. As I'm sure you can tell from the title of this post it was a game of hangman. I made this decision because I found out about the string [translate](http://docs.python.org/library/string.html#string-functions) feature in Python and thought that it would be perfect to gradually reveal the word.

This file (and a dictionary) is located [here](http://goo.gl/VLx1M) if you want the whole file.

So the script works as follows:

Start in either one or two player mode. In two player mode this is very simple as it asks for a word from the first player and then starts. In one player mode it randomly selects a word from a dictionary.txt file I provided (as long as it's in the same directory as the file being run). This is the code for reading in the file and selecting a random word from it.

192021222324252627282930
`word ``=` `""``if` `(players ``=``=` `1``):``dictionary ``=` `os.path.dirname(``str``(sys.argv[``0``])) ``+` `"/dictionary.txt"``if` `(``not` `os.path.exists(dictionary)):``print``(``"No dictionary found in %s\n"` `%``(dictionary))``quit()``dict_file ``=` `open``(dictionary)``lines ``=` `dict_file.readlines()``num ``=` `len``(lines)``line_no ``=` `random.randrange(num)``word ``=` `str``(lines[line_no])``word ``=` `word[:``-``2``]`

This opens the dictionary file (if found) then makes a list of the lines, chooses a line at random and stores it in the variable `word`.

If it is started in two player mode it will ask for a word to guess at and check there are no nasty symbols in it.

31323334353637383940
`else``:``# enter word``word ``=` `raw_input``(``"Enter word?\n"``)``word ``=` `str``(word)``if` `(``"_"` `in` `word):``print``(``"That's Cheating!!!!!!\n"``)``quit()``if` `(``not` `word):``print``(``"Don't enter a blank word\n"``)``quit()`

It is started in one player mode by default (for testing) and the command line argument "-2" is needed to start it two player. Here is the code that deals with this, just standard (not very robust e.g no -h for help) command line parsing.

10111213141516
`players ``=` `1``if` `(``len``(sys.argv) > ``2``):``print``(``"Too many arguments"``)``quit()``if` `(``len``(sys.argv) ``=``=` `2``):``if` `(sys.argv[``1``] ``=``=` `"-2"``):``players ``=` `2`

The game then loops through asking for guessed characters storing guesses and displaying beautiful ascii hangmen. There is error checking on the guess in that, it checks if you've guessed it before, it checks you've entered something and it checks that it's a normal ascii letter. After this it is a valid guess and thus it is checked against the word to be guessed. Then the following is run:

189190191192193194195196
`if` `(guess ``in` `word):``message ``=` `"Correct!"``point ``=` `ord``(guess) ``-` `65``underscores ``=` `underscores[``0``:point] ``+` `guess ``+` `underscores[point``+``1``:]``trans ``=` `string.maketrans(string.ascii_uppercase ``+` `string.ascii_lowercase, underscores)``show ``=` `word.translate(trans)``if` `(``not` `"_"` `in` `show):``guessed ``=` `True`

This means that the guess is removed from the translation map and so shows up in the terminal. It then checks if the whole word has been guessed as if there is no underscore in the word then there are no more letters to be guessed.

And that's that really just a nice simple program building off of the handy string [translate](http://docs.python.org/library/string.html#string-functions) feature .

[This](http://goo.gl/VLx1M) is a link to the hangman program file and the dictionary.
