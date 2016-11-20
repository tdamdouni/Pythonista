# coding: utf-8

# https://gist.github.com/hiilppp/6aa5b7ca127823c8eea6

# Python script for capitalizing titles (according to The Chicago Manual of Style's rules) in Editorial (see http://www.editorial-workflows.com/workflow/5247248250175488/_f57rqO3mos).

import linguistictagger
import re
import workflow

def capitalize_(s):
	if re.search(r"[A-Z]", s):
		return s
	else:
		return s.capitalize()

articles = ["a", "an", "the"]
coordinating_conjunctions = ["and", "but", "for", "nor", "or"]
general_exceptions = articles + coordinating_conjunctions + ["to", "n’t", "n't"]

input = workflow.get_input()
input_prefix = re.sub(r"^([^A-z]*).*", "\\1", input)
title = re.sub(r"^[^A-z]*([A-z].*)", "\\1", input)
title_tagged = linguistictagger.tag_string(title, linguistictagger.SCHEME_LEXICAL_CLASS)
last_word = len(title_tagged) - 1
output = []

while True:
	if re.search(r"[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0-9]", title_tagged[last_word][1]): # `r"[A-z]"`/`r"\w"` matches `_`!?
		break
	last_word -= 1

for i, v in enumerate(title_tagged):
	w = re.sub(r"^[*_]*([^*_]*)", "\\1", v[1])
	w_prefix = re.sub(r"^([*_]*)[^*_]*", "\\1", v[1])
	if i == 0 or i == last_word:
		output.append(w_prefix + capitalize_(w))
	elif w.lower() in general_exceptions:
		# output.append(w_prefix + w.lower())
		output.append(v[1])
	elif v[0] == "Preposition":
		if len(w) > float("inf"):
			output.append(w_prefix + w.capitalize())
		else:
			# output.append(w_prefix + w.lower())
			output.append(v[1])
	else:
		output.append(w_prefix + capitalize_(w))

output = input_prefix + "".join(output)

workflow.set_output(output)