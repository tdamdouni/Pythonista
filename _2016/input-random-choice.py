#!/usr/bin/env python3

# https://forum.omz-software.com/topic/3793/ned-solution-for-specific-button-press/3

import console
import random
messages = ("Du kommer bli rik inom närmaste framtiden",
            "Du kommer få tur i kärleken",
            "Du kommer att göra en resa",
            "Du kommer att få framgång i ditt yrke",
            "Den närmaste framtiden ser otydlig ut",
            "Olycka väntar dig",
            "Framtiden är mörk...",
            "Hmmm ser inte bra")
val = "j"
while val == "j":
	console.clear()
	print(random.choice(messages))
	print("Vill du testa igen (j/n)")
	val = input().strip().lower()  # <space>J<space> == j
print("hejdå")
console.hide_output()

