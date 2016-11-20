from contextlib import contextmanager
from operator import itemgetter
from sys import argv, stdout
from time import time

@contextmanager
def duration(outfile=stdout):
	start = time()
	yield
	end = time()
	outfile.write(str(end - start) + '\n')
	
def groupby(seq, func):
	d = dict()
	for item in seq:
		d.setdefault(func(item), []).append(item)
	return d
	
with duration():
	with open(argv[1], 'r') as file:
		word_pairs = [line.strip().split(',') for line in file]
		result = groupby(word_pairs, itemgetter(0))

