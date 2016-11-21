# coding: utf-8

# https://forum.omz-software.com/topic/2528/character-count-without-spaces

def char_count(s):
	return len([x for x in s if not x.isspace()])
	

