#coding: utf-8
from __future__ import print_function
def minsort(liste):
 
    # gehe die Liste von Anfang bis zur vorletzen Stelle durch (Zähler i)
    for i in range(len(liste)-1):
 
        # suche das Minimum von der i-ten Stelle bis zum Ende
        minimum = i
        for z in range(i, len(liste)):
            if liste[z] < liste[minimum]:
                minimum = z
 
        # Tausche i-te Stelle mit dem Minimum, falls sie sich unterscheiden
        if minimum != i:
            print("Tausche %d. Element (%d) mit %d. Element (%d)"%(i+1, liste[i], minimum+1, liste[minimum]))
            tausch = liste[minimum]
            liste[minimum] = liste[i]
            liste[i] = tausch
 
    return liste
