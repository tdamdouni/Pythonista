# https://forum.omz-software.com/topic/3710/how-to-spritesheet-subtexture/7

from scene import *
x,y,xs,ys = 0,0,1,1

# Above sets up the initial subtexture(Rect(x,y,xs,ys)) on line 25 to show the full image until touch_began and touch_ended changes the coordinates of the subtexture to show whatever section you set in touch began.

class MyScene (Scene):
    def setup(self):
        self.background_color = 'black'
        
        self.texture_name = SpriteNode(Texture('test:Mandrill'),
        scale = 2, 
        position = self.size / 2,
        parent = self)
        
    def touch_began(self, touch):
        global x,y,xs,ys #These variables must be referenced as global or they will not be recognized.
        
        x,y,xs,ys = 0,0,.5,1 #This changes the coordinates for update() on line 25 to show a portion of the texture.
    
    def touch_ended(self, touch):
        global x,y,xs,ys #These variables must be referenced as global or they will not be recognized.
        
        x,y,xs,ys = 0,0,1,1 #This changes the coordinates back to show the full image when you stop touching the screen.
        
    def update(self):
        self.texture_name.texture = Texture('test:Mandrill').subtexture(Rect(x,y,xs,ys))
        #This updates the Texture according to the cooridantes set by touch_began (line 17) and touch_ended (line 22).
        

run(MyScene())

# One of the things that was making it hard for me to understand was that after initially setting up the Texture, on line 9, I thought you could simply reference the subtexture() directly like this...

# self.texture_name.texture.subtexture = Rect(?,?,?,?) or # self.texture_name.subtexture = Rect(?,?,?,?)

# ... but this was not working and it racked my brain for a while. Then I tried this...

# self.texture_name.texture = Texture('test:Mandrill').subtexture(Rect(?,?,?,?))

# ... and found out that you must set, not just the subtexture, but the Texture and subtexture  the variable (self.texture_name.texture) before it's updated.
