## README:
"""
Please read the file "Readme.txt"
"""

## Import sage_interface for SageMathCell server:
from sage_interface import *

## Import numpy and matplotlib.pyplot: (here I suppose the local python environment has only numpy and matplotlib as basic math libraries)
import numpy as np
#np.set_printoptions(threshold=np.inf)

import matplotlib.pyplot as plt

## Import python built-in useful libraries, if required:
import time   ## for example time to test the time execution of a calculation






filename1 = 'input_sage_01.py'

start_time = time.time()
sage_output_01 = execute_sage_script(filename1)
stop_time = time.time()

for j in range(len(sage_output_01)):
	print(sage_output_01[j])
	print('++++++++++++++++++++++')
print("Size of output list by SageMathCell after execution of script '" + filename1 + "':")
print(len(sage_output_01))




print('++++++++++++++++++++++')
print('++++++++++++++++++++++')
print('++++++++++++++++++++++')


  
  
  
filename2 = 'input_sage_02.py'
sage_inputs_01 = namestr( a=sage_output_01[10] , b=sage_output_01[11] , c=sage_output_01[12] )

start_time = time.time()
sage_output_02 = execute_sage_script_w_inputs(sage_inputs_01, filename2)
stop_time = time.time()

for j in range(len(sage_output_02)):
	print(sage_output_02[j])
	print('++++++++++++++++++++++')
print("Size of output list by SageMathCell after execution of script '" + filename2 + "':")
print(len(sage_output_02))

  
  

  
