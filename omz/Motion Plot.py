'''This script records your device's orientation (accelerometer data) for 5 seconds, and then renders a simple plot of the gravity vector, using matplotlib.'''

import motion
import matplotlib.pyplot as plt
from time import sleep
import console

def main():
	console.alert('Motion Plot', 'When you tap Continue, accelerometer (motion) data will be recorded for 5 seconds.', 'Continue')
	motion.start_updates()
	sleep(0.2)
	print 'Capturing motion data...'
	num_samples = 100
	data = []
	for i in xrange(num_samples):
		sleep(0.05)
		g = motion.get_gravity()
		data.append(g)
	motion.stop_updates()
	print 'Capture finished, plotting...'	
	
	x_values = [x*0.05 for x in xrange(num_samples)]
	for i, color, label in zip(range(3), 'rgb', 'XYZ'):
		plt.plot(x_values, [g[i] for g in data], color, label=label, lw=2)
	plt.grid(True)
	plt.xlabel('t')
	plt.ylabel('G')
	plt.gca().set_ylim([-1.0, 1.0])
	plt.legend()
	plt.show()

if __name__ == '__main__':
	main()