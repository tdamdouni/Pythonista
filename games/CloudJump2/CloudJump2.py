from __future__ import print_function
import cStringIO, console, Image, ImageDraw, math, numpy, os, os.path
import pickle, random, requests, sound, threading, time, zipfile
from scene import *
import ui

DEAD_ZONE =  0.02
DIFFICULTY_Q = 100000.0
ENEMY_DENSITY = 0.2
game_character = 'Boy'
GAME_FONT = 'AppleSDGothicNeo-Bold' # easier to change font later
GAME_GRAVITY = 2000
GAME_WAITING, GAME_PLAYING, GAME_DEAD = range(3)
IMAGE_WIDTH = 100
MAX_CLOUD_DIST = 505
PLAYER_BOUNCE_VELOCITY = 1700
PLAYER_CONTROL_SPEED = 2000
PLAYER_INITIAL_BOUNCE = 1700
SCRIPT_NAME  = os.path.basename(__file__)[:-3]
RESOURCE_DIR = __file__[:-3] + '_resources/'
USER_FILE = RESOURCE_DIR + 'user.txt'

try:
    os.mkdir(RESOURCE_DIR)
except OSError:
    pass

player_name = None
urls = [ 'http://powstudios.com/system/files/smokes.zip',
         'https://dl.dropboxusercontent.com/u/25234596/Exp_type_C.png' ]

# === imported from HighScores.py ===

class HighScores(object):
    def __init__(self, in_file_name = SCRIPT_NAME + ' high scores'):
        file_ext = '.pkl'
        self.file_name = RESOURCE_DIR + in_file_name
        if not self.file_name.endswith(file_ext):
            self.file_name += file_ext
        self.high_scores = self.__load_scores()

    def __load_scores(self):  # private function
        try:
            with open(self.file_name, 'r') as in_file:
                return pickle.load(in_file)
        except IOError:
            return {}

    def __save_scores(self):  # private function
        with open(self.file_name, 'w') as out_file:
            pickle.dump(self.high_scores, out_file)

    def is_high_score(self, name, score):
        try:
            curr_high_score = self.high_scores.get(name, score-1)
        except TypeError:
            raise TypeError('The score arguement must be a number.')
        is_new_high_score = score > curr_high_score
        if is_new_high_score:
            self.high_scores[name] = score
            self.__save_scores()
        return is_new_high_score

# === end import from HighScores.py ===

def get_remote_resources(in_urls = urls):
    def url_to_local_file(in_url, in_file_name):
        short_name = in_file_name.rpartition('/')[2] or in_file_name
        console.show_activity('Downloading: ' + short_name)
        time.sleep(1)
        with open(in_file_name, 'w') as out_file:
            out_file.write(requests.get(in_url).content)
        console.hide_activity()

    for url in in_urls:
        file_name = RESOURCE_DIR + (url.rpartition('/')[2] or url)
        if not os.path.isfile(file_name):
            url_to_local_file(url, file_name)

def get_username(file_name = USER_FILE):
    player_name = None
    if os.path.isfile(file_name):
        with open(file_name) as f:
            for line in f.readlines():
                if line.istitle():
                    player_name = line
    if not player_name:
        player_name = console.input_alert('What is your name? ').title()
        if player_name:
            with open(file_name, 'w') as f:  
                f.write(player_name)
    return player_name or 'default'

def slice_image_into_tiles(in_image, img_count_h, img_count_v = 1):
    w, h = in_image.size  # get the size of the big image
    w /= img_count_h      # calculate the size of smaller images
    h /= img_count_v
    return [load_pil_image(in_image.crop((x*w, y*h, (x+1)*w, (y+1)*h)))
                for y in xrange(img_count_v) for x in xrange(img_count_h)]

def get_images_from_zip_file(file_name, directory, starts_with):
        with open(file_name) as in_file:
            starts_with = directory + '/' + starts_with
            zip_file = zipfile.ZipFile(in_file)
            return [load_pil_image(Image.open(cStringIO.StringIO(zip_file.open(name).read())))
                    for name in zip_file.namelist() if name.startswith(starts_with)]

def player_killed_sounds():
    for i in xrange(4):
        sound.play_effect('Hit_{}'.format(i+1))
        time.sleep(0.5)

def high_score_sounds():
    for i in xrange(4):
        sound.play_effect('Jump_{}'.format(i+1))
        time.sleep(0.3)

def run_in_thread(in_function):
    threading.Thread(None, in_function).start()

def tinted_text(s, x, y, tint_color = Color(0, 0, 1)):
    tint(0, 0, 0)
    text(s, GAME_FONT, 48, x + 2, y - 2)
    tint(*tint_color)
    text(s, GAME_FONT, 48, x, y)

def shadow_text(s, x, y):
    tinted_text(s, x, y, Color(0.0, 0.5, 1.0))

def score_text(s, x, y):
    tinted_text(s, x, y, Color(1.0, 1.0, 0.4))

def pil_rect_to_scene_rect(pil_rect = (1, 2, 3 ,4)):
    if pil_rect:
        l, t, r, b = pil_rect
        return Rect(l, t, r-l, b-t)
    else:
        return Rect()

class Sprite(Layer):
    def __init__(self, rect = Rect(), parent = None, image_name = 'Boy'):
        super(Sprite, self).__init__(rect)
        if parent:
            parent.add_layer(self)
        self.image = image_name
        self.velocity = Point(0, 0)

    def update(self, dt):  # make the clouds blow in the wind?
        super(Sprite, self).update(dt)
        self.frame.x += dt * self.velocity.x
        self.frame.y += dt * self.velocity.y

class AnimatedSprite(Sprite):
    def __init__(self, rect, parent, in_images, in_frames_per_image, **kwargs):
        super(self.__class__, self).__init__(rect, parent, in_images[0])
        assert in_images and isinstance(in_images, list)
        self.images = in_images
        self.frames_per_image = in_frames_per_image
        self.max_frames = len(in_images) * in_frames_per_image
        self.frame_count = 0
        self.looped = False
        self.is_done = True
        self.configure(**kwargs)

    def configure(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def update(self, dt):
        super(AnimatedSprite, self).update(dt)
        if self.is_done:
            self.image = None 
            return
        self.image = self.images[int(self.frame_count / self.frames_per_image)]
        self.frame_count += 1
        if self.frame_count >= self.max_frames:
            if self.looped:
                self.frame_count %= self.max_frames
            else:
                self.is_done = True

class Player(Sprite):
    def __init__(self, rect = Rect(), parent = None):
        super(self.__class__, self).__init__(rect, parent, game_character)

    def death_completion(self):
        self.superlayer.remove_layer(self)
        self.superlayer = None

    def die(self):
        self.frame.y = max(self.frame.y, 50)
        run_in_thread(player_killed_sounds)
        self.animate('scale_x', 0.01)
        self.animate('scale_y', 0.01, completion=self.death_completion)
        #del self  # suicide is not an tenable option

class GrassBlock(Sprite):
    def __init__(self, rect = Rect(), parent = None):
        super(self.__class__, self).__init__(rect, parent, 'PC_Grass_Block')

class Enemy(Sprite):
    def __init__(self, rect = Rect(), parent = None):
        super(self.__class__, self).__init__(rect, parent, 'Alien_Monster')
        self.tint = Color(1, 0, 1)

class Cloud(Sprite):
    def __init__(self, rect = Rect(), parent = None):
        cloud_image = self.cloud_maker()
        new_rect = pil_rect_to_scene_rect(cloud_image.getbbox())
        rect.w, rect.h = new_rect.w, new_rect.h
        super(self.__class__, self).__init__(rect, parent, load_pil_image(cloud_image))
        self.velocity.x = random.randint(-1, 4)  # give clouds a 2-in-6 chance to be moving
        if self.velocity.x > 1:
            self.velocity.x = 0
        self.velocity.x *= 50

    @classmethod
    def generate_shapes(cls, num_circles):
        shapes = []
        for i in xrange(num_circles):
            x = (i * 20 - ((num_circles/2)*30))+90
            y = ((random.random()-0.5) * 30)+15
            rad = random.randint(50, 100)
            shapes.append([x, y, rad])
        return shapes

    @classmethod
    def draw_cloud(cls, draw):
        num_circles = random.randint(5, 6)
        circles = cls.generate_shapes(num_circles)
        for i in circles:
            r = i[2]
            bbox = (i[0], 40-i[1], i[0]+r, 40-i[1]+r)
            draw.ellipse(bbox, fill='rgb(90%,90%,90%)')
        for i in circles:
            r = i[2]
            bbox = (i[0], 40-i[1]-10, i[0]+r, 40-i[1]+r-10)
            draw.ellipse(bbox, fill='white')

    # found on 'http://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil'
    @classmethod
    def crop_image(cls, img):
        image_data = numpy.asarray(img)
        image_data_bw = image_data.max(axis=2)
        non_empty_columns = numpy.where(image_data_bw.max(axis=0)>0)[0]
        non_empty_rows    = numpy.where(image_data_bw.max(axis=1)>0)[0]
        crop_box = (min(non_empty_rows),    max(non_empty_rows),
                    min(non_empty_columns), max(non_empty_columns))
        image_data_new = image_data[crop_box[0]:crop_box[1]+1,
                                    crop_box[2]:crop_box[3]+1, :]
        img = Image.fromarray(image_data_new)
        return img

    @classmethod
    def cloud_maker(cls):
        image_size = (220, 140)
        img = Image.new('RGBA', image_size)
        draw = ImageDraw.Draw(img)
        cls.draw_cloud(draw)
        del draw
        return cls.crop_image(img)

class MyScene(Scene):
    def __init__(self):
        run(self)

    def create_ground(self, max_blocks = 12):
        block_size_w = self.bounds.w / max_blocks
        block_size_h = block_size_w * 171 / 101  # image is 101 x 171 pixels
        for i in xrange(max_blocks):
            rect = Rect(i * block_size_w, 0, block_size_w, block_size_h)
            GrassBlock(rect, self)
        return block_size_h * 0.7  # the new ground level

    def generate_clouds(self):
        y = self.cloud_height
        while self.cloud_height < self.bounds.h * 2:
            q = min(self.climb, DIFFICULTY_Q)
            min_dist = int(MAX_CLOUD_DIST * q / DIFFICULTY_Q)
            max_dist = int(MAX_CLOUD_DIST / 2 + min_dist / 2)
            self.cloud_height += random.randint(min_dist, max_dist)
            rect = Rect(random.random() * (self.bounds.w - 150),
                              self.cloud_height, 0, 0)
            cloud = Cloud(rect, self)
            if random.random() < ENEMY_DENSITY:
                #generate new enemy
                rect = Rect(0, 0, 64, 64)
                rect.center(cloud.frame.center())
                rect.y = cloud.frame.top() - 15
                enemy = Enemy(rect, self)
                enemy.velocity = cloud.velocity

    def cull_scenery(self):
        for sublayer in self.root_layer.sublayers:
            if sublayer.frame.top() < 0:
                sublayer.superlayer.remove_layer(sublayer)
                del sublayer

    def control_player(self):
        tilt = gravity().x
        if abs(tilt) > DEAD_ZONE:
            move = self.dt * tilt * PLAYER_CONTROL_SPEED
            self.player.frame.x += move
            self.player.frame.x = max(self.player.frame.x, 0)
            self.player.frame.x = min(self.player.frame.x,
                                      self.bounds.w - self.player.frame.w)

    def lower_scenery(self, y):
        self.climb += y
        self.cloud_height -= y
        for sublayer in self.root_layer.sublayers:
            if sublayer not in (self.player, self.smoke_normal, self.smoke_special):
                sublayer.frame.y -= y

    def end_game(self):
        self.game_state = GAME_DEAD
        self.player.velocity = Point(0, 0)
        death_loc = self.player.frame.center()
        death_loc.y = max(death_loc.y, 80)
        self.player.die()
        del self.player
        self.player = None
        score = int(self.climb / 10)
        if self.high_scores.is_high_score(player_name, score):
            self.smoke_special.frame.center(death_loc)
            self.smoke_special.configure(frame_count=0, is_done=False)
            #console.hud_alert('New high score!') # for debugging purposes
            run_in_thread(high_score_sounds)
            fmt = 'Congratulations {}:\nYou have a new high score!'
            self.high_score_msg = fmt.format(player_name)
        else:
            self.smoke_normal.frame.center(death_loc)
            self.smoke_normal.configure(frame_count=0, is_done=False)

    def run_gravity(self):
        player_y_move = self.dt * self.player.velocity.y
        scenery_y_move = 0
        old_velocity_y = self.player.velocity.y
        self.player.velocity.y -= self.dt * GAME_GRAVITY
        if old_velocity_y > 0 and self.player.velocity.y <= 0:
            self.player_apex_frame = True
        if self.player.frame.y >= self.player_max_y :
            scenery_y_move = self.player.frame.y - self.player_max_y
            self.player.frame.y = self.player_max_y
            self.lower_scenery(scenery_y_move)
        elif self.player.frame.center().y < 0:
            self.player.frame.y = 0
            sound.play_effect('Crashing')
            self.end_game()

    def collision_detect(self):
        bounce = False
        if self.player.velocity.y < 0:
            p = self.player.frame.center()
            for sublayer in self.root_layer.sublayers:
                if self.player.frame.center() in sublayer.frame:
                    if isinstance(sublayer, Enemy):
                        sound.play_effect('Powerup_1')
                        self.end_game()
                        return  # player killed by collision
                    elif isinstance(sublayer, Cloud):
                        bounce = True
        if bounce:
            self.player.velocity.y = PLAYER_BOUNCE_VELOCITY
            sound.play_effect('Boing_1')

    def game_loop(self):
        if self.game_state == GAME_PLAYING:
            self.run_gravity()
            if not self.player:
                return  # player killed by gravity
            self.collision_detect()
            if not self.player:
                return  # player killed by collision
            self.control_player()
            if self.player_apex_frame:
                self.cull_scenery()
                self.generate_clouds()
                self.player_apex_frame = False

    def draw_text(self):
        x = self.bounds.center().x
        score = int(self.climb / 10)
        score_as_text = 'Score: {}'.format(score)
        if self.game_state == GAME_PLAYING:
            shadow_text(score_as_text, x, self.bounds.h * 0.95)
        elif self.game_state == GAME_DEAD:
            shadow_text(score_as_text, x, self.bounds.h * 0.95)
            if self.high_score_msg:
                score_text(self.high_score_msg, x, self.bounds.h * 0.78)
            shadow_text('Game Over', x, self.bounds.h * 0.6)
            shadow_text('Tap to Play Again', x, self.bounds.h * 0.4)
        elif self.game_state == GAME_WAITING:
            shadow_text('Tap Screen to Start',  x, self.bounds.h * 0.6)
            shadow_text('Tilt Screen to Steer', x, self.bounds.h * 0.4)

    def setup_smoke(self):
        rect = Rect(0, 0, 200, 200)
        file_name = RESOURCE_DIR + 'smokes.zip'
        images = get_images_from_zip_file(file_name, 'smoke puff up', 'smoke_puff')
        self.smoke_normal = AnimatedSprite(rect, self, images, 8)

        rect = Rect(0, 0, 200, 200)
        file_name = RESOURCE_DIR + 'Exp_type_C.png'
        images = slice_image_into_tiles(Image.open(file_name), 48)
        self.smoke_special = AnimatedSprite(rect, self, images, 2)

    def setup(self):
        self.climb = 0
        self.cloud_height = 200
        self.game_state = GAME_WAITING
        self.high_scores = HighScores()
        self.high_score_msg = None
        ground_level = self.create_ground(12)
        self.generate_clouds()
        
        rect = Rect(0, 0, IMAGE_WIDTH, IMAGE_WIDTH)
        rect.center(self.bounds.center())
        rect.y = ground_level
        self.player = Player(rect, self)
        self.player_apex_frame = False
        self.player_max_y = self.bounds.h * 0.6
        self.setup_smoke()

    def draw(self):
        self.game_loop()
        background(0.40, 0.80, 1.00)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        self.draw_text()

    def touch_began(self, touch):
        if self.game_state == GAME_WAITING:
            self.game_state = GAME_PLAYING
            self.player.velocity.y = PLAYER_INITIAL_BOUNCE
        elif self.game_state == GAME_DEAD:
            self.setup()

characters = 'Boy Girl Guardsman Person_Blond Woman Man Hamster_Face Mouse_Face Bear_Face Cat_Face Cow_Face Dog_Face'.split()
high_scores = {n:(i+1)*1000 for i, n in enumerate('Al Bob Carl David Elliot Freddie Godzilla'.split())}

class SelectACharacterView(ui.View):
    def __init__(self):
        self.background_color = (0.40, 0.80, 1.00)
        self.add_subview(self.make_header())
        half = len(characters) / 2
        for i, character in enumerate(characters):
            x = 62 + i % half * 155
            y = 160 if i < half else 365
            self.add_subview(self.make_button(x, y, character))

    @classmethod
    def make_header(cls):
        header = ui.Label(frame = (200, 19.5, 700, 116.5))
        header.text_color = 'white'
        header.text = 'Select A Character'
        header.font = ('AvenirNext-Heavy', 70)
        return header

    @classmethod
    def character_tapped(cls, sender):
        print('The user wants to be: ' + sender.name)
        game_character == sender.name
        print(game_character)

    @classmethod
    def make_button(cls, x, y, image_name = 'Boy'):
        img = ui.Image.named(image_name).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
        button = ui.Button(name=image_name, frame=(x, y, 160, 128, 128), image=img)
        button.action=cls.character_tapped
        return button

class Data (ui.ListDataSource):
    def __init__(self, items=None):
        ui.ListDataSource.__init__(self, items)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = str(self.items[row])
        cell.text_label.alignment = ui.ALIGN_CENTER
        return cell

class HighScoreView(ui.View):
    def __init__(self, high_scores=high_scores):
        self.name = 'Cloud Jump 2 - Leaderboard'
        self.frame=(0, 0, 500, 500)
        tv = ui.TableView()
        tv.frame=(0, 0, 500, 500)
        tv.data_source = Data(items=self.scores_list(high_scores))
        tv.allows_selection = tv.data_source.delete_enabled = False 
        self.add_subview(tv)

    @classmethod
    def scores_list(cls, high_scores):
        scores_sorted = sorted(zip(high_scores.values(),
                                   high_scores.keys()), reverse=True)
        return ['{:7>}  |  {}'.format(s, n) for s, n in scores_sorted]

class UserNameView(ui.View):
    def __init__(self, default_user_name='Name'):
        self.name = 'Enter your username:'
        self.background_color = 0.40, 0.80, 1.00
        self.frame=(0, 0, 500, 500)
        self.label = ui.Label(frame=(12, 100, 2000, 55))
        self.label.text = 'What is your name?'
        self.label.text_color = 'black'
        self.label.font = ('Avenir-Black', 55)
        self.add_subview(self.label)
        self.text_field = ui.TextField(frame=(155, 175, 200, 32))
        self.text_field.text = default_user_name
        self.text_field.text_color = 'grey'
        self.text_field.clear_button_mode = 'while_editing'
        self.add_subview(self.text_field)
        button = ui.Button(background_color='white',
                   frame=(360, 175, 75, 36),
                   image=ui.Image.named('ionicons-arrow-right-a-32'))
        self.add_subview(button)

def change_character(sender):
	SelectACharacterView().present(style='full_screen', hide_title_bar=True)
	
def change_name(sender):
	UserNameView().present(style='sheet', hide_title_bar=True)

def show_leaderboard(sender):
	HighScoreView().present('sheet')

def play_game(sender):
	root_view.add_subview(scene_view)
	
get_remote_resources()
player_name = get_username()

root_view = ui.load_view('ui-menu')
root_view.background_color = (0.40, 0.80, 1.00)
root_view.present(orientations=['landscape'], hide_title_bar=True)
scene_view = SceneView(frame=root_view.frame)
scene_view.flex = 'WH'
scene_view.scene = MyScene()
