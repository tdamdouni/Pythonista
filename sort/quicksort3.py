from __future__ import print_function

def quicksort(liste):
    print("Sortiere",liste)
    if len(liste) <= 1:
        print("nichts zu tun!")
        return liste
    pivotelement = liste[0]
    links  = [element for element in liste[1:] if element <  pivotelement]
    rechts = [element for element in liste[1:] if element >= pivotelement]
    print("Linker Teil:",links,"Pivotelement:",pivotelement,"Rechter Teil:",rechts)
    return quicksort(links) + [pivotelement] + quicksort(rechts)

