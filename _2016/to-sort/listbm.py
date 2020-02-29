#!/usr/bin/env python

# https://gist.github.com/gps/717650

"""
listbm.py

Created by Gopal Sharma on 2010-11-26.
Copyright (c) 2010 Gopal Sharma. All rights reserved.
"""
from __future__ import print_function

import random
import gc
from time import time

sizes = [10 ** i for i in range(1, 8)]
N = 50

def generate_list_of_size(size):
	return random.sample(xrange(10 ** 8), size)

def bm_index():
	print("Index:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(size)
		sample = []
		for i in xrange(1000):
			sample.append(l[random.randint(0, size-1)])
		gc.collect()
		start = time()
		for s in sample:
			tmp = l.index(s)
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_count():
	print("Count:")
	results = {}
	sample = generate_list_of_size(1000)
	for size in sizes:
		l = generate_list_of_size(size)
		gc.collect()
		start = time()
		for s in sample:
			tmp = l.count(s)
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_pop():
	print("Pop:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(size)
		gc.collect()
		start = time()
		for i in xrange(5):
			tmp = l.pop(random.randint(0, len(l) - 1))
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_remove():
	print("Remove:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(size)
		sample = random.sample(l, 5)
		gc.collect()
		start = time()
		for s in sample:
			l.remove(s)
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_insert():
	print("Insert:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(size)
		sample = random.sample(xrange(size), 5)
		gc.collect()
		start = time()
		for s in sample:
			l.insert(s, random.randint(-300, 300))
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_reverse():
	print("Reverse:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(size)
		gc.collect()
		start = time()
		l.reverse()
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_sort():
	print("Sort:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(size)
		gc.collect()
		start = time()
		l.sort()
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_extend():
	print("Extend:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(1000)
		sample = generate_list_of_size(size)
		gc.collect()
		start = time()
		l.extend(sample)
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results

def bm_append():
	print("Append:")
	results = {}
	for size in sizes:
		l = generate_list_of_size(size)
		sample = generate_list_of_size(1000)
		gc.collect()
		start = time()
		for s in sample:
			l.append(s)
		end = time()
		print(size, end-start)
		results[size] = end-start
	print()
	return results
	
def main():
	functions = {}
	functions['Sort'] = bm_sort
	functions['Reverse'] = bm_reverse
	functions['Count'] = bm_count
	functions['Index'] = bm_index
	functions['Pop'] = bm_pop
	functions['Remove'] = bm_remove
	functions['Insert'] = bm_insert
	functions['Extend'] = bm_extend
	functions['Append'] = bm_append
	results = {}
	for name, func in functions.items():
		results[name] = []
		for i in xrange(N):
			results[name].append(func())
	
	print()
	
	for name, numbers in results.items():
		runs = {}
		for sets in numbers:
			for s, t in sets.items():
				if s not in runs.keys():
					runs[s] = []
				runs[s].append(t)
		print(name)
		for s in sorted(runs.keys()):
			print(s, sum(runs[s]) / len(runs[s]))

if __name__ == '__main__':
	main()
