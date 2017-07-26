# https://www.python-forum.de/viewtopic.php?t=37699

import numpy as np
import matplotlib

phi = np.linspace(0,np.pi*2,Lp)
the = np.linspace(-np.pi/2,np.pi/2,Lq)

def nautilus(phi, the):
	PHI,THE = np.meshgrid(phi,the) # (P[i,j],Q[i,j]) = (p[i],q[j])
	
	
	x = (a*np.e**(PHI) + r * np.cos(PHI)) * np.cos(PHI)
	y = (a*np.e**(PHI) + r * np.cos(PHI)) * np.sin(PHI)
	z = r * np.sin(PHI)
	
	fig=figure()
	ax3d=fig.add_subplot(111,projection='3d',aspect=1)
	ax3d.plot_surface(x,y,z)
	
nautilus(phi,the)

