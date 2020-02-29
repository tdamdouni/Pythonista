#!/usr/bin/env python2

# coding: utf-8

# https://forum.omz-software.com/topic/3698/how-to-save-user-input-from-text-field-and-use-throughout-script-with-ui/3

""" Math """
from __future__ import print_function

import random
import speech


def gen_add_equ():

	""" Generate Equations """
	
	try:
	
		count = 0
		
		count_wrong = 0
		
		start_over = 0
		
		wrong = 5
		
		all_wrong = 0
		
		all_right = 0
		
		#speak_how = speech.say("how many would you like to do", "en-US", 0.5)
		
		finish = (int(input("How many would you like to do: ")))
		
		str_fin = str(finish)
		
		#speak_ok = speech.say("ok"+ str_fin + "it is", "en-US", 0.5)
		
		if finish < 5:
		
			#speak_must = speech.say("oops...sorry...you must do at least 5","en-US", 0.5)
			
			print("\nYou must do at least 5")
			
			finish = 5
			
		while count < finish:
		
			count = count + 1
			
			a1 = random.randint(10, 999)
			
			b1 = random.randint(10, 999)
			
			while a1 < b1:
			
				a1 = b1 + a1
				
			#speak_sol = speech.say("solve the equation", "en-US", 0.5)
			
			sol_pro = "Solve the equation:"
			
			str_num_a1 = str(a1)
			
			str_num_b1 = str(b1)
			
			#speak_nums = speech.say("what is"+ str_num_a1 + "+"+ str_num_b1, "en-US", 0.5)
			
			print("\n#."+str(count),sol_pro, "{:,}".format(a1), "+", "{:,}".format(b1))
			
			ans = a1 + b1
			
			yours = ""
			
			str_ans = str(ans)
			
			while yours != ans:
			
				yours = int(input("\nYour Answer: "))
				
				str_your = str(yours)
				
				if yours != ans:
				
					count_wrong = count_wrong + 1
					
					if count_wrong > wrong:
					
						count_wrong = start_over + 1
						
					#speak_yours = speech.say(str_your + "is incorrect....try again....")
					
					print("\n",count_wrong,"wrong","{:,}".format(yours),"Is Incorrect Try Again.")
					
					if count_wrong == wrong:
					
						#speech.say("maybe you should try" + str_ans + "and lets see what happens")
						
						print("\n",ans,"might do it!")
						
				else:
				
					#speak_yours = speech.say(str_ans + "is correct....good job....")
					
					print("\n","{:,}".format(ans),"Is Correct Good Job!\n")
					
		if count == finish:
		
			#speak_done = speech.say("youre done for now....Bye.bye", "en-US", 0.5)
			
			print("Done For Now Bye Bye")
			
			print("\n",count_wrong,"were wrong out of",finish)
			
	except:
	
		print()
		
		return
		
		
def main():

	""" Run Script """
	
	gen_add_equ()
	
if __name__ == "__main__":
	main()

