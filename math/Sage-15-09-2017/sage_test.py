## For now this script can execute only independent scripts, that is: the output of a script executed by SageMathCell through the function 'execute_sage(filename, timeout)' can't be passed to the input for the next script executed by SageMathCell.
## Working on it to pass, easly, input-output from/for Sage server and Pythonista.

from sage_interface import *

import time
import numpy as np
np.set_printoptions(threshold=np.inf)
import matplotlib.pyplot as plt


## third script = 'input_sage_03.py' : execute_sage(full-filename, timeout_in_seconds)
output_03 = execute_sage('input_sage_03.py', 1)   ## script executed by Sage remote server
print(output_03+100)   ## command executed by Pythonista (local Python core)
print(output_03+(120+180.j))   ## to check the compatibility with the built-in Pythonista numpy v1.8.0
print('-----------------------')

output_03_mod = output_03 * (1)   ## command executed by Pythonista (local Python core), like the following ones:
print(output_03_mod)
plt.suptitle("Solutions for h (green) and g (red) by processed script 'input_sage_03.py'", fontsize=14, fontweight='bold')
plt.plot(output_03_mod[:,0], output_03_mod[:,1], color='g')   ## plot h(t)
plt.plot(output_03_mod[:,0], output_03_mod[:,2], color='r')   ## plot g(t)
plt.xlabel('time (s)', fontsize=12, fontweight='bold')
plt.ylabel('h, g', fontsize=12, fontweight='bold')
plt.show()
print('-----------------------')