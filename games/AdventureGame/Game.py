from __future__ import print_function
import json
import sqlite3
import cmd
import textwrap
import shutil
import tempfile
 
def get_room(id, dbfile='rooms.sqlite'):
  ret = None
    
  con = sqlite3.connect(dbfile)
  
  try:
  	rows = con.execute("select json from rooms where id=?", (id,))
  except Exception as e:
  	print('DB ERROR', e)
    
  for row in rows:
  	jsontext = row[0]
  	d = json.loads(jsontext)
  	d['id'] = id
  	ret = Room(**d)
  	break
      
  con.close()
    
  return ret
 
class Room():
  def __init__(self, id=0, name="A Room", description="An empty room", neighbors={}):
    self.id = id
    self.name = name
    self.description = description
    self.neighbors = neighbors
      
  def _neighbor(self, direction):
    if direction in self.neighbors:
      return self.neighbors[direction]
    else:
      return None
      
  def north(self):
    return self._neighbor('n')
  
  def south(self):
    return self._neighbor('s')
      
  def east(self):
    return self._neighbor('e')
      
  def west(self):
    return self._neighbor('w')
 
class Game(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self)
    
    self.dbfile = 'rooms.sqlite' #tempfile.mktemp()
    #shutil.copyfile("rooms.sqlite", self.dbfile)]
    
    self.loc = get_room(1, self.dbfile)
    self.look()
      
  def move(self, dir):
    newroom = self.loc._neighbor(dir)
    if newroom is None:
      print("you can't go that way")
    else:
      self.loc = get_room(newroom, self.dbfile)
      self.look()
        
    if newroom==13:
      exit()
    
  def look(self):
    print('### %s ###' % self.loc.name)
    print("")
    for line in textwrap.wrap(self.loc.description, 72):
      print(line)
 
  def do_up(self, args):
    """Go up"""
    self.move('up')
  
  def do_down(self, args):
    """Go down"""
    self.move('down')
  
  
  def do_n(self, args):
    """Go north"""
    self.move('n')
  
  def do_s(self, args):
    """Go south"""
    self.move('s')
      
  def do_e(self, args):
    """Go east"""
    self.move('e')
  
  def do_w(self, args):
    """Go west"""
    self.move('w')
  
  def do_quit(self, args):
    """Leaves the game"""
    print("Thank you for playing")
    return True
 
  def do_save(self, args):
    """Saves the game"""
    shutil.copyfile(self.dbfile, args)
    print("The game was saved to {0}".format(args))
      
if __name__ == "__main__":
  g = Game()
  g.cmdloop()