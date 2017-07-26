# coding: utf-8

# https://forum.omz-software.com/topic/3796/added-physics-to-game-tutorial-for-realistic-player-movement

'''
Part 7 -- Space Lasers! ✳️

The whole game has been somewhat defensive so far, so let's give the little alien something to attack -- lasers!

When a laser hits a meteor, it should be destroyed in an explosion, and as additional motivation to shoot them down, a destroyed meteor leaves behind a valuable star coin to collect.

A laser is shot when you tap anywhere on the screen, by implementing the `touch_began()` method. A maximum of 3 lasers can be on the screen at once; maybe the laser gun needs recharging -- in any case, it's supposed to discourage simply hammering on the screen the entire time.

Overall, lasers are similar to coins and meteors, but they move upwards, and only collide with meteors, not the player. Because of that, their collisions are handled in a separate method.

When a laser hits a meteor, its texture is replaced with a star (that is then basically treated like a coin), and a couple of smaller rocks move in all directions to simulate an explosion with a simple particle effect.

This concludes the tutorial. I hope you enjoyed watching this little game grow.

Of course, there's a lot more you can do with this basic concept. Here are some ideas that you could try:

* Save highscores to a file?
* Replace the alien with a space ship?
* Use touch instead of motion to control movement?
* Add some enemy space ships that also shoot lasers?
* Add some additional items to collect, maybe power-ups for the laser?
* Make a "hard mode" where the game is over when a meteor hits the ground?
* Instead of just picking random positions, maybe add the coins and meteors using interesting patterns?
* ...

Modified by Ed Suominen (edsuom.com) to make player motion more
realistic. Yay physics! Also couldn't help doing a little cleanup
of some long lines here and there in the code. No copyright claimed
to changes from Tutorial Part 7.py, included with Pythonista and
upon which this adaptation is based.
'''

from scene import *
import sound, random
from math import sin, cos, pi
A = Action

def cmp(a, b):
  return ((a > b) - (a < b))

standing_texture = Texture('plf:AlienGreen_front')
walk_textures = [Texture('plf:AlienGreen_walk1'), Texture('plf:AlienGreen_walk2')]
hit_texture = Texture('plf:AlienGreen_hit')

class Coin (SpriteNode):
  def __init__(self, **kwargs):
    SpriteNode.__init__(self, 'plf:Item_CoinGold', **kwargs)

class Meteor (SpriteNode):
  def __init__(self, **kwargs):
    img = random.choice(
      ['spc:MeteorBrownBig1', 'spc:MeteorBrownBig2'])
    SpriteNode.__init__(self, img, **kwargs)
    self.destroyed = False


class Player(SpriteNode):
  """
  Refactored player into its own class with motion stuff.

  by Ed Suominen (edsuom.com). No copyright claimed to changes
  from Tutorial Part 7.py, included with Pythonista and upon
  which this adaptation is based.
  """
  dt = 1.0/60
  accel= 7000
  drag = 0.03
  bounce = 0.6
  # Realistic acceleration with drag eliminates need for
  # speed limit
  #max_speed = 40

  def __init__(self, groundWidth):
    self.groundWidth = groundWidth
    SpriteNode.__init__(self, standing_texture)

  def center(self):
    """
    Centers the player, standing still.
    """
    self.v = 0
    self.position = (self.groundWidth/2, 32)
    self.texture = standing_texture

  def motion(self, gx):
    """
    Given the accelerometer's x-axis reading, updates player's
    velocity and returns change in position.
    """
    self.v = (1-self.drag) * \
            (self.v + self.accel * gx * self.dt)
    return self.v * self.dt

  def reverseMotion(self):
    """
    Reverses velocity with some energy lost.
    """
    self.v = -self.bounce * self.v

  def move(self, gx):
    """
    Given accelerometer input, moves the player in a realistic
    manner. Bounces, acceleration, and drag.
    """
    dx = self.motion(gx)
    x = self.position.x + dx
    hwPlayer = 0.5 * self.size[0]
    if x < hwPlayer:
      self.reverseMotion()
      x = hwPlayer + 1
    elif x > self.groundWidth - hwPlayer:
      self.reverseMotion()
      x = self.groundWidth - hwPlayer - 1
    self.position = x, 32


class Game (Scene):
  def setup(self):
    self.background_color = '#004f82'
    self.ground = Node(parent=self)
    x = 0
    while x <= self.size.w + 64:
      tile = SpriteNode(
        'plf:Ground_PlanetHalf_mid', position=(x, 0))
      self.ground.add_child(tile)
      x += 64
    self.player = Player(self.size.w)
    self.player.anchor_point = (0.5, 0)
    self.add_child(self.player)
    score_font = ('Futura', 40)
    self.score_label = LabelNode(
      '0', score_font, parent=self)
    self.score_label.position = (
      self.size.w/2, self.size.h - 70)
    self.score_label.z_position = 1
    self.items = []
    self.lasers = []
    self.new_game()

  def new_game(self):
    for item in self.items:
      item.remove_from_parent()
    self.items = []
    self.lasers = []
    self.score = 0
    self.score_label.text = '0'
    self.walk_step = -1
    self.player.center()
    self.speed = 1.0
    self.game_over = False

  def update(self):
    if self.game_over:
      return
    self.update_player()
    self.check_item_collisions()
    self.check_laser_collisions()
    if random.random() < 0.05 * self.speed:
      self.spawn_item()

  def touch_began(self, touch):
    self.shoot_laser()

  def update_player(self):
    """
    This is where the player moves
    """
    g = gravity()
    if abs(g.x) < 0.02:
      # Realistic motion allows tighter
      # threshold for disregarding
      # accelerometer input
      self.player.texture = standing_texture
      self.walk_step = -1
      return
    self.player.x_scale = cmp(g.x, 0)
    self.player.move(g.x)
    step = int(
            self.player.position.x / 40) % 2
    if step != self.walk_step:
      self.player.texture = walk_textures[step]
      sound.play_effect(
        'rpg:Footstep00', 0.05, 1.0 + 0.5 * step)
      self.walk_step = step

  def check_item_collisions(self):
    player_hitbox = Rect(
      self.player.position.x - 20, 32, 40, 65)
    for item in list(self.items):
      if item.frame.intersects(player_hitbox):
        if isinstance(item, Coin):
          self.collect_item(item)
        elif isinstance(item, Meteor):
          if item.destroyed:
            self.collect_item(item, 100)
          else:
            self.player_hit()
      elif not item.parent:
        self.items.remove(item)

  def check_laser_collisions(self):
    for laser in list(self.lasers):
      if not laser.parent:
        self.lasers.remove(laser)
        continue
      for item in self.items:
        if not isinstance(item, Meteor):
          continue
        if item.destroyed:
          continue
        if laser.position in item.frame:
          self.destroy_meteor(item)
          self.lasers.remove(laser)
          laser.remove_from_parent()
          break

  def destroy_meteor(self, meteor):
    sound.play_effect('arcade:Explosion_2', 0.2)
    meteor.destroyed = True
    meteor.texture = Texture('plf:Item_Star')
    for i in range(5):
      m = SpriteNode('spc:MeteorBrownMed1', parent=self)
      m.position = meteor.position + (
        random.uniform(-20, 20), random.uniform(-20, 20))
      angle = random.uniform(0, pi*2)
      dx, dy = cos(angle) * 80, sin(angle) * 80
      m.run_action(A.move_by(dx, dy, 0.6, TIMING_EASE_OUT))
      m.run_action(A.sequence(A.scale_to(0, 0.6), A.remove()))

  def player_hit(self):
    self.game_over = True
    sound.play_effect('arcade:Explosion_1')
    self.player.texture = hit_texture
    self.player.run_action(
      A.move_by(0, -150))
    self.run_action(
      A.sequence(A.wait(2*self.speed), A.call(self.new_game)))

  def spawn_item(self):
    if random.random() < 0.2 * self.speed:
      # Reduced meteor probability from 0.3
      # to allow more player motion
      meteor = Meteor(parent=self)
      meteor.position = (
        random.uniform(20, self.size.w-20), self.size.h + 30)
      d = random.uniform(2.0, 4.0)
      actions = [
        A.move_to(random.uniform(0, self.size.w), -100, d),
        A.remove()]
      meteor.run_action(A.sequence(actions))
      self.items.append(meteor)
    else:
      coin = Coin(parent=self)
      coin.position = (
        random.uniform(20, self.size.w-20), self.size.h + 30)
      d = random.uniform(2.0, 4.0)
      actions = [
        A.move_by(0, -(self.size.h + 60), d),
        A.remove()]
      coin.run_action(A.sequence(actions))
      self.items.append(coin)
    self.speed = min(3, self.speed + 0.005)

  def collect_item(self, item, value=10):
    if value > 10:
      sound.play_effect('digital:PowerUp8')
    else:
      sound.play_effect('digital:PowerUp7')
    item.remove_from_parent()
    self.items.remove(item)
    self.score += value
    self.score_label.text = str(self.score)

  def shoot_laser(self):
    if len(self.lasers) >= 3:
      return
    laser = SpriteNode('spc:LaserGreen12', parent=self)
    laser.position = self.player.position + (0, 30)
    laser.z_position = -1
    actions = [
      A.move_by(0, self.size.h, 1.2 * self.speed),
      A.remove()]
    laser.run_action(A.sequence(actions))
    self.lasers.append(laser)
    sound.play_effect('digital:Laser4')

if __name__ == '__main__':
  run(Game(), PORTRAIT, show_fps=True)
# --------------------
