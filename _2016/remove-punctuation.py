# https://pythonadventures.wordpress.com/2017/02/05/remove-punctuations-from-a-text/

import string
tr = str.maketrans("", "", string.punctuation)
s = "Hello! It is time to remove punctuations. It is easy, you will see."
print(s)
print(tr)
print(s.translate(tr))
#'Hello Its time to remove punctuations Its easy youll see'

