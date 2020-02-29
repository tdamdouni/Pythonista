#!python2
# http://stackoverflow.com/questions/33287270/syntax-error-on-else-in-my-quiz

# [{"question":"what is 5*4 ?","options":[10,20,30],"answer_index":1},{"question":"what is 10*4 ?","options":[40,50,60,30],"answer_index":0}]

from __future__ import print_function
def quiz():
	score  = 0
	begin = raw_input("do you want to start ?")
	if begin == "yes":
		print("A : 56")
		print("B : 48")
		print("C : 45")
		q1 = raw_input("what is 12*4")
		if q1 in ["b","B"]:
			print("congrats !! well done!1")
			score += 1
		else:
			print("sorry!! you are wrong try next one !! good luck")
			
		print("A : Another ice age")
		print("B : A meteor will hit the earth")
		print("C : Aliens will invade earth")
		q2 = raw_input("what will happen in 50 years?")
		if q2 in ["a","A"]:
			print("nice !! keep going!1")
			score += 1
		else:
			print("sorry!! you are wrong try next one !! good luck")
			
		return score
	else:
		print("ok bye")
		return 0

