# https://forum.omz-software.com/topic/3595/connecting-two-files/4

# data1.txt
# ["aa", "bb", "cc", "dd"]
# --------------------

import ast
import json

with open('data1.txt') as fp:
	my_list = ast.literal_eval(fp.read())
	print(my_list)
	
with open('data1.txt') as fp:
	my_list1 = json.load(fp)
	print(my_list1)

