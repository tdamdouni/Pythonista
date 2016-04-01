#----------------------------------------------------------------------
# Copyright (c) 2012, Guy Carver
# All rights reserved.
# https://gist.github.com/GuyCarver/4000630
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#
#     * The name of Guy Carver may not be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# FILE    mazecraze.py
# BY      Guy Carver
# DATE    11/01/2012 09:15 PM
#----------------------------------------------------------------------

import ui
import motion
from scene import *
from sound import *
from random import random, randint, shuffle
from functools import partial

images = ['House','Door','Alien','Ghost','PC_Character_Horn_Girl','Cyclone','PC_Tree_Short']
sounds = ['Click_2','Ding_3','Explosion_6', 'Bleep','Powerup_3']

#Tint colors used for the teleport images.  If more teleports are added more colors should be added.
telecolors = [Color(0, 1, 0), Color(0, 0, 1),
              Color(1, 0.5, 0.3), Color(1, 1, 1)]

IPad = True
defrow = 12
rows = 14  #Number of rows for IPad at medium level.
cols = 10  #Default number of columns but this is re-calculated based on the row count.
cellsize = 32 #Default size of a maze cell.
fontsize = 20 #Size of the font for display of score and games played.
offset = Point(0, 0) #Offset from the left/bottom for the start of the maze area.  This is set when row/column counts are set.
visualize = False #Set this to true to watch the maze generate.
#The following values represent min/max/gamestep ranges.  As the # of completed mazes increase the # of the specific items increase.
numcreatures = (3, 14, 4) #Min/Maximum/level step number of creatures.
numholes = (2, 12, 3) #Min/Max/step number of holes to poke in the maze walls to make it easier to get around the creatures.
numteleports = (0, 4, 2) #Min/Maximum/step number of teleport pairs.
numbushes = (0, 10, 3) #Min/Maximum/step number of bushes.

uiimagenames = ['White_Square', 'Checkmark_3']
uiimages = [ui.Image.named(i).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL) for i in uiimagenames]
senserange = (0.02, 0.4) #Range for sensitivity slider.
mrate = 2 #Movement rate for sensitivity ball.

gravsense = 0.06  #Tilt sensitivity for player control.  Increase the # for less sensitivity.
tilt = 0.0 #Gravity y center point adjustment.

empty = 0 #Represents an empty cell (No walls)
n = 1 #North wall/direction.
e = 2 #East wall/direction.
s = 4 #South wall/direction.
w = 8 #West wall/direction.
ne = n | e
sw = s | w
allwalls = ne | sw
dirs = [n, e, s, w] #List of wall directions.  This list is shuffled for random wall/direction selection.

ms = None

def sgn(val):
  '''-1 if < 0 otherwise 1'''
  return 1 if val >= 0 else -1

def otherside(side):
  '''Given a wall side return the alternate side.'''
  if side == n:
    return s
  elif side == s:
    return n
  elif side == e:
    return w
  elif side == w:
    return e
  else:
    return empty

def left(dir):
  '''Return the left direction from the given direction.'''
  if dir == n:
    return w
  if dir == e:
    return n
  if dir == s:
    return e
  if dir == w:
    return s

def leftright(dir, right):
  '''Return either the left or right direction from the given direction.'''
  l = left(dir)
  return l if not right else otherside(l)

def gravitydirections(dir):
  '''Return a tuple of 2 directions.  The 1st tuple is the direction representing the
   largest gravity direction.  The 2nd tuple is the lesser direction.'''
  dir.y -= tilt
  ax = abs(dir.x)
  ay = abs(dir.y)
  dx = empty
  dy = empty
  #If x is larger than the sensitivity then set east or west.
  if ax > gravsense:
    dx = e if dir.x > 0 else w
  #If y is larger than the sensitivity then set north or south.
  if ay > gravsense:
    dy = n if dir.y > 0 else s

  #return direction tuple in order of largest gravity direction.
  return (dy, dx) if ay > ax else (dx, dy)

def dirtoangle(dir):
  '''given a direction return an angle.'''
  if dir == e:
    return 90
  elif dir == w:
    return 270
  elif dir == s:
    return 0
  else:
    return 180

def vector(dir):
  '''Convert direction into x,y point.'''
  x = 0
  y = 0
  if dir & n:
    y = 1
  elif dir & s:
    y = -1
  if dir & e:
    x = 1
  elif dir & w:
    x = -1
  return Point(x,y)

def walladjust(wall):
  '''This wall adjustment value is used to adust a size of the cell to let the background show through between
   the cells.  This represents the walls.'''
  adj = vector(wall)
  #The adjustment value is the negative of the vector of a wall direction.
  adj.x = -adj.x
  adj.y = -adj.y
  return adj

def rowcol( pnt ):
  '''convert screen coords into cell coords.'''
  pnt.x = int((pnt.x - offset.x) / cellsize)
  pnt.y = int((pnt.y - offset.y) / cellsize)
  return pnt

def getrect(pos):
  '''return a rect at given cell location with size of cell.'''
  return Rect(pos.x * cellsize + offset.x,
                          pos.y * cellsize + offset.y,
                          cellsize, cellsize)

def newangle(angle, spin, amount):
  '''rotate by amount in the direction of spin.
     return (new angle, spinamount)'''
  if spin < 0:
    spin += amount
    if spin > 0:
      amount -= spin
      spin = 0
    angle -= amount
  else:
    spin -= amount
    if spin < 0:
      amount += spin
      spin = 0
    angle += amount
  if angle < 0:
    angle += 360
  elif angle > 360:
    angle -= 360

  return (angle, spin)
    
def setcolor(btn):
  v = btn.superview
  c1 = v['color1']
  c2 = v['color2']

  btn.image = uiimages[1]
  ob = c1 if btn == c2 else c2
  ob.image = uiimages[0]
  csname = btn.name + 'sample'
  cs = v[csname]
  v.bgcolor = Color(*cs.background_color)
  v.fgcolor = Color(*cs.border_color)
  play_effect('Beep')

def setsense(btn):
  global gravsense
  v = btn.superview
  gravsense = ((senserange[1] - senserange[0]) * btn.value) + senserange[0]
  v['scalev'].text = '{0:.2f}'.format(gravsense)

def setvis(btn):
  play_effect('Coin_4')
  pass

def start(btn):
  play_effect('Click_1')
  v = btn.superview
  v.close()
  v.will_close()

def showhelp(btn):
  play_effect('Ding_3')
  v = btn.superview
  ht = v['helptext']
  ht.hidden = not ht.hidden
  ht.bring_to_front()
  
def settilt(btn):
  play_effect('Laser_5')
  v = btn.superview
  v['tiltview'].settilt()
  
class TiltView (ui.View):
  def __init__(self):
    self.ball = None

  def settilt(self):
    '''Reset ball position to the center of the box.'''
    global tilt
    gy, gx, gz = motion.get_gravity()
    tilt = gy
    tvx, tvy, tvw, tvh = self.frame
    self.ball.x = int(tvw / 2) - (self.ball.bounds[2] / 2) + tvx
    self.ball.y = int(tvh / 2) - (self.ball.bounds[3] / 2) + tvy
    
  def draw(self):
    '''Update the ball position based on gravity.'''
    if self.ball == None : return
    m = Point(0,0)
    gy, gx, gz = motion.get_gravity()
    gy -= tilt
    if abs(gx) >= gravsense:
      m.x = mrate * sgn(gx)
    if abs(gy) >= gravsense:
      m.y = mrate * sgn(gy)
    #If movement in x or y then update.
    if m.x or m.y:
      tvx, tvy, tvw, tvh = self.frame
      tvmaxx = tvx + tvw - self.ball.bounds[2]
      tvmaxy = tvy + tvh - self.ball.bounds[3]
      self.ball.x = max(tvx, min(tvmaxx, self.ball.x + m.x)) #Clamp values within box.
      self.ball.y = max(tvy, min(tvmaxy, self.ball.y + m.y))
      self.ball.set_needs_display()

class MyView (ui.View):
  def __init__(self):
    ui.View.__init__(self)
    self.tv = None
    self.difficulty = 1
    self.starting = True

  def setdiff(self, btn):
    play_effect('Ding_2')
    self.difficulty = btn.selected_index

  def did_load(self):
    ht = self['helptext']
    self.tv = self['tiltview']
    ht.hidden = True
    ht.y = 100
    c1 = self['color1']
    setcolor(c1)
    ss = self['sensitivity']
    
    ss.value = (gravsense - senserange[0]) / (senserange[1] - senserange[0])
    self['scalev'].text = '{0:.2f}'.format(gravsense)
    dfc = self['difficulty']
    dfc.action = self.setdiff
    dfc.selected_index = self.difficulty    

    vis = self['visualize']
    if vis:
      vis.value = False

    b = self['bubble']
    b.image = ui.Image.named('Red_Circle').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
    self.tv.ball = b
    motion.start_updates()

  def getvisualize(self):
    return self['visualize'].value

  def will_close(self):
    motion.stop_updates()
    self['startbutton'].title = 'Resume'
    if ms :
      ms.resumegame()

  def refresh(self):
    if self.tv:
      self.tv.set_needs_display()
  
class cell(Layer):
  '''Layer object used to represent a cell of the maze.'''
  def __init__(self, apos, scn):
    Layer.__init__(self)
    self.pos = apos #column/row index of the cell.
    self.frame = getrect(apos) #Convert the column/row into x,y,w,h.
    scn.add_layer(self)

  def reset(self, clr):
    '''Reset the cell in preparation for creation of a new maze.'''
    self.visited = False #Indicates whether the cell has been visited by the maze generator.
    self.tint = Color(1,1,1,1)
    self.background = clr
    self.walls = allwalls #Turn all walls on.
    self.image = None
    self.teleport = None #Cell paired with this cell if it is a teleport cell.
    self.bush = False  #Set to true if this is a bush cell.
    self.safe = False
    self.makewallimage() #Create the base frame to represent the walls set for this cell.

  def setbush(self):
    '''If cell is a basic cell make it a bush.  Return true if made a bush cell.'''
    if self.image == None:
      self.image = images[6]
      self.bush = True
    return self.bush

  def setteleport(self, other, index):
    '''If both this and the other cells are basic, then set them as teleport pairs.
       Index is used to set the pair color.'''
    if self.teleport == None: #This check is to prevent endless recursion during pair setup.
      if self.image != None: #If an image is set this is not a basic cell.
        return False

      self.teleport = other #Set teleport to the other cell.

      #Call this function for the other cell.  If returns false then other isn't a basic cell so cancel.
      if not other.setteleport(self, index):
        self.teleport = None
        return False

      self.image = images[5]
      #Set the tint color.  Index starts at numteleports so subtract 1 to make it 0 based.
      self.tint = telecolors[index - 1]

    return True

  def makewallimage(self):
    '''Create the wall image with empty space on the sides with walls to allow the background to show through representing the wall.'''
    wh = walladjust(self.walls & ne)
    xy = walladjust(self.walls & sw)
    self.frame = getrect(self.pos)
    self.frame.x += xy.x
    self.frame.y += xy.y
    self.frame.w += wh.x - xy.x
    self.frame.h += wh.y - xy.y

  def clearwall(self, wall):
    '''Clear bit representing a wall.'''
    self.walls &= ~wall

  def setwall(self, wall):
    '''Set bit representing a wall.'''
    self.walls |= wall

  def testwall(self, wall):
    '''Test to see if wall exists.'''
    return self.walls & wall

  def deadend(self):
    '''If 3 walls are set then this is a deadend.'''
    w = 0
    for i in range(4):
      if self.walls & (1 << i):
        w += 1
    return (w == 3)

  def openwall(self, other, wall):
    '''Open wall then clear the opposite wall in the given neighbor cell.'''
    self.clearwall(wall)
    other.clearwall(otherside(wall))
    #Recalculate the images.
    self.makewallimage()
    other.makewallimage()
#    self.background = Color(1,1,0)
#    other.background = Color(0.8, 1, 0.4)

class creature(Layer):
  '''represents a creature.'''
  def __init__(self, scn):
    Layer.__init__(self)
    #NOTE: The following 2 function pointers could have been empty functions in this class that child classes
    # would override but shows an alternate method of doing that.
    self.face = None #Function to call to set facing of a movement direction.  By default this is not on.
    self.playstep = None #Function to call to play step sound.
    self.auto = True #True means movement is automatic.
    self.speed = 0.5 #Movement speed.
    self.background = Color(0,0,0,0)
    self.tint = Color(1,1,1,0)
    self.movedone = self.setposandmove #Default function to call when movement animation is done.
    self.scene = scn #The maze to which this creature is attached.
    self.reset()
    scn.add_layer(self)

  def setpos(self, pos):
    '''force creature to a position.'''
    self.pos = pos
    self.moving = False #Movement animation is not on.
    self.frame = getrect(self.pos) #Set the frame to the position.  This is redundant after animation is complete but useful for teleport.

  def setposandmove(self, pos):
    '''Set the position then start movement again.'''
    self.setpos(pos)
    self.move()

  def reset(self):
    '''Reset the creature in preparation for a new game.'''
    #Random start position.
    pos = Point(randint(int(cols / 4), cols - 1), randint(0, rows - 1))
    self.setpos(pos)
    #Random movement direction.
    self.dir = dirs[randint(0, len(dirs)-1)]
    #Random image for the creature.
    self.image = images[randint(2, 3)]
    #Start invisible.
    self.alpha = 0

  def colrect(self):
    '''Get the rect used for collision detection.'''
    f = self.frame
    #The adjustment values should be a % of the cell size.
    return Rect(f.x + 8, f.y + 8,f.w - 16, f.h - 16)

  def checkcollide(self, rct):
    '''Check if the collision rectangle for this creature intersects the given rectangle.'''
    return self.colrect().intersects(rct)

  def shouldpickdir(self, blocked):
    '''Return true if should pick a new direction.'''
    return blocked or random() < 0.4

  def testdir(self):
    '''Test to see if a direction is blocked.'''
    #Get the cell the creature is on.
    c = self.scene.getcell(self.pos)
    #Check if blocked in the direction we are moving.
    blocked = c.testwall(self.dir)
    #Determine if we should pick a new direction.
    if self.shouldpickdir(blocked):
      #If so try left/right from direction we are moving.
      lr = randint(0, 1)
      newdir = leftright(self.dir, lr)
      #If that direction is blocked check the other side.
      if c.testwall(newdir):
        newdir = otherside(newdir)
        #If that direction is blocked then if we are blocked in the direction we
        # are moving we'll have to turn around.
        if c.testwall(newdir):
          if blocked:
            newdir = otherside(self.dir)
          else:
            newdir = self.dir

      self.dir = newdir
      blocked = False #picked a new direction so no longer blocked.

    return blocked

  def move(self):
    '''if not moving and not blocked in the movement direction then start movement anims in the given direction.'''
    if not self.moving and not self.testdir():
      pos = Point(0, 0)
      if self.face:
        self.face() #Call function to face direction we are moving.

      mv = vector(self.dir)
      #If any movement then start animation.
      if mv.x or mv.y:
        pos.x = self.pos.x + mv.x
        pos.x = min(max(0, pos.x), cols-1) #clamp x within columns.
        pos.y = self.pos.y + mv.y
        pos.y = min(max(0, pos.y), rows - 1) #clamp y to row count which includes empty row at top.
                                                                            # also allow -1 for empty row at bottom.
        self.moving = True #Set flag indicating we are moving.
        torect = getrect(pos) #Get rectangle for the destination column, row.
        fun = partial(self.movedone, pos) #function to call when animation is done (movedone with pos as parameter).
        if self.playstep:
          self.playstep() #Call step sound function.
        self.animate('frame', torect, self.speed, curve=curve_linear, completion = fun)

class player(creature):
  '''Extend the creature class to represent the player.'''
  def __init__(self, scn):
    creature.__init__(self, scn)
    self.face = self.doface #Function to call to face movement direction.
    self.playstep = self.doplaystep #Function to call to play step sound.
    self.auto = False #Don't do auto movement as the player controls movement.
    self.image = images[4]
    self.movedone = self.setpos #Set function to call when movement animation is done.
    self.reset()

  def reset(self):
    '''Reset player for new game.'''
    self.dir = e
    self.speed = 0.3
    self.sounddelay = 0.0 #Delay timer to use for playing hit sound (Keeps the sound from spamming).
    self.alpha = 0
    self.hitcount = 0 #Number of times hit by a creature (score).
    self.hold = False #When set to true gravity movement is not possible.
    self.spinning = 0

  def shouldpickdir(self, blocked):
    '''Override creature shouldpickdir to always return false because the player picks.'''
    return False

  def doface(self):
    '''Animation direction. If no direction to turn or spinning then skip.'''
    if self.dir != empty and self.spinning == 0:
      self.animate('rotation', dirtoangle(self.dir), 0.2, curve=curve_linear)

  def doplaystep(self):
    '''Play footstep sound.'''
    play_effect(sounds[0], 0.06)

  def blocked(self, dir):
    '''Return true if movement is blocked in the given direction from the players cell.'''
    return self.scene.getcell(self.pos).testwall(dir)

  def caught(self):
    '''If the player is not hiding then set caught.'''
    if self.alpha > 0.5:
      #Can't get caught too many times so if sound delay is on (from last catch) then skip.
      if self.sounddelay == 0:
        play_effect(sounds[2], 0.05)
        self.sounddelay = 1.0 #Set sound delay to 1 second.
        self.hitcount += 1 #Increment hit count.
      self.speed = 2.5 #Set movement delay.

  def tryteleport(self):
    '''Try to teleport.'''
    #Can't be moving to teleport.
    if not self.moving:
      #Get the current cell and see if it's a teleport.
      c = self.scene.getcell(self.pos)
      if c.teleport != None:
        self.spinning = 720 #spin around twice.
        play_effect(sounds[4])
        self.setpos(c.teleport.pos)

  def setpos(self, pos):
    '''Set the position then check if we are on a special cell.'''
    creature.setpos(self, pos)
    c = self.scene.getcell(self.pos)
    #If on the end cell then game is over.
    if c == self.scene.end:
      self.scene.setwon()
    elif c.bush: #If on a bush then hide by setting alpha.
      self.animate('alpha', 0.2, 0.5, curve=curve_linear)
    elif self.alpha != 1: #If not at full alpha then set to full.
      self.animate('alpha', 1, 0.5, curve=curve_linear)

  def update(self, dt):
    '''If sound delay then update it.'''
    if self.sounddelay > 0:
      self.sounddelay = max(0, self.sounddelay - 0.5 * dt)

    #if spinning then do so but dont allow movement.
    if self.spinning != 0:
      self.rotation, self.spinning = newangle(self.rotation, self.spinning, 720.0 * 2 * dt)
    #If not moving and allowed to move then do so.
    elif not self.moving and self.speed < 2.0 and not self.hold :
      gdrs = gravitydirections(gravity())
      #Loop for the directions returned by gravitydirections.
      for d in gdrs:
        #If not blocked then move in this direction.
        if not self.blocked(d):
          self.dir = d
          #Don't try to move if direction is empty.
          if d != empty:
            self.move()
            break

    #If we are slowed down then slowly speed up.
    if self.speed > 0.3:
      self.speed = max(0.3, self.speed - 0.1 * dt)

    #Call the creature update function.
    creature.update(self, dt)

class MazeScene (Scene):
  def __init__(self):
    Scene.__init__(self)
    self.start = None #Start cell.
    self.end = None   #End cell.
    self.state = self.donothing #Set update/render state function (Start with options).
    self.games = 0 #Number of games played.
    self.numcreatures = numcreatures[0] #Number of creatures to start with.
    self.teleports = 0
    self.prevstate = None
    self.wantstate = None
    
  def setup(self):
    global IPad
    IPad = self.size.w > 700

    self.scorepos = Point(self.bounds.w - 120, self.bounds.h - 18)
    self.gamepos = Point(120, self.bounds.h - 18)
    self.root_layer = Layer(self.bounds)

    self.pausetext, sz = render_text('PAUSE', 'Copperplate-Bold', fontsize)
    self.pauserect = Rect(self.bounds.center().x - sz.w / 2, self.bounds.h - fontsize - 5, *sz)
    self.pausebuttonrect = Rect(self.pauserect.x - 5, self.pauserect.y - 2, self.pauserect.w + 10, self.pauserect.h + 4)

    #Have to do this load_image() here or the images do not draw correctly.     
    #Pre-load images to prevent hitching.
    for image in images:
      load_image(image)

    #Pre-load sounds to prevent hitching.
    for s in sounds:
      load_effect(s)

  def loadoptionscreen(self):
    '''Load the option screen ui and queue the state to show it.'''
    self.optionscreen = ui.load_view('mazecraze') #Create the options screen.
    self.wantstate = self.showoptionscreen

  def donothing(self):
    '''empty state'''
    pass

  def setwon(self):
    '''set update/render state for ended game.'''
    play_effect(sounds[1])
    self.wantstate = self.wonstate
    self.games += 1

  def getcell(self, apos):
    '''If position is within the maze grid then return the cell at that position.'''
    if apos.x >= 0 and apos.x < cols and apos.y >= 0 and apos.y < rows:
      return self.maze[apos.y][apos.x]
    else:
      return None

  def neighbor(self, acell):
    '''Randomly check the neighbors of a cell for an unvisited cell.
       Return the cell and the direction relative to the given cell.'''
    shuffle(dirs)
    for d in dirs:
      mv = vector(d)
      mv.x += acell.pos.x
      mv.y += acell.pos.y
      nc = self.getcell(mv)
      if nc != None and not nc.visited:
        return nc, d

    return None, empty

  def initgame(self):
    '''initialize system options and start a new game.'''
    global cellsize
    global offset
    global cols
    global rows

    #Size of maze based on difficulty level. # of rows increases by 2 per level.
    rows = defrow + (2 * self.optionscreen.difficulty)

    #If on IPhone.
    if not IPad:
      rows -= 3

    #Calculate playing area size.
    cellsize = self.size.h / (rows + 2)
    cols = int(self.size.w / cellsize) - 2
    offset.x = int((self.size.w - (cols * cellsize)) / 2)
    offset.y = int((self.size.h - (rows * cellsize)) / 2)

    #Create list of cells.
    self.maze = [[cell(Point(c,r), self) for c in xrange(cols)] for r in xrange(rows)]
    #Create list of base # of creatures.
    self.creatures = [creature(self) for i in range(1)]
    self.player = player(self)
    self.newgame()

  def newgame(self):
    '''Initialize a new game and start maze building.'''
    self.wantstate = self.constructionstate

    bgclr = self.optionscreen.bgcolor
    #Reset the cells in the maze.
    for r in self.maze:
      for c in r:
        c.reset(bgclr)

    #Reset the creatures.
    for cr in self.creatures:
      cr.reset()

    self.player.reset() #Reset player to beginning.
    self.stk = [] #Create stack for recursive visitation of cells in maze generation.

    #Pick a random starting position.
    pos = Point()
    pos.x = randint(0, cols - 1)
    pos.y = randint(0, rows - 1)
    self.c = self.getcell(pos)

    #We want to visualize for at least 1 frame to get the scene displayed.
    self.visualize = -1 if self.optionscreen.getvisualize() else 1

  def setcolor(self, bgclr):
    #set color of cells in the maze.
    for r in self.maze:
      for c in r:
        c.background = bgclr

  def startcreatures(self):
    '''Start creatures moving.'''
    #Set the number of creatures.
    step = numcreatures[2] - self.optionscreen.difficulty
    self.numcreatures = min(numcreatures[1], (numcreatures[0] + (self.games / step)))
    dif = self.numcreatures - len(self.creatures)
    #Make sure enough creatures exist.
    for a in range(dif):
      self.creatures.append(creature(self))

    #Make creatures visible and start moving.
    for cr in self.creatures:
      cr.alpha = 1
      cr.move()

  def playervmonster(self):
    '''Check for player vs monster collision.'''
    c = self.getcell(self.player.pos)
    if not c.safe:
      r = self.player.colrect()
      for c in self.creatures:
        if c.checkcollide(r):
          self.player.caught()
          break

  def setstart(self):
    '''Set the starting cell and place the player there.'''
    r = randint(0, rows - 1)
    self.start = self.maze[r][0]
    self.start.tint = Color(1,1,1,1)
    self.start.image = images[1]
    self.start.safe = True
    self.player.setpos(Point(0, r))
    self.player.alpha = 1 #Make player visible.

  def setend(self):
    '''Set the end cell to the 1st deadend we find from the right side of the maze.'''
    self.end = None
    pos = Point(cols - 1, 0)
    r = randint(0, rows - 1)

    def checkrows(r0, r1):
      '''Check cell in rows within the range.'''
      for rw in range(r0, r1):
        pos.y = rw
        cl = self.getcell(pos)
        if cl.deadend():
          self.end = cl
          break

    #Loop until we've covered all cells or found an end cell position.
    while pos.x >= 0 and self.end == None:
      checkrows(r, rows)
      if self.end == None:
        checkrows(0, r)
      pos.x -= 1 #Move left 1 column.

    if self.end != None:
      self.end.image = images[0]
      self.end.tint = Color(1,1,1,1)

  def makebushes(self):
    '''Randombly place bushes in the maze.'''
    step = numbushes[2] + self.optionscreen.difficulty
    self.bushes = min(numbushes[1], int(numbushes[0] + (self.games / step)))
    ind = self.bushes
    while (ind):
      r = randint(0, rows - 1)
      c = randint(2, cols - 1) #Don't place bush in 1st 2 columns.
      cl = self.getcell(Point(c, r))
      #If bush placement was successfull.
      if cl.setbush():
        ind -= 1

  def maketeleports(self):
    '''Randomly place teleport pairs in the maze.'''
    step = numteleports[2] + self.optionscreen.difficulty
    self.teleports = min(numteleports[1], int(numteleports[0] + (self.games / step)))
    ind = self.teleports
    rm = (rows - 1) / 2 #Place 1st teleport portal in top half of maze.
    while (ind):
      r = randint(0, rm)
      c = randint(0, cols - 2)
      cl1 = self.getcell(Point(c,r))
      #Place 2nd teleport portal in bottom half of maze.
      r = randint(rm + 1, rows - 1)
      c = randint(0, cols - 3)
      cl2 = self.getcell(Point(c,r))
      #If set was successfull.
      if cl1.setteleport(cl2, ind):
        ind -= 1

  def makeholes(self):
    '''Randomly remove walls in the generated maze.'''
    step = numholes[2] - self.optionscreen.difficulty
    self.holes = max(numholes[0], numholes[1] - (self.games / step))

    for i in range(self.holes):
      r = randint(1, rows - 2)
      c = randint(1, cols - 2)
      cl = self.getcell(Point(c, r))
      shuffle(dirs) #Randomize wall directions.
      #Find a set wall.
      for d in dirs:
        if cl.testwall(d):
          mv = vector(d)
          mv.x += cl.pos.x
          mv.y += cl.pos.y
          ncl = self.getcell(mv)
          #Open the wall.
          cl.openwall(ncl, d)
          break

  def updatemaze(self):
    '''Update the maze generation.'''
    #While a cell is left to visit.
    while self.c != None:
      self.c.visited = True #Set cell as visited.
      nc, d = self.neighbor(self.c) #Get a random neighbor.
      #If no unvisited neighbor then go back.
      if d == empty:
        if (self.visualize < 0):
          self.c.background = self.optionscreen.bgcolor
        self.c.makewallimage()
        #If anything is in the stack the get the last entry.
        if len(self.stk):
          self.c = self.stk.pop()
        else: #We are done so start the game.
          self.c = None #No more cells to update.
          self.makeholes()
          self.setstart()
          self.setend()
          self.maketeleports()
          self.makebushes()
          self.startcreatures()
          play_effect(sounds[3]) #Play game start sound.
          self.wantstate = self.playstate #Set the update/render state for playing.
      else:
        self.c.openwall(nc, d) #Open wall between cell and neighbor.
        if (self.visualize < 0):
          self.c.background = Color(1,0,0,1)
          self.c.makewallimage()
        #Add the cell to the stack.
        self.stk.append(self.c)
        self.c = nc #Set the current cell to the neighbor.
      if self.visualize:
        if self.visualize > 0: #If visualization is > 0 then count down to 0.
          self.visualize -= 1
        break #We are generating 1 cell at a time so exit loop.

  def drawscore(self):
    '''Draw the score strings.'''
    tint(1,0,0,1)
    text('score: ' + str(self.player.hitcount), 'Copperplate-Bold', fontsize, *self.scorepos.as_tuple())
    text('games: ' + str(self.games), 'Copperplate-Bold', fontsize, *self.gamepos.as_tuple())
    tint(1,1,1,1)
    image('White_Square', *self.pausebuttonrect)
    tint(1,0,0,1)
    image(self.pausetext, *self.pauserect)

  def resumegame(self):
    '''Resume game from pause state.'''
    if self.prevstate != None :
      self.wantstate = self.prevstate
      self.prevstate = None
      self.setcolor(self.optionscreen.bgcolor)
    else:
      self.wantstate = self.initgame

  def pausegame(self):
    play_effect('8ve-tap-wooden')
    '''Pause game and show the options screen.'''
    self.prevstate = self.state
    self.showoptionscreen()
    
  def showoptionscreen(self):
    self.wantstate = self.optionstate
    self.optionscreen.present(style='popover', hide_title_bar=True, orientations=['landscape-right'])
 #   self.optionscreen.wait_modal()

  def optionstate(self):
    '''Draw the options screen.'''
#    background(0,0,0)
    self.optionscreen.refresh()

  def constructionstate(self):
    '''Update initialization and draw the creating maze string.'''
    self.root_layer.draw()
    tint(0,1,1,1)
    s = 40 if IPad else 17
    text('creating maze', 'Futura', s, *self.bounds.center().as_tuple())
    self.updatemaze()

  def playstate(self):
    '''Update the game and draw the score.'''
    self.root_layer.update(self.dt)
    self.playervmonster()
    self.root_layer.draw()
    self.drawscore()

  def wonstate(self):
    '''Draw the won message.'''
    self.root_layer.draw()
    tint(0,1,1,1)
    self.drawscore()
    s = 80 if IPad else 20
    text('You won!', 'Futura', s, *self.bounds.center().as_tuple())

  def draw(self):
    '''Set the background then call the current state.'''
    c = self.optionscreen.fgcolor
    background(c.r, c.g, c.b)
    #If a new state is desired switch to it.
    if self.wantstate :
      self.state = self.wantstate
      self.wantstate = None
    self.state()

  def touch_began(self, touch):
    '''Handle touch events.'''
    #Check if pause button pressed.
    loc = Rect(touch.location.x, touch.location.y, 1, 1)
    if touch.location in self.pausebuttonrect:
      self.pausegame()
    else:
      #If touching the screen hold the player at his current position.
      self.player.hold = True

  def touch_ended(self, touch):
    '''Handle touch end events.'''
    #Player free to move.
    self.player.hold = False
    #If game is over start a new one.
    if self.state == self.wonstate:
      self.newgame()
    else:
      #See if player is on a teleport cell.
      self.player.tryteleport()

#Run in landscape mode.
ms = MazeScene()
ms.loadoptionscreen()
run(ms, LANDSCAPE)