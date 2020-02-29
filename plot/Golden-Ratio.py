from __future__ import print_function
# https://github.com/ThomasBoynton/Fibonnaci-Fun/blob/master/Golden%20Ratio.py

import matplotlib.pyplot as plt

#Define Functions---------------------------------------------

def fib(n):
    """Generates Fibonacci Sequence"""
    fib_list = []
    i = 0
    num = 1.0
    while i <= n:
        if i <= 1:
            fib_list.insert(i,num)
            i += 1
        elif i >= 2:
            num += fib_list[i-2]
            fib_list.insert(i,num)
            i += 1
        else:
            print("Error")
    return fib_list

def Phi(fib):
    """Takes a list as an argument, if the fibonacci list is passed
        then a series of numbers converging on Phi, the golden ratio"""
    if len(fib) > 0:
        phi_approx = []
        i = 0
        phi = 0.0
        while i <=len(fib):
            phi = fib[i-1]/fib[i-2]
            phi_approx.insert(i, phi)
            i += 1
        return phi_approx
    else:
        return "Error: The Fibonnaci Sequence List is empty!"  
#-------------------------------------------------------------

Input = input("How many terms in the sequence do you want to generate?: ")

fib_sequence = fib(Input)
print(fib_sequence)

phi_sequence = Phi(fib_sequence)
print(phi_sequence)

#Plot Graphs
plt.figure(1)
plt.subplot(211)
plt.title("The Golden Ratio")
plt.plot(fib_sequence)
plt.ylabel("Fibonnaci Sequence")

plt.subplot(212)
plt.plot(phi_sequence)
plt.ylabel("Phi (approx)")
plt.show()
  
