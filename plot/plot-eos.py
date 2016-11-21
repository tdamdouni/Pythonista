# coding: utf-8

# https://forum.omz-software.com/topic/2925/help-fsolve-numpy/5

import matplotlib.pyplot as plt
import numpy as np
x2=-1 #roots only exist if x2 is negative, and <-0.83

def EOS(x,y) :
   e11=1.00 ; e22=0.40 ; e12=0.60
   return np.log(1.-x)+x**2*(e22*y+ e11*(1-y) + 2*x2*(1-y)*e12)

for i in np.arange(1,99,1) :
   y=i*0.01
   #ans[i]=fsolve(lambda x: EOS(x,y),x0)
   x=np.linspace(-5,1,100)
   plt.plot(x,EOS(x,y))
plt.show()
