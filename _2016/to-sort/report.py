# coding: utf-8

#This is my Automatic Report Writer Script
#It uses lists, choices and If, Elif and Else statements and my own functions!

#-----Import libaries-----#

from __future__ import print_function
from random import choice

#-----Variables------#

pupil_details = [["Tom","b","good"],["Pierre","b","bad"],["Hilary","g","ok"],["Victoria","g","bad",],["Jimmy","b","good"],["James","b","ok"],["Alice","g","good"],["Lilly","g","bad"]]

pupil_gender = ["He","She"]

pupil_behaviour_good = [" should be rewarded."," adds a whole new dimension to lessons."," knows more than the teacher."," makes me want to cry."," needs to be admired."]

pupil_behaviour_ok = [" does a good job."," should be pleased."," has a good understanding of the topics."," shows the poor performers what they could become."," should be given a Freddo."]

pupil_behaviour_bad = [" should be disciplined."," needs to care about their future."," needs extra tutition."," should retake tests."," needs to aim for higher grades."]

i = ['','','']
#------Functions-----#

def make_report():                               #This function makes reports.
	for i in pupil_details:                        	#For each list in the pupil_details...
		print ("This is the report for " +i[0])      #Print the title and the pupil's name.
if i[2] == "good":                           #If the pupil was behaving good...
	print(i[0] + choice(pupil_behaviour_good)) #Print pupil's name and a random element from the 
	#pupil_behaviour_good list.
elif i[2] == "ok":                           #If the pupil was behaving ok...
		print(i[0] + choice(pupil_behaviour_ok))   #Print pupil's name and a random element from the
			#pupil_behaviour_good list
else:                                        #There is only one other option...
		print(i[0] + choice(pupil_behaviour_bad))  #print pupil's name and a random element from the
				#pupil_behaviour_bad list.
print("\n")                                  #Create a new line before the next report.

#------Initialisation------#

def main():
	print('i am in the main function')

	#look this up on the net to see why you do this way
	if __name__ == '__main__':
		main()

#------Main Program Code-----#
	make_report()