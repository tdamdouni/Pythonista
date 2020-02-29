from __future__ import print_function
import random
 
tipp = -1
anzahl = 0
zahl = random.randint(0,30)
 
while tipp != zahl:
    tipp = int(raw_input("Dein Tipp: "))
    anzahl =anzahl + 1
    if tipp < zahl:
        print("Deine Zahl ist zu klein!")
    else:
        if tipp > zahl:
            print("Deine Zahl ist zu gross!")
        else:
            print("Du hast die Zahl in",anzahl,"Versuchen erraten!")
