# https://forum.omz-software.com/topic/3170/action-repeat-won-t-repeat/6

#up = A.move_to(self.size.w/2, 350, 9, TIMING_EASE_BACK_OUT)
#d = 2.0 # duration
# Inline function for the call action:
#def move_random():
#  x, y = random.randrange(100,924), random.randrange(300,700)
  #self.boss.run_action(A.move_to(x, y, d))
# The call action doesn't wait until the move action finishes, so add a wait action for that:
#repmo = A.repeat(A.sequence(A.call(move_random), A.wait(d)), -1))
#phase_1 = A.sequence(stationary, up)
#mo = A.move_to(, 2, TIMING_EASE_BACK_IN_OUT)
#self.boss.run_action(A.sequence(phase_1, repmo))
# --------------------
#repmo = A.repeat(A.sequence(A.call(move_random), A.wait(d)), -1))

# --------------------

# coding: utf-8

from scene import *
import sound
import random

# one full turn = 6.823
A = Action

big_up = Texture('Big rise.PNG')
big_boss_s = Texture('Big Boss.PNG')
big_boss_b = Texture('BIG BOSS.PNG')
boss_left = Texture('left.PNG')
boss_right = Texture('right.PNG')
boss_off = Texture('floating.PNG')
boss_standing = Texture('standing.PNG')
boss_up = Texture('rising.PNG')
boss_texture = Texture('Boss.PNG')
background = Texture('Background.JPG')
standing_texture = Texture('Standing.PNG')
walk_textures = [Texture('Running1.PNG'),Texture('Running2.PNG')]
hit = Texture('IMG_3808.PNG')

class Game (Scene):
    
    def setup(self):    
    
        self.background_color = '#2e2e2e'
        self.bg = SpriteNode('IMG_3929.JPG')
        self.bg.position = (self.size.w / 2, 385)
        self.add_child(self.bg)
        ground = Node(parent=self)
        x = 0
        while x <= self.size.w + 64:
            tile = SpriteNode('plf:Ground_SandCenter', position=(x, 0))
            ground.add_child(tile)
            x += 64         
        self.player = SpriteNode('Standing.PNG')
        self.player.anchor_point = (0.5, 0)
        self.player.position = (200, 32)
        self.add_child(self.player)
        self.walk_step = -1     
        self.items = []
        self.boss_ai()
        
        
    def update(self):           
        self.collisions()
        self.boss_animation()
        self.update_player()
        if random.random() < 0.05 and self.t > 7:
            self.attack()
        
        
    def update_player(self):
        g = gravity()
        if abs(g.y) > 0.05:
            self.player.x_scale = cmp(g.y, 0)
            x = self.player.position.x
            max_speed = 25
            x = max(0, min(self.size.w, x + g.y * max_speed))
            self.player.position = x, 32
            step = int(self.player.position.x / 40) % 2
            if step != self.walk_step:
                self.player.texture = walk_textures[step]
                sound.play_effect('rpg:Footstep09', 0.05, 1.0 + 0.5 * step)
                self.walk_step = step
        else:
            self.player.texture = standing_texture
            self.walk_step = -1     
            
    def collisions(self):
        self.player_hitbox = Rect(self.player.position.x - 20, 32, 40, 65)
        for item in list(self.items):
            if item.frame.intersects(self.player_hitbox):
                self.player_hit()
                
                
    def move_random():
        x, y = random.randrange(100,924), random.randrange(300,700)
        self.boss.run_action(A.move_to(x, y, d))
        
                
    def player_hit(self):
        pass
        
    
    def boss_ai(self):
        self.boss = SpriteNode('standing.PNG')
        self.boss.anchor_point = (0.5, 0.3)
        self.boss.position = (self.size.w/2, 90)
        self.boss.speed = 2
        self.add_child(self.boss)
        self.attack()
                
                
    def boss_animation(self):
        if self.t > 0.25:
            self.boss.texture = boss_up
        if self.t > 3:
            self.boss.texture = boss_off
        if self.t > 4:
            self.boss.texture = boss_texture

            
    def attack(self):
        self.sh = SpriteNode('sharooken.PNG')
        sp = 1
        self.sh.position = (self.boss.position)
        self.add_child(self.sh)
        rot = A.repeat(A.rotate_by(6.823, 0.5), -1)
        actions = [A.move_by(random.randrange(-300,300), -(self.size.h + 60), sp), A.remove()]
        self.sh.run_action(A.group(rot, A.sequence(actions)))
        self.items.append(self.sh)
                        

    
        
        
        
        
if __name__ == '__main__':
    run(Game(), LANDSCAPE, show_fps=False)

# --------------------
