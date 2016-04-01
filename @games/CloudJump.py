from scene import *
import random

IMAGE_WIDTH = 101
IMAGE_HEIGHT = 171
IMAGE_Y_OFFSET = -30
BLOCK_HEIGHT = 40
BLOCK_DEPTH = 80
DEAD_ZONE_MIN = -0.02
DEAD_ZONE_MAX =  0.02
PLAYER_CONTROL_SPEED = 2000
PLAYER_BOUNCE_VELOCITY = 1700
PLAYER_INITIAL_BOUNCE = 1700
MAX_CLOUD_DIST = 500
DIFFICULTY_Q = 100000.0
GAME_GRAVITY = 2000
GAME_WAITING = 0
GAME_PLAYING = 1
GAME_DEAD = 2

class Player(object):
    def __init__(self):
        self.bounds = Rect()
        self.velocity = 0

    def draw(self):
        tint(1,1,1)
        image('PC_Character_Pink_Girl', self.bounds.x, self.bounds.y + IMAGE_Y_OFFSET)

class GroundBlock(object):
    def __init__(self):
        self.bounds = Rect()

    def draw(self):
        tint(1,1,1)
        image('PC_Grass_Block', self.bounds.x, self.bounds.y)

class Cloud (object):
    def __init__(self):
        self.shapes = []

        num_circles = random.randint(4, 5)
        for i in xrange(num_circles):
            x = i * 20 - ((num_circles/2)*30)
            y = (random.random()-0.5) * 30
            rad = random.randint(50, 100)
            self.shapes.append([x, y, rad])

        self.width = num_circles * 30 + 30
        self.bounds = Rect(0, 0, self.width, 60)

    def is_colliding(self, pos):
        startp = self.bounds.x - self.width/2
        endp = self.bounds.x + self.width/2
        if ((pos.x < endp) and (pos.x > startp) and
            (pos.y < (self.bounds.y + 30)) and
            (pos.y > (self.bounds.y + 10))):
                return True 
        return False

    def draw(self):
        push_matrix()
        translate(self.bounds.x, self.bounds.y)
        no_stroke()
        fill(0.90, 0.90, 0.90)
        for i in self.shapes:
            ellipse(i[0], i[1] - 5, i[2], i[2])

        fill(1.00, 1.00, 1.00)
        for i in self.shapes:
            ellipse(i[0], i[1] + 5, i[2], i[2])

        pop_matrix()

class MyScene (Scene):

    def create_ground(self):
        for x in range((int(self.bounds.w) / IMAGE_WIDTH) + 1):
            block = GroundBlock()
            block.bounds = Rect(x * IMAGE_WIDTH, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
            self.scenery.append(block)

    def generate_clouds(self):
        y = self.cloud_height
        while self.cloud_height < self.bounds.h * 2:
            q = min(self.climb, DIFFICULTY_Q)
            min_dist = int(MAX_CLOUD_DIST * q / DIFFICULTY_Q)
            max_dist = int(MAX_CLOUD_DIST / 2 + min_dist / 2)
            self.cloud_height += random.randint(min_dist, max_dist)
            cloud = Cloud()
            cloud.bounds.x = random.random() * (self.bounds.w - 150)
            cloud.bounds.y = self.cloud_height
            self.scenery.append(cloud)

    def cull_scenery(self):
        i = len(self.scenery)
        for sprite in self.scenery[:]:
            if sprite.bounds.top() < 0:
                self.scenery.remove(sprite)         

    def control_player(self):
        tilt = gravity().x
        if(tilt < DEAD_ZONE_MIN) or (tilt > DEAD_ZONE_MAX):
            move = self.dt * tilt * PLAYER_CONTROL_SPEED
            self.player.bounds.x += move
            if(self.player.bounds.x < 0):
                self.player.bounds.x = 0
            elif(self.player.bounds.x > self.bounds.w - self.player.bounds.w):
                self.player.bounds.x = self.bounds.w - self.player.bounds.w

    def lower_scenery(self, y):
        self.climb += y
        self.cloud_height -= y
        for sprite in self.scenery:
            sprite.bounds.y -= y

    def run_gravity(self):
        player_y_move = self.dt * self.player.velocity
        scenery_y_move = 0
        old_velocity = self.player.velocity
        self.player.velocity -= self.dt * GAME_GRAVITY
        if(old_velocity > 0) and (self.player.velocity <= 0):
            self.player_apex_frame = True
        self.player.bounds.y += player_y_move
        if(self.player.bounds.y >= self.player_max_y):
            scenery_y_move = self.player.bounds.y - self.player_max_y
            self.player.bounds.y = self.player_max_y
            self.lower_scenery(scenery_y_move)
        elif(self.player.bounds.top() < 0):
            self.game_state = GAME_DEAD

    def collision_detect(self):
        bounce = False
        if(self.player.velocity < 0):
            p = Point(self.player.bounds.x + self.player.bounds.w/2, self.player.bounds.y)
            for sprite in self.scenery:
                if hasattr(sprite, 'is_colliding'):
                    collision = sprite.is_colliding(p)
                else:
                    collision = p in sprite.bounds
                if collision:
                    self.player.velocity = PLAYER_BOUNCE_VELOCITY
                    break 

    def game_loop(self):
        if self.game_state == GAME_PLAYING:
            self.run_gravity()
            self.collision_detect()
            self.control_player()
            if self.player_apex_frame:
                self.cull_scenery()
                self.generate_clouds()
                self.player_apex_frame = False

    def shadow_text(self, s, x, y):
        tint(0,0,0)
        text(s, 'AvenirNext-Heavy', 48, x + 2, y - 2)
        tint(0.00, 0.50, 1.00)
        text(s, 'AvenirNext-Heavy', 48, x, y)

    def draw_text(self):
        if(self.game_state == GAME_WAITING):
            if(int(self.t) % 2):
                self.shadow_text('Tap Screen to Start', self.bounds.w / 2, self.bounds.h * 0.6)
                self.shadow_text('Tilt Screen to Steer', self.bounds.w / 2, self.bounds.h * 0.4)
        elif(self.game_state == GAME_PLAYING):
            self.shadow_text('Score : ' + str(int(self.climb / 10)), self.bounds.w / 2, self.bounds.h * 0.95)
        if(self.game_state == GAME_DEAD):
            self.shadow_text('Score : ' + str(int(self.climb / 10)), self.bounds.w / 2, self.bounds.h * 0.95)
            self.shadow_text('Game Over', self.bounds.w / 2, self.bounds.h / 2)


    def setup(self):
        self.game_state = GAME_WAITING
        self.scenery = []
        self.climb = 0
        self.create_ground()
        self.cloud_height = 200
        self.generate_clouds()
        self.player = Player()
        self.player_apex_frame = False
        self.player.bounds = Rect(self.bounds.w / 2 - IMAGE_WIDTH / 2, BLOCK_HEIGHT + BLOCK_DEPTH / 2, IMAGE_WIDTH, IMAGE_HEIGHT)
        self.player_max_y = self.bounds.h * 0.6

    def draw(self):
        self.game_loop()
        background(0.40, 0.80, 1.00)
        for sprite in self.scenery:
            sprite.draw()
        self.player.draw()
        self.draw_text()

    def touch_began(self, touch):
        if self.game_state == GAME_WAITING:
            self.game_state = GAME_PLAYING
            self.player.velocity = PLAYER_INITIAL_BOUNCE
        elif self.game_state == GAME_DEAD:
            self.setup()

run(MyScene(), PORTRAIT)
