# https://forum.omz-software.com/topic/3793/ned-solution-for-specific-button-press/2

import random
import console

def getAn(ansnu):
	if ansnu == 1:
		return "Du kommer bli rik inom närmaste framtiden"
	elif ansnu == 2:
		return "Du kommer få tur i kärleken"
	elif ansnu == 3:
		return "Du kommer att göra en resa"
	elif ansnu == 4:
		return "Du kommer att få framgång i ditt yrke"
	elif ansnu == 5:
		return "Den närmaste framtiden ser otydlig ut"
	elif ansnu == 6:
		return "Olycka väntar dig"
	elif ansnu == 7:
		return "Framtiden är mörk..."
	elif ansnu == 8:
		return "Hmmm ser inte bra"
		
val = "j"
while val == "j":
	console.clear()
		# resten måste vara inanför while oxå
	r = random.randint(1,8)
	fort = getAn(r)
	print(fort)
	print("Vill du testa igen (j/n)")
	val = input()
	if val == "n":
		print("hejdå")
console.hide_output()

