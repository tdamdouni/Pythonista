# https://forum.omz-software.com/topic/2718/crash-when-using-sleep-in-scene-module

@ui.in_background
	def go(self, start_square):
		try:
			self.green_list.remove(start_square)
		except:
			pass
		for square in start_square.white_neighbours(self.squares):
			self.green_list.append(square)
			square.run_action(go_action)
			square.state = 3
			square.color = color4
			sleep(0.004)
			self.go(square)
		if len(self.green_list) == 0:
			sleep(0.004)
			self.check_win()
			
# --------------------
start_square# --------------------
self.green_list# --------------------
while len(mydeque):
	square =mydeque.pop()
	#process square.......... change color, etc
	for n in square.white_neighbors():
		if n not in mydeque:
			mydeque.append(n)
# --------------------
Action.call()# --------------------
time.sleep()# --------------------
@ui.in_background# --------------------
def go(self, start_square):

	def cascade(node, progress):
		# Nested animation function
		if progress == 1 and self.win:
			node.color = color4
		elif progress == 1 and not self.win:
			node.color = color3
			
	self.green_list.append(start_square)
	index = 0.01
	while self.green_list:
		square = self.green_list.pop(randint(0, len(self.green_list) - 1)) # Pop a random square from the list of squares (initially just the start_square)
		square.run_action(A.call(cascade, index)) # Calls the nested cascade() function with index as the duration
		index += 0.01 # The delay increments, meaning the animation cascades through the squares
		
		for n in square.white_neighbours(self.squares):
			if n not in self.green_list:
				self.green_list.append(n)
				
		# Once list is empty, check win status
		self.check_win()
# --------------------
	@ui.in_background
	def go(self, start_square):
		try:
			self.green_list.remove(start_square)
		except:
			pass
		for square in start_square.white_neighbours(self.squares):
			self.green_list.append(square)
			square.run_action(go_action)
			square.state = 3
			square.color = color4
			sleep(0.004)
			self.go(square)
		if len(self.green_list) == 0:
			sleep(0.004)
			self.check_win()
			
# --------------------
start_square# --------------------
self.green_list# --------------------
while len(mydeque):
	square =mydeque.pop()
	#process square.......... change color, etc
	for n in square.white_neighbors():
		if n not in mydeque:
			mydeque.append(n)
# --------------------
Action.call()# --------------------
time.sleep()# --------------------
@ui.in_background# --------------------
def go(self, start_square):

	def cascade(node, progress):
		# Nested animation function
		if progress == 1 and self.win:
			node.color = color4
		elif progress == 1 and not self.win:
			node.color = color3
			
	self.green_list.append(start_square)
	index = 0.01
	while self.green_list:
		square = self.green_list.pop(randint(0, len(self.green_list) - 1)) # Pop a random square from the list of squares (initially just the start_square)
		square.run_action(A.call(cascade, index)) # Calls the nested cascade() function with index as the duration
		index += 0.01 # The delay increments, meaning the animation cascades through the squares
		
		for n in square.white_neighbours(self.squares):
			if n not in self.green_list:
				self.green_list.append(n)
				
		# Once list is empty, check win status
		self.check_win()
# --------------------
		if progress == 1:
			node.color = color4 if self.win else color3
# --------------------

