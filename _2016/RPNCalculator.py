#!python2
# https://gist.github.com/PKHG/4245408

# https://forum.omz-software.com/topic/3706/rpncalculator

# https://forum.omz-software.com/topic/57/scientific-calculator

#version 1.2 8 dec. 2012 PKHG
#---------
#inverse sin etc. deg <-> rad
#4 12 2012 prgramming preparations
#UNDO partly done
from __future__ import print_function
from scene import *
from random import random
from string import ascii_lowercase
from math import *
from random import random
########## some globals easier typing
memories = {}
l_n = {}
l_red_n ={}
mesg = None
info = None
rad_set = True 
#hyp_setting = ''
last_x = 'TODO'
hyp_set = False 
#???done_18_red = False 
pgrm_mode = 0
pgrm_data ={}
pdata_length = 0
copy_xyzw_data = []
copy_xyzw_pgrm = ['','','','']
infos = ['DEG', 'RAD', 'DEG HYP', 'RAD HYP', 'pgrm mode'] # others append!
infos.append('Clear tap: 0 >X, 1 ->MEMs 2 ->Pgrm, 3 ->sum, 4 ->cancel') #nr. 5
infos.append('MEMs set to 0')
info_mode = 1
input_action = False 
clear_info_shown = False 
confirmed = False 
ch_ob = {'data':['0','1','2','3','4','UNDO'],'active':False, 'but':{}}
save_state = {'memories':[ii for ii in range(41)],'pressed_but':-1,'info_mode':-1}


class MyButton (Scene):
	def __init__(self, x=10, y=10, w=1, h=1, txt='      '):
		self.x, self.y = x, y
		self.txt = txt
		self.w, self.h = w, h
		self.b_red = False
		self.red, self.green, self.blue = Color(1,0,0), Color(0,1,0), Color(0,0,1)
		self.l_buf_normal =[]
		self.alphabet = []
		self.a_places = [ el for el in range(31,37)]
		tmp = [el for el in range(25,31)]
		self.a_places.extend(tmp)
		tmp = [el for el in range(20,24)]
		self.a_places.extend(tmp)
		tmp = [el for el in range(16,19)]
		self.a_places.extend(tmp)
		tmp = [el for el in range(11,14)]
		self.a_places.extend(tmp)
		tmp = [el for el in range(6,9)]
		tmp.append(1)
		self.a_places.extend(tmp)
		#self.memories = {}
		for el in self.a_places:
			memories[el] = str(el)
		#print(self.a_places)
		#print memories
		memories[37]=' 0'
		for el in range(38,41):
			memories[el] = '  0  '
		self.action = -1
		self.digit_places = [1,6,7,8,11,12,13,16,17,18]
		self.digit_found = -1
		self.rad_deg, size = render_text('rad -> deg')
		self.deg_rad,size = render_text('deg -> rad')
		self.names = None	
		
	def add_pgrm_data(self,but):
		global pgrm_data,pdata_length, info_modey, pgrm_mode, copy_xyzw_data, copy_xyzw_pgrm
		if but == 5 and pdata_length == 0:
			pgrm_mode = 2
			return #back from Pgrm and Red 
			
		if self.b_red:
			#print 'add_prgm L 74',but
			if but == 3:  #Pgrm ends this Pgrm-mode RESTORE!
				self.b_red = False 
				pgrm_mode = 0
				#print 'DBG L81',copy_xyzw_data[:]
				for el in range(4):
					memories[37+el] = copy_xyzw_data[el]
					txt = self.adjust_txt(copy_xyzw_data[el])
					img , size = render_text(txt)
					self.root_layer.sublayers[37+el].image = img
				copy_xyzw_data =[]
				self.root_layer.sublayers[3].background = self.blue
				self.root_layer.sublayers[5].background = self.blue
				self.change_info(1,col=Color(0,1,0))
				self.set_normal()
				return #FINISHED
#PKHG.TODO ?? next line ??!!
			but = 38 + but
			#print 'dbg L92',but
		s = 0 #to simplify adding an integer
		if but in self.digit_places:
			tmp = self.digit_places.index(but)
			if self.digit_found == -1:
				self.digit_found = 1
				pgrm_data[pdata_length] = tmp
				s = tmp
			else:
				try:
					pdata_length -= 1
					s = tmp + 10 * pgrm_data[pdata_length]
					pgrm_data[pdata_length] = s
					self.digit_found += 1	
				except:
					print('***ERROR INPUT OF INT TOO LONG')
					pdata_length += 1
					self.digit_found = -1
			#print '		digit found ',tmp
		else:
			pgrm_data[pdata_length] = [but, info_mode]
			self.digit_found = -1
			######## hier 
		for el in range(3,0,-1):
			copy_xyzw_pgrm[el] = copy_xyzw_pgrm[el-1]
		if self.digit_found > 0:
			#print s
			copy_xyzw_pgrm[0] = 'adr ' + str(pdata_length) + ' ' + str(s)
		else:		
			copy_xyzw_pgrm[0] = 'adr ' + str(pdata_length) + ' ' + self.names[but]		
		pdata_length += 1
		for el in range(4):
			txt = self.adjust_txt(copy_xyzw_pgrm[el])
			img , size = render_text(txt)
			self.root_layer.sublayers[37+el].image = img
		
	def m_one_txt_layer(self, txt, x, y, col=Color(0,0,0), extra = 0):
		#img, size = render_text(txt, font_size=30)
		img, size = render_text('Peter')
		#print(img,size)
		lay = Layer(Rect(x, y, size.w, size.h + 10 + extra))
		#lay.image ='Baby_Chick_1'
		lay.image = img 
		lay.background = col
		return lay
	
	def adjust_txt(self,txt,width=30):
		lt = len(txt)
		vo = int((width-lt)/2)
		na = width - vo - lt
		txt = ' '*vo + txt + ' '*na
		return txt
	
	def adjust_display(self, txt, col=Color(0,0,1)):
		txt = self.adjust_txt(txt)
		img , size = render_text(txt)
		self.root_layer.sublayers[37].image = img
		self.root_layer.sublayers[37].background = col
	
	def change_mesg(self, message, col=Color(1,0,0)):
		global mesg
		img,size = render_text(str(message))
		mesg.background = col
		mesg.image = img
	
	def change_info(self,infos_index,col=Color(0,0,0)):
		global infos, info
		tmp = self.adjust_txt(infos[infos_index],width=50)
		img,size = render_text(tmp)
		info.background = col
		info.image = img
		
	def m_layer(self,txt,col,row,width_1,width_2,extra=0,backgr = Color(0,0,1),w_stroke=True):
		img, size = render_text(txt, font_size = 30)
		layer = Layer(Rect(self.x + col * (width_1+extra), self.y + 45 * row, width_2, self.h + size.h))
		layer.stroke_weight = 1
		if w_stroke:
			layer.stroke = Color(0,1,0)
		layer.background = backgr
		layer.image = img
		self.root_layer.add_layer(layer)
		self.all_layers.append(layer)
		return layer
			
	def setup(self):	
		global mesg, info, ch_ob
		# This will be called before the first frame is drawn.
		# Set up the root layer and one other layer:
		self.root_layer = Layer(self.bounds)
		#center = self.bounds.center()
	
		self.l_n, l_but_info, maks = self.make_l_n()
		self.l_buf_normal = l_but_info
		self.all_layers =[]
		for row in range(4):
			for col in range(5):
				wi = col + 5 * row + self.b_red * 38
				self.m_layer(l_n[wi],col,row,maks,maks,50)
		self.m_layer(l_n[20+self.b_red*38],0,4,maks,maks)
		for ii in range(21,25):
			self.m_layer(l_n[(ii+self.b_red*38)], ii % 20, 4, maks,maks,50)
		for ii in range(25,31):
			self.m_layer(l_n[(ii+self.b_red*38)], ii % 25, 5, maks,maks,25)
		for ii in range(31,37):
			self.m_layer(l_n[(ii+self.b_red*38)], ii % 31, 6, maks,maks,25)
		#l_n[37] = memories[37]
		memories[37] = l_n[37+self.b_red*38]
		for ii in range(4):
			memories[37+ii] = self.adjust_txt(memories[37+ii])
			self.m_layer(memories[37+ii],0, 7.5 + ii, 200, 300)
		n_xyzw = ['x','y','z','w']
		for ii in range(4):
			#print self.root_layer.sublayers[37].frame #==> Rect(x=10, y=347.5, w=300, h=36.0)
			self.m_layer(n_xyzw[ii],10.2, 7.5 +ii,30,36,backgr=Color(0,0,0),w_stroke=False )
			#print self.root_layer.sublayers[-1].frame
		self.m_layer('messages:',1, 7.5 + 5,0,100,backgr=Color(0,0,0),w_stroke=False )
		#print self.root_layer.sublayers[-1].frame #Rect(x=10, y=572.5, w=100, h=36.0)
		self.m_layer(self.adjust_txt('OK',width=50),10, 7.5 + 5,12,500,backgr=Color(0,1,0))
		mesg = self.root_layer.sublayers[-1] #mesg is global	
		self.m_layer('info:',1, 7.5 + 6,0,100,backgr=Color(0,0,0),w_stroke=False )
		#print self.root_layer.sublayers[-1].frame #Rect(x=10, y=572.5, w=100, h=36.0)
		self.m_layer(self.adjust_txt('Rad',width=50),10, 7.5 + 6,12,500,backgr=Color(0,1,0))
		info = self.root_layer.sublayers[-1] #info is global
		#print 'info',type(info),info
		self.m_layer('choices:',1, 7.5 + 7,0,100,backgr=Color(0,0,0),w_stroke=False )
		self.m_layer('extra:',1, 7.5 + 8,0,100,backgr=Color(0,0,0),w_stroke=False )
		#ch_ob = {'data':['0','1','2','3','4','cancel'],'active':False, 'but':{}}	
		#def m_layer(self,txt,col,row,width_1,width_2,extra=0,backgr = Color(0,0,1),w_stroke=True):
		for ii in range(5):
			ch_ob['but'][ii] = self.m_layer(ch_ob['data'][ii],1.65+ii,14.5,maks*0.5,maks,50)
		ch_ob['but'][5] = self.m_layer(ch_ob['data'][5],1.65,15.5,maks*0.5,maks,50,backgr=Color(1,.3,1))
		
	def set_normal(self):
			#for ii, w in enumerate(self.a_places):
			for w in range(37):
				img,size = render_text( self.l_n[w +38 *self.b_red])
				self.root_layer.sublayers[w].image = img
			
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0, 0, 0)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
	
	def touch_began(self, touch):
		global input_action, save_state, info_mode, clear_info_shown, pgrm_data, confirmed
		def prepare_undo(but):
			print('***********   prepare_undo called')
		#save_state = {'memories':[],'pressed_but':-1,'info_mode':-1}
			save_state['info_mode'] = info_mode
			for el in memories:
				save_state['memories'][el] = memories[el]
			save_state['pressed_but'] = but
		#check, which button is touched			
		t_button = -1
		for i, el in enumerate(self.all_layers):
			if touch.location in el.frame:
				t_button = i
				break
		#for touched_button
		def do_UNDO():
			global clear_info_shown
			#print('DBG L 262 UNDO',clear_info_shown)
			if clear_info_shown:  # clear what?!
				clear_info_shown = False 
				self.change_info(1, col=Color(0,0,1))
			else:
				for ii, el in enumerate(save_state['memories']):
					memories[ii] = el
				info_mode = save_state['info_mode']
				self.change_info(info_mode, self.green)
				for el in range(37,41):
					img, size = render_text(self.adjust_txt(memories[el]))
					self.root_layer.sublayers[el].image = img
					
##### real begin of touch_begin **********************************			
		print('dbg touch black?',i,t_button)
		#print self.root_layer.sublayers[i].frame
		#t_button == -1 => no button touched!!
		if t_button == 56: #UNDO
			print('**********                               undo called')
			do_UNDO()
			return
		if clear_info_shown and t_button in [51, 52, 53, 54, 55]:
			clear_info_shown = False
			self.change_info(info_mode, col=Color(0,0,1))
			if confirmed and (t_button <> 53):
				confirmed = False 
				self.change_mesg('OK',Color(0,1,0))		
			if t_button == 55: #but 4 = cancel?!
				return
			if t_button == 51: #X reg
				memories[37] = ''
				self.adjust_display(' ')
				return			
			if t_button == 52:
				clear_memories()
				self.change_info(6)
				return
			if t_button == 53:		
				if confirmed:		
					pgrm_data ={}
					print('*** INFO PGRM CLEARED')
					confirmed = False
					self.change_mesg('Pgrm CLEARED',Color(0,1,1))
				else:
					self.change_mesg('REALLY? confirm: tap me again!',Color(1,0,0))				
					clear_info_shown = True 	
					confirmed =True 
				return
			if t_button == 54:
				print('*** INFO CLEAR SUM NOT YET IMPLEMENTED')
				return

			return # canceled nothing to do ;-)
		if t_button < 0 or t_button > 36: #not handled but? Yes, return!
			return 
####normal commands
		prepare_undo(t_button)
 		#print save_state
		self.exe_commands(t_button)
		
	def exe_commands(self,t_button):	
		global mesg, last_x, hyp_set, pgrm_mode, save_state
		error =''
		def set_alphabet():
			for ii, w in enumerate(self.a_places):
				img , size = render_text('  '+ascii_lowercase[ii] + '  ')
				self.root_layer.sublayers[w].image = img
				
		def mem_up():
			for el in range(39,36,-1):
				memories[el+1] = memories[el]
			for el in range(37,41):
				img, size = render_text(self.adjust_txt(memories[el]))
				self.root_layer.sublayers[el].image = img
				
		def mem_down():
			for el in [39,40]:
				memories[el-1] = memories[el]		
			#memories[40] = '0'
			for el in range(37,41):
				img, size = render_text(self.adjust_txt(memories[el]))
				self.root_layer.sublayers[el].image = img
		
		def rotate_down():
			tmp = memories[37]
			for el in [38,39,40]:
				memories[el-1] = memories[el]
			memories[40] = tmp
			for el in range(37,41):
				img, size = render_text(self.adjust_txt(memories[el]))
				self.root_layer.sublayers[el].image = img
		
		def red_actions(but):
			global hyp_set, rad_set, pgrm_mode, info_mode #???done_18_red
			global clear_info_shown, input_action
			error = 'not yet impemented '
			if but == 31: #X^2
				try:
					tmp = float(memories[37])**2
					memories[37]=str(tmp)
					error =''
				except:
					error = '***ERROR X^2 X=' #+ memories[37]
			elif but == 32: #10^X
				try:
					tmp = 10**float(memories[37])
					memories[37] = str(tmp)
					error = ''
				except :
					error = '***ERROR 10^X X='
			elif but == 33: #LOG(X)
				try:
					tmp = log10(float(memories[37]))
					memories[37] = str(tmp)
					error = ''
				except :
					'***ERROR LOG(X) X='
			elif but == 22:
			#	print '22 tapped',rad_set
				error = ''
				rad_set = not rad_set
				if rad_set:
					self.root_layer.sublayers[22].background = self.blue
					self.root_layer.sublayers[18].image = self.deg_rad		
				else: 
					self.root_layer.sublayers[22].background = self.red	
					self.root_layer.sublayers[18].image = self.rad_deg	
				info_mode = 1*rad_set+2*hyp_set
				self.change_info(info_mode,col=Color(random(),random(),1))			
			elif but == 25:
				error = 'COMPLX TAPPED, not yet implemented'
			elif but == 24: #CLEAR
				clear_info_shown = True 
				input_action = True 
				self.change_info(5)
				error = ''
				#CLEAR X VARS PROG SUM
			elif  but == 26: #pi
				error = ''
				memories[37] = str(pi)
			elif but == 27: #SET HYP
				hyp_set = not hyp_set
				if hyp_set:
					self.root_layer.sublayers[27].background = self.red
				else: 
					self.root_layer.sublayers[27].background = self.blue
				#TODO needs indicator
				info_mode = 1*rad_set+2*hyp_set
				self.change_info(info_mode,col=Color(random(),random(),1))			
				#self.adjust_display('HYP set')
				error = ''
			elif but == 20: #LAST_X
				error = ''
				memories[37] = last_x
				#print '*RED 20****DBG', type(last_x), last_x
			elif but == 18: #DEG <=> RAD
				try:
					arg = float(memories[37])
					if rad_set:
						memories[37] = str(radians(arg))
						#self.root_layer.sublayers[18].image = self.deg_rad		
					else:
						memories[37] = str(degrees(arg))
						#self.root_layer.sublayers[18].image = self.rad_deg
					error = ''
				except:
					error = '***ERROR DEG <=> RAD'
			elif but == 28: #ASIN
				try:
					arg =float(memories[37])
					memories[37] = str(asin(arg))
					error = ''
				except :
					error = '***ERROR asin'
			elif but == 29: #ACOS
				try:
					arg =float(memories[37])
					memories[37] = str(acos(arg))
					error = ''
				except :
					error = '***ERROR acos'
			elif but == 30: #ATAN
				try:
					arg =float(memories[37])
					memories[37] = str(atan(arg))
					error = ''
				except :
					error = '***ERROR atan'
			elif but == 3: #PGRM
				col = self.red
				error = ''
				#print('Pgrm tap ', pgrm_mode,' data =',pgrm_data.values())
				if pgrm_mode == 0:
					for el in range(37,41):
						copy_xyzw_data.append(memories[el])
					#print 'xyzw saved in copy_xyzw_data'
					pgrm_mode = 1 # first time not in Pgrm!
					self.change_info(4, col=Color(0,0,1))
				elif pgrm_mode == 2:
					pgrm_mode = 0
					col = self.blue
				else:
					prgm_mode = 0 # disable Pgrm mode
					self.change_info(info_mode, col=Color(0,0,1))
					col = self.blue
				self.root_layer.sublayers[3].background = col
				
			elif but == 0: #OFF
				#from sys import exit
				#exit(0)
				print('saved commands')
				for el in pgrm_data.values():
					print(el)
				error = 'tap x to real exit'
				#self.change_mesg(self.adjust_txt('tap x to real exit', width=50),col=Color(1,1,0))
			if not error and pgrm_mode == 0:
				self.adjust_display(memories[37])
			return error

		if  t_button == 5:     #RED is a toggle
			if self.b_red:
				self.b_red = False
				self.root_layer.sublayers[t_button].background = self.blue
				self.change_mesg(self.adjust_txt('OK', width=50),col=Color(0,1,0))
				self.root_layer.sublayers[27].background = self.blue			
				self.root_layer.sublayers[22].background = self.blue
				col = self.blue
				if hyp_set:	
					col = self.red
				for bu in range(28,31):
					self.root_layer.sublayers[bu].background = col
				#if prgm_mode == 'active': #PKHG if really needed?
					#self.root_layer.sublayers[3].background = self.blue
			else:
				self.b_red = True		
				self.root_layer.sublayers[t_button].background = self.red
				for bu in range(28,31):
					self.root_layer.sublayers[bu].background = self.blue
				if hyp_set:
					self.root_layer.sublayers[27].background = self.red
				else: 
					self.root_layer.sublayers[27].background = self.blue
				#TODO needs indicator
			self.set_normal()
#### already a return for new touch, RED changes layout with corresponing actions
			if pgrm_mode > 0:
				if pgrm_mode > 1:
					self.add_pgrm_data(5)
				else:
					pgrm_mode = 2
			return
		
		if pgrm_mode:
			self.add_pgrm_data(t_button)	
		elif self.b_red:
			error = red_actions(t_button)
		elif self.action == 25: #STO
			#print 'nu sto checken'
			if t_button in self.a_places:
				tmp = memories[37]
				#print 'wat=',tmp, 'where',t_button
				if tmp.find('***') <  0:
					memories[37] = '0'
				memories[t_button] = tmp #WHY NOT MEMORIES[37] POSSIBLE.
				#print 'stored',memories[t_button]
				self.action = -1
				memories[37] = tmp
				#self.setup()
				self.set_normal()
				self.adjust_display(memories[37])
		elif self.action == 26: # RCL
			#print 'nu rcl check'
			#print memories
			#print 'de t_button', t_button
			if t_button in self.a_places:
				#print 'value to set',memories[t_button]
				self.action = -1
				memories[37]= memories[t_button]
				self.set_normal()
				self.adjust_display(memories[37])		
		elif t_button in self.digit_places:
			#print 'digit place',t_button
			print('>',memories[37],'<')
			if memories[37].strip() == '0':
				memories[37] = ''
			if self.action == -1:
				self.action = -2
				#mem_up()+
				w = self.digit_places.index(t_button)
				memories[37] = str(w)
				self.adjust_display(memories[37])
			elif self.action == -2:
				#max check!! digit . check
				w = self.digit_places.index(t_button)
				memories[37] += str(w)
				self.adjust_display(memories[37])
				
		elif t_button in [4,9,14,19]: # + - * /
			self.action = -1
			try:
				arg1 = float(memories[38])
			except:
				error = "***ERROR arg1, zero used"
				arg1 = 0
			try:
				arg2 = float(memories[37])
			except:
				error += " ***ERROR arg2, zero used"
				arg2 = 0
			if t_button == 4: #add
				memories[37] = str(arg1 + arg2)
			elif t_button == 9:
				memories[37] = str(arg1 - arg2)
			elif t_button == 14:
				memories[37] = str(arg1 * arg2)
			elif t_button == 19:
				try:
					memories[37] = str(arg1 / arg2)  #no division by zero!
				except:
					memories[37] = str(arg1) +'x / 0 ***Clear me!'
					
			mem_down()		
		elif t_button == 25:    #STO prepare
			self.action = 25
			set_alphabet()
		elif t_button == 26:    #RCL prepare
			self.action = 26 
			set_alphabet()	
		elif t_button == 27: #ROTATE DOWN
			rotate_down()
		elif t_button == 0: #CLEAR
			memories[37] = ''
			self.adjust_display('')
		elif t_button == 2:
			#print '. touched'
			#print('www',memories[37].find('.'))
			if memories[37].find('.') < 0:
				memories[37] = memories[37].strip() + '.'
				self.adjust_display(memories[37])
		
		elif (self.action == -1 or self.action ==-2) and t_button ==  20: # ENTER CASE
			last_x = memories[37]
			#print 'but' + str(t_button) + ' pressed', type(last_x), last_x
			mem_up()
			self.action =-1		
			self.adjust_display(memories[37])	
		elif t_button == 24:
			tmp = memories[37].strip()
			if len(tmp) > 0:
				memories[37] = tmp[:-1]
				self.adjust_display(memories[37])			
		elif t_button == 21: # x<>y
			tmp = memories[38]
			memories[38] = memories[37]
			img, size = render_text(self.adjust_txt(memories[38]))
			#img, size = render_text(memories[38])
			self.root_layer.sublayers[38].image = img
			memories[37] = tmp
			self.adjust_display(memories[37])
			
		elif t_button == 22:   # +- button
			if self.action == -2:
				tmp = memories[37]
				tep = tmp.find('e')
				if tep > -1:
					mant = tmp[:tep+1]
					expd = tmp[(tep+2):]
					#print 'expd',len(expd),expd
					len_expd = len(expd)				
					try:
						expd = str(-int(float(expd)))
					except:
						expd = '-'			
					#print 'expd',len(expd),expd	
					memories[37] = mant + expd
				else:
					try:
						tmp = -float(memories[37]) 
						memories[37] = str(tmp)
					except:
						memories[37] = '-'
				self.adjust_display(memories[37])
			
		elif t_button == 23: #E case
			tmp = memories[37].find('e')
			if tmp < 0:
				self.action = -2 
				memories[37] += 'e'
				self.adjust_display(memories[37])
			else:
				self.action = -2
		
		elif t_button == 35:  # 1/x 
			try:
				tmp = 1.0 / float(memories[37])
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except:
				error = '1/x ***ERROR.?? with '
		
		elif t_button == 31: #SQRT
			try:
				tmp = sqrt(float(memories[37]))
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except :
				error = '*** SQRT ERROR WITH'
		
		elif t_button == 32: #EXP
			try:
				tmp = exp(float(memories[37]))
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except :
				error = '*** EXP ERROR WITH '
		
		elif t_button == 33: #LOG
			try:
				tmp = log(float(memories[37]))
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except :
				error = '*** LOG ERROR WITH '
		
		elif t_button == 34: #Y^X
			try:
				tmp = float(memories[38])**float(memories[37])
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except :
				error = '*** Y^X ERROR WITH '
				
		elif t_button ==  28: #SIN
			try:
				arg = float(memories[37])
				if hyp_set:
					tmp = sinh(arg)
				else:
					if not rad_set:
						arg = radians(arg)
					tmp = sin(arg)
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except :
				error = '*** SIN(H) ERROR WITH '

		elif t_button ==  29: #COS
			try:
				arg = float(memories[37])
				if hyp_set:
					tmp = cosh(arg)
				else: 
					if not rad_set:
						arg = radians(arg)
					tmp = cos(arg)
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except :
				error = '*** COS(H) ERROR WITH '
		elif t_button ==  30: #TAN TANH
			try:
				arg = float(memories[37])
				if hyp_set:
					tmp = tanh(arg)
				else:
					if not radians(arg):
						arg = radians(arg)	
					tmp = tan(arg)			
				memories[37] = str(tmp)
				self.adjust_display(memories[37])
			except :
				error = '*** TAN(H) ERROR WITH '

		elif t_button == 3: #R/S
			print(pgrm_data)
			ueerror = 'R/S not yet'
		if error:
			tmp = error + '"' + memories[37] + '"'
			self.change_mesg(tmp)
			#print tmp
		else:
			self.change_mesg(self.adjust_txt('OK', width=50),col=Color(0,1,0))
	
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

	def make_l_n(self):
		"""make names for lower part of calculator"""
#		l_n = {}
		l_n[0] = "  C  "
		l_n[1] = "  0  "
		l_n[2] = "  .  "
		l_n[3] = " R/S "
		l_n[4] = "  +  "
		l_n[5] = " RED "
		l_n[6] = "  1  "
		l_n[7] = "  2  "
		l_n[8] = "  3  "
		l_n[9] = "  -  "
		l_n[10] = "down"
		l_n[11] = "  4  "
		l_n[12] = "  5  "
		l_n[13] = "  6  "
		l_n[14] = "  *  "
		l_n[15] = " XEQ "
		l_n[16] = "  7  "
		l_n[17] = "  8  "
		l_n[18] = "  9  "
		l_n[19] = "  /  "
		l_n[20] = 'ENTER'
		l_n[21] = 'x<>y'
		l_n[22] = '+/-'
		l_n[23] = '  E  '
		l_n[24] = ' <== '
		l_n[25] = ' sto '
		l_n[26] = ' rcl '
		l_n[27] = 'rot dn'
		l_n[28] = ' SIN '
		l_n[29] = ' COS '
		l_n[30] = 'TAN'
		l_n[31] = 'SQRT'
		l_n[32] = 'EXP'
		l_n[33] = 'LN'
		l_n[34] = 'Y^X'
		l_n[35] = '1/X'
		l_n[36] = 'sum +'
		l_n[37] = self.adjust_txt('0')
		######red ones
		l_n[38+0] = "  OFF  "
		l_n[38+1] = "  input  "
		l_n[38+2] = "  show  "
		l_n[38+3] = " Pgrm "
		l_n[38+4] = " View  "
		l_n[38+5] = " RED "
		l_n[38+6] = " save/restore "
		l_n[38+7] = " stat "
		l_n[38+8] = " prob "
		l_n[38+9] = " mem "
		l_n[38+10] = " ^ "
		l_n[38+11] = " lbl/rtn "
		l_n[38+12] = " loop "
		l_n[38+13] = " flags "
		l_n[38+14] = " tests "
		l_n[38+15] = " gto "
		l_n[38+16] = "P<>R"
		l_n[38+17] = "H<>HMS"
		l_n[38+18] = "deg -> rad"
		l_n[38+19] = "Base"
		l_n[38+20] = 'Last X'
		l_n[38+21] = 'parts'
		l_n[38+22] = 'rad/deg'
		l_n[38+23] = 'disp'
		l_n[38+24] = 'clear'
		l_n[38+25] = 'complx'
		l_n[38+26] = ' pi  '
		l_n[38+27] = 'HYP'
		l_n[38+28] = 'ASIN'
		l_n[38+29] = 'ACOS'
		l_n[38+30] = 'ATAN'
		l_n[38+31] = 'x^2'
		l_n[38+32] = '10^x'
		l_n[38+33] = 'LOG'
		l_n[38+34] = '%'
		l_n[38+35] = '%CHG'
		l_n[38+36] = 'sum -'
		l_n[38+37] = self.adjust_txt('0')
		self.names = l_n
		l_but_inf = {}
		for i, el in enumerate(l_n.values()):
			#print el
			l_but_inf[i] = render_text(l_n[i], font_size = 30)
		#print(l_but_inf[0])
		tmp = [l_but_inf[i][1].w for i in range(20)]
		#print tmp
		#print max(tmp)
		return (l_n, l_but_inf, max(tmp))

def clear_memories():
	for ii in range(41):
		memories[ii] = '0'
	print('*** INFO: memories set to "0"')
		
run(MyButton())

