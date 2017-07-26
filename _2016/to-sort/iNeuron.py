# iNeuron
#
#
# Michele Giugliano, 18-19/10/2014, Antwerpen
# http://www.uantwerpen.be/michele-giugliano
#
# pythonista://MG/iNeuron?action=run 
#

import string
import sound
from scene import *
from random import *
from time import localtime
from itertools import chain
from math import sin, exp, fmod

ipad = False #will be set in the setup method

# Our class inherits from Scene, so that its draw method
# is automatically called 60 times per second when we run it.
# This implies approximately once every 16.6666... ms

class iNeuron (Scene):
	def setup(self):
		global ipad, yy, tt
		ipad = self.size.w > 700
		#Render all the digits as individual images:
		self.numbers = {}
		self.numbers_small = {}
		font_size = 150 if self.size.w > 700 else 60
		for s in chain(string.digits, [':', '.']):
			#render_text returns a tuple of
			#an image name and its size.
			self.numbers[s] = render_text(s, 'Helvetica-Light', font_size)
			self.numbers_small[s] = render_text(s, 'Courier', 20)
			
		#--------------------------------------------------------------------------
		# Simulation definition and control, general parameters
		self.umin = -100.;			# Minimal voltage to be displayed
		self.umax = 100.;				# Maximal voltage to be displayed
		self.t       = 0;       # Current sim. time [ms]
		self.mdt     = .1;      # Integration time step [ms]
		self.u 			 = -70.6;		# Membrane potential state variable
		self.w 			 = 0.;			# Adaptation state variable
		self.t0			 =-9999.;		# Last firing time [ms], for refractoryness
		self.In      = 0.;			# Synaptic fluctuating background current
		self.Iext    = 0.;			# External current, when the touch screen is touched
		#--------------------------------------------------------------------------
		# (1) Model neuron parameters (i.e. exponential I&F)
		self.th      = 20;       #[mV] - peak value for a spike
		self.C       = 281;      #[pF] - membrane capacitance
		self.g_L     = 30;       #[nS] - leak conductance
		self.E_L     = -70.6;    #[mV] - leak reversal potential (or resting potential)
		self.V_T     = -50.4;    #[mV] - excitability threshold
		self.Delta_T = 2;        #[mV] - excitability slope
		self.Tarp    = 2.;       #[ms] - absolute refractory period
		#--------------------------------------------------------------------------
		self.tau_w   = 144;      #[ms] - decay time constant for adaptation variable
		self.a       = 4;        #[nS] - voltage-dependence of adaptation variable
		self.b       = 0.0805;   #[nA] - spike-dependence of adaptation variable
		#--------------------------------------------------------------------------
		self.mu      = 200.;		 # Mean of the synaptic background current
		self.sigma   = 400.;		 # Stddev of the syn. backgr. current (e.g., 2 * mu)
		self.taux 	 = 5.;			 # Autocorrelation time length [ms]
		self.t1      = self.mdt / self.taux;  # Temp. var.for convenience - refer to eqs.
		self.t2      = sqrt(2.*self.t1); 	 	  # Temp. var.for convenience - refer to eqs.
		#--------------------------------------------------------------------------

		
	def should_rotate(self, orientation):
		return True
	
	def draw(self):
		global yy, tt
		background(0., 0., 0.)
		fill(0.6,0,0) 
		stroke(0.6,0,0)
		stroke_weight(3)
		#---------------------------------------------------------------------------------------
					
		# Main simulation cycle, repeated as many are the horizontal points on scren			
		for kk in range(int(self.size.w)):
			# Iteratively update the equation for the noisy external cu
			self.In += (self.mu - self.In) * self.t1 + self.sigma * self.t2 * gauss(0,1);  

			if self.u==self.th: # threshold
				self.u = self.E_L;
				self.w += self.b;
				self.t0 = self.t;
				line(kk,0.1 * self.size.h,kk,self.size.h)
				tmp = sound.play_effect('Drums_02', 100, 20)
				#sound.stop_effect(tmp)
			else:
				if (abs(self.t-self.t0) >= self.Tarp):
					udot = self.mdt/self.C*(-self.g_L*(self.u-self.E_L) + self.g_L*self.Delta_T*exp((self.u-self.V_T)/self.Delta_T) - self.w + self.In + self.Iext);
					if ((self.u + udot) > self.th):	
						self.u = self.th	
					else: 
						self.u  += udot
				else:
					self.u    = self.E_L;
			wdot = self.mdt/self.tau_w*(self.a*(self.u-self.E_L) - self.w);
			self.w += wdot;
			self.t += self.mdt;
			ud = (self.u - self.umin)/(self.umax - self.umin) * self.size.h * 0.9 + 0.1 * self.size.h
					
			if (fmod(kk,2)==0):
				ellipse(kk, ud, 2, 2)
		#------------------------------------------------------------------------------------------
		t = localtime()										# current time probed, in the structure "t"
		minute = t.tm_min									# minutes
		second = t.tm_sec									# seconds
		hour   = t.tm_hour 	 							# hours
			
		#Format the elapsed time (dt):
		s = '%02d:%02d.%02d' % (hour, minute, second)
		#Determine overall size for centering:
		w, h = 0.0, self.numbers['0'][1].h
		for c in s:
			size = self.numbers[c][1]
			w += size.w
		#Draw the digits:
		x = int(self.size.w * 0.5 - w * 0.5)
		y = int(self.size.h * 0.5 - h * 0.5)
		for c in s:
			img, size = self.numbers[c]
			image(img, x, y, size.w, size.h)
			x += size.w

		#Format the real-time index:
	  # self.dt : time in seconds elapsed since the last "draw" operation
		tmp1 = (0.001 * self.mdt * self.size.w) 	# simulated seconds per frame
		tmp2 = tmp1 / self.dt
		s = '%02f' % tmp2
		#Determine overall size for centering:
		w, h = 0.0, self.numbers_small['0'][1].h
		for c in s:
			size = self.numbers_small[c][1]
			w += size.w
		#Draw the digits:
		x = int(self.size.w * 0.5 - w * 0.5)
		y = int(self.size.h * 0.75 - h * 0.5)
		for c in s:
			img, size = self.numbers_small[c]
			image(img, x, y, size.w, size.h)
			x += size.w

	def touch_began(self, touch):
		self.Iext    = 200.;

	def touch_ended(self, touch):
		self.Iext    = 0.;
	
#Run the scene that we just defined (10 frames/sec --> "6")
run(iNeuron(),orientation=DEFAULT_ORIENTATION, frame_interval=6, anti_alias=False)

# 1: 60
# 2: 30
# 3: 20
# 4: 15
# 5: 12
# 6: 10
# 7: 60/7
# 8: 60/8

