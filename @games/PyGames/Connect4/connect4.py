# coding=UTF8

# Python Connect4 game with AI using MTD(f) algorithm
# Author: Maurits van der Schee <maurits@vdschee.nl>

from Tkinter import Tk, Button, Frame, Canvas
from tkFont import Font
from copy import deepcopy
from time import time

class Board:

  nodes = {}

  def __init__(self,other=None):
    self.player = 'X'
    self.opponent = 'O'
    self.empty = '.'
    self.width = 7
    self.height = 6
    self.fields = {}
    for y in range(self.height):
      for x in range(self.width):
        self.fields[x,y] = self.empty
    # copy constructor
    if other:
      self.__dict__ = deepcopy(other.__dict__)

  def move(self,x):
    board = Board(self)
    for y in range(board.height):
      if board.fields[x,y] == board.empty:
        board.fields[x,y] = board.player
        break
    board.player,board.opponent = board.opponent,board.player
    return board

  def __heuristic(self):
    return self.__heuristic_score(self.player)-self.__heuristic_score(self.opponent)

  def __heuristic_score(self, player):
    lines = self.__winlines(player)
    winpositions = self.__winpositions(lines,player)
    score = 0
    for x in range(self.width):
      for y in range(self.height-1,0,-1):
        win = winpositions.get("{0},{1}".format(x,y),False)
        below = winpositions.get("{0},{1}".format(x,y-1),False)
        if win and below:
          score+=self.height-y*100
    for line in lines:
      pieces = 0
      height = []
      for x,y in line:
        if self.fields[x,y] == player:
          pieces = pieces + 1
        elif self.fields[x,y] == self.empty:
          height.append(y)
      heightscore = self.height - int(sum(height) / float(len(height)))
      score=score+pieces*heightscore
    return score

  def __winpositions(self, lines, player):
    lines = self.__winlines(player)
    winpositions = {}
    for line in lines:
      pieces = 0
      empty = None
      for x,y in line:
        if self.fields[x,y] == player:
          pieces = pieces + 1
        elif self.fields[x,y] == self.empty:
          if not empty == None:
            break
          empty = (x,y)
      if pieces==3:
        winpositions["{0},{1}".format(x,y)]=True
    return winpositions

  def __winlines(self, player):
    lines = []
    # horizontal
    for y in range(self.height):
      winning = []
      for x in range(self.width):
        if self.fields[x,y] == player or self.fields[x,y] == self.empty:
          winning.append((x,y))
          if len(winning) >= 4:
            lines.append(winning[-4:])
        else:
          winning = []
    # vertical
    for x in range(self.width):
      winning = []
      for y in range(self.height):
        if self.fields[x,y] == player or self.fields[x,y] == self.empty:
          winning.append((x,y))
          if len(winning) >= 4:
            lines.append(winning[-4:])
        else:
          winning = []
    # diagonal
    winning = []
    for cx in range(self.width-1):
      sx,sy = max(cx-2,0),abs(min(cx-2,0))
      winning = []
      for cy in range(self.height):
        x,y = sx+cy,sy+cy
        if x<0 or y<0 or x>=self.width or y>=self.height:
          continue
        if self.fields[x,y] == player or self.fields[x,y] == self.empty:
          winning.append((x,y))
          if len(winning) >= 4:
            lines.append(winning[-4:])
        else:
          winning = []
    # other diagonal
    winning = []
    for cx in range(self.width-1):
      sx,sy = self.width-1-max(cx-2,0),abs(min(cx-2,0))
      winning = []
      for cy in range(self.height):
        x,y = sx-cy,sy+cy
        if x<0 or y<0 or x>=self.width or y>=self.height:
          continue
        if self.fields[x,y] == player or self.fields[x,y] == self.empty:
          winning.append((x,y))
          if len(winning) >= 4:
            lines.append(winning[-4:])
        else:
          winning = []
    # return
    return lines

  def __iterative_deepening(self,think):
    g = (3,None)
    start = time()
    for d in range(1,10):
      g = self.__mtdf(g, d)
      if time()-start>think:
        break
    return g;

  def __mtdf(self, g, d):
    upperBound = +1000
    lowerBound = -1000
    best = g
    while lowerBound < upperBound:
      if g[0] == lowerBound:
        beta = g[0]+1
      else:
        beta = g[0]
      g = self.__minimax(True, d, beta-1, beta)
      if g[1]!=None:
        best = g
      if g[0] < beta:
        upperBound = g[0]
      else:
        lowerBound = g[0]
    return best

  def __minimax(self, player, depth, alpha, beta):
    lower = Board.nodes.get(str(self)+str(depth)+'lower',None)
    upper = Board.nodes.get(str(self)+str(depth)+'upper',None)
    if lower != None:
      if lower >= beta:
        return (lower,None)
      alpha = max(alpha,lower)
    if upper != None:
      if upper <= alpha:
        return (upper,None)
      beta = max(beta,upper)
    if self.won():
      if player:
        return (-999,None)
      else:
        return (+999,None)
    elif self.tied():
      return (0,None)
    elif depth==0:
      return (self.__heuristic(),None)
    elif player:
      best = (alpha,None)
      for x in range(self.width):
        if self.fields[x,self.height-1]==self.empty:
          value = self.move(x).__minimax(not player,depth-1,best[0],beta)[0]
          if value>best[0]:
            best = value,x
          if value>beta:
            break
    else:
      best = (beta,None)
      for x in range(self.width):
        if self.fields[x,self.height-1]==self.empty:
          value = self.move(x).__minimax(not player,depth-1,alpha,best[0])[0]
          if value<best[0]:
            best = value,x
          if alpha>value:
            break
    if best[0] <= alpha:
      Board.nodes[str(self)+str(depth)+"upper"] = best[0]
      Board.nodes[self.__mirror()+str(depth)+"upper"] = best[0]
    elif best[0] >= beta:
      Board.nodes[str(self)+str(depth)+"lower"] = best[0]
      Board.nodes[self.__mirror()+str(depth)+"lower"] = best[0]
    return best

  def best(self):
    return self.__iterative_deepening(2)[1]

  def tied(self):
    for (x,y) in self.fields:
      if self.fields[x,y]==self.empty:
        return False
    return True

  def won(self):
    # horizontal
    for y in range(self.height):
      winning = []
      for x in range(self.width):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
          if len(winning) == 4:
            return winning
        else:
          winning = []
    # vertical
    for x in range(self.width):
      winning = []
      for y in range(self.height):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
          if len(winning) == 4:
            return winning
        else:
          winning = []
    # diagonal
    winning = []
    for cx in range(self.width-1):
      sx,sy = max(cx-2,0),abs(min(cx-2,0))
      winning = []
      for cy in range(self.height):
        x,y = sx+cy,sy+cy
        if x<0 or y<0 or x>=self.width or y>=self.height:
          continue
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
          if len(winning) == 4:
            return winning
        else:
          winning = []
    # other diagonal
    winning = []
    for cx in range(self.width-1):
      sx,sy = self.width-1-max(cx-2,0),abs(min(cx-2,0))
      winning = []
      for cy in range(self.height):
        x,y = sx-cy,sy+cy
        if x<0 or y<0 or x>=self.width or y>=self.height:
          continue
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
          if len(winning) == 4:
            return winning
        else:
          winning = []
    # default
    return None

  def __mirror(self):
    string = ''
    for y in range(self.height):
      for x in range(self.width):
        string+=' '+self.fields[self.width-1-x,self.height-1-y]
      string+="\n"
    return string

  def __str__(self):
    string = ''
    for y in range(self.height):
      for x in range(self.width):
        string+=' '+self.fields[x,self.height-1-y]
      string+="\n"
    return string

class GUI:

  def __init__(self):
    self.app = Tk()
    self.app.title('Connect4')
    self.app.resizable(width=False, height=False)
    self.board = Board()
    self.buttons = {}
    self.frame = Frame(self.app, borderwidth=1, relief="raised")
    self.tiles = {}
    for x in range(self.board.width):
      handler = lambda x=x: self.move(x)
      button = Button(self.app, command=handler, font=Font(family="Helvetica", size=14), text=x+1)
      button.grid(row=0, column=x, sticky="WE")
      self.buttons[x] = button
    self.frame.grid(row=1, column=0, columnspan=self.board.width)
    for x,y in self.board.fields:
      tile = Canvas(self.frame, width=60, height=50, bg="navy", highlightthickness=0)
      tile.grid(row=self.board.height-1-y, column=x)
      self.tiles[x,y] = tile
    handler = lambda: self.reset()
    self.restart = Button(self.app, command=handler, text='reset')
    self.restart.grid(row=2, column=0, columnspan=self.board.width, sticky="WE")
    self.update()

  def reset(self):
    self.board = Board()
    self.update()

  def move(self,x):
    self.app.config(cursor="watch")
    self.app.update()
    self.board = self.board.move(x)
    self.update()
    move = self.board.best()
    if move!=None:
      self.board = self.board.move(move)
      self.update()
    self.app.config(cursor="")

  def update(self):
    for (x,y) in self.board.fields:
      text = self.board.fields[x,y]
      if (text=='.'):
        self.tiles[x,y].create_oval(10, 5, 50, 45, fill="black", outline="blue", width=1)
      if (text=='X'):
        self.tiles[x,y].create_oval(10, 5, 50, 45, fill="yellow", outline="blue", width=1)
      if (text=='O'):
        self.tiles[x,y].create_oval(10, 5, 50, 45, fill="red", outline="blue", width=1)
    for x in range(self.board.width):
      if self.board.fields[x,self.board.height-1]==self.board.empty:
        self.buttons[x]['state'] = 'normal'
      else:
        self.buttons[x]['state'] = 'disabled'
    winning = self.board.won()
    if winning:
      for x,y in winning:
        self.tiles[x,y].create_oval(25, 20, 35, 30, fill="black")
      for x in range(self.board.width):
        self.buttons[x]['state'] = 'disabled'

  def mainloop(self):
    self.app.mainloop()

if __name__ == '__main__':
  GUI().mainloop()
