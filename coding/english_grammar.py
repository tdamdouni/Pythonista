from __future__ import print_function
# Computer programming isn't just used for math. You can teach a computer [english grammar](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/english_grammar.py)!

# The following program can extract nouns and verbs from a sentence.

# Add more verbs to the following array
verbs = ['run','walk','fall']

# Add more nouns to the following array
nouns = ['he','she','it']

# We will extract all verbs and nouns out of the following sentence:
sentence = "He walks, she runs, and it falls."

# We will get the verbs and nouns in the sentence as an array
words = sentence.split()

# This function gets the verbs of the sentence
def get_verbs(s):
    for verb in verbs:
        if verb in s:
            print(verb + ' is a verb!')

# This function gets the nouns of the sentence
def get_nouns(s):
    for noun in nouns:
        if noun in s:
            print(noun + ' is a noun!')


# Now to use the functions above:
get_verbs(sentence)

print() # just adding a tab to the output

get_nouns(sentence)

# Try making a function that get's other parts of speech like adjectives out of a sentence.
