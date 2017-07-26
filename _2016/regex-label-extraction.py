# https://gist.github.com/paultopia/c6b3d2c440d6f17f56c314130e58b5fb

# Common data cleaning pattern: you need to find regex matches in some block of text, stored w/ labels in a
# dictionary (i.e., from json), extract those matches, and store them as an additional labels.
# here's a quick and dirty utility function to do so.  can then be used in loop or listcomp over entire dataset
import re
from collections import Counter
def pattern_extractor(instance, pattern, textlabel, newlabel):
	found = re.findall(pattern, instance[textlabel])
	if found:
		if isinstance(found[0], (list, tuple)):
			matches = [filter(None, x)[0] for x in found]
		else:
			matches = filter(None, found)
		instance[newlabel] = sorted(Counter(matches).most_common())
	return instance

