
from scene import *
import random
import ui

A = Action
g1 ='plc:Grass_Block'
g2 ='plc:Dirt_Block'
g3 = 'plc:Brown_Block'
g4='plc:Roof_South'
g5='plc:Water_Block'
tb='plc:Wall_Block'


all_tiles_names=[g1,g2,g3,g4,g5]
all_tiles=[ui.Image(n) for n in all_tiles_names]
tile_names=[g1,g2,g1,g3,g4,g5,g2,g1]
tiles=[ui.Image(n) for n in tile_names]
current_tile=tiles[0]

mapsize=100

#map is just a nxn array of indexes to texture
themap=[[random.randint(0,len(tiles)-1) for _ in range(mapsize)] for _ in range(mapsize)]

class Arrow (SpriteNode):
    def __init__(self, **kwargs):
        SpriteNode.__init__(self, 'typw:Compass', **kwargs) 
            
class MyScene (Scene):
    def setup(self):    
        self.unit=20
        unit =self.unit
        self.items=[]
        self.points=0
        #states of buttons
        self.edit_mode=False
        self.recenter_gravity= 0,0,0


        
        self.background_color = '#000000'
        sizex,sizey=self.size
        self.ground = SpriteNode(parent=self)
        self.ground.anchor_point=(0,1)
        self.gen_map()
        
        #player
        self.ship = SpriteNode('spc:PlayerLife3Orange')
        self.ship.size=(unit,unit)
        self.ship.position = self.size / 2
        self.add_child(self.ship)
        
        #__________BUTTONS&UI_____________
        self.toolbar=SpriteNode()
        self.toolbar.color='blue'
        self.toolbar.size=(unit*16,unit*2)
        self.toolbar.position=(unit*8,unit)
        self.add_child(self.toolbar)
        
        self.edit_button=SpriteNode('emj:Wrench')
        self.edit_button.size=(unit*2,unit*2)
        self.edit_button.position=(unit,unit)
        self.add_child(self.edit_button)
        
        self.re_center=SpriteNode('emj:Anger_Symbol')
        self.re_center.size=(unit*2,unit*2)
        self.re_center.position=(unit*3,unit)
        
        self.selected=SpriteNode(g1)
        self.selected.size=(unit*2,unit*2)
        self.selected.position=(unit*8,unit)
        self.draws=SpriteNode('emj:Black_Nib')
        self.draws.size=(unit*2,unit*2)
        self.draws.position=(unit*6,unit)
        
        
        self.tree = SpriteNode('plc:Tree_Tall')
        self.tree.size=(unit*3,unit*3)
        #self.add_child(self.pb)
        
        #text on screen
        self.score= LabelNode('0')
        self.score.position=10,sizey-10
        self.add_child(self.score)
        
        
        
        
    def update_map(self):

       pass
       '''
        sizex,sizey=self.size
        self.ground.position.x
        for _ in themap:
            for tile in _:
                
                if tile.position.x+self.ground.position.x>=-self.unit and tile.position.y+self.ground.position.y>=-self.unit and tile.position.x+self.ground.position.x<= sizex +self.unit and tile.position.y+self.ground.position.y<= sizey+ self.unit:
                    tile.z_position=-1
                    self.ground.add_child(tile)
                else:
                    tile.remove_from_parent()
                    '''
    def change_tile(self,i,j,t):
        themap[i][j]=t
        unit=self.unit
        with ui.ImageContext(self.unit*mapsize,self.unit*mapsize) as ctx:
           self.mapimg.draw(0,0)
           tiles[t].draw(i*2*unit,j*2*unit,2*unit,2*unit)
           self.mapimg=ctx.get_image()
           self.ground.texture=Texture(self.mapimg)
        print('{},{},{}'.format(i,j,t))
    def gen_map(self):
        sizex,sizey=self.size
        unit=self.unit
        #laggyyyy if multi press!!!
                
        #themap=[[] for _ in range(mapsize)]
        #generate a random map
        y=-unit/5
        zpos=mapsize
        ypos=0
        with ui.ImageContext(self.unit*mapsize,self.unit*mapsize) as ctx:
           for i in range (mapsize):
              for j in range (mapsize):
                 tiles[themap[i][j]].draw(i*2*unit,j*2*unit,2*unit,2*unit)
           self.mapimg=ctx.get_image()
        self.ground.texture=Texture(self.mapimg)

            
    def place_tree(self,xy):    
        self.tree.position=xy-self.ground.position
        self.tree.z_position=2
        
        self.ground.add_child(self.tree)
        
    def projectile(self,x,y):
        ammo = Arrow(parent=self)
        ammo.size=self.unit*2,self.unit*2
        ammo.position = (self.ship.position)
        #ammo.rotation=self.ship.rotation
        actions = [A.move_to(x,y,1,6), A.remove()]
        ammo.run_action(A.sequence(actions))
        ammo.rotation=self.ship.rotation
        self.items.append(ammo)
        
    def check_ammo_collisions(self):
        sizex,sizey=self.size
        for ammo in self.items:
            if ammo.position in     self.pb.frame:
                self.items.remove(ammo)
                ammo.remove_from_parent()
                self.points+=1
                self.pb.position=random.randint(0,sizex),random.randint(0,sizey)
                
    def update(self):
        #self.update_map()
        #self.check_ammo_collisions()
        #self.score.text=str(self.points)
        
        #save old posotion
        #pos=self.ground.position
        #posx,posy=pos
        
        sizex,sizey=self.size
        x, y, z = gravity()
        #adjust for held angle of device
        #xx,yy,zz = self.recenter_gravity
        #x-=xx
        #-=yy
        #z-=zz
        
        self.ground.run_action(Action.move_by(-x * 10, -y * 10))
        
        #use old and new posotion for rotation

        self.ship.run_action(Action.rotate_to(3*math.pi/2+(math.atan2(y,x))))

    
    
    def wrench(self,xy):
        if xy in self.edit_button.bbox:
            if self.edit_mode==True:
                self.edit_mode=False
                self.edit_button.color='red'
                self.re_center.remove_from_parent()
                self.draws.remove_from_parent()
                self.selected.remove_from_parent()
            elif self.edit_mode==False:
                self.edit_mode=True 
                self.edit_button.color='#00ff00'
                self.add_child(self.re_center)
                self.add_child(self.draws)
                self.add_child(self.selected)
                
    def editmode(self,xy):  
        if xy in self.re_center.bbox:
            self.recenter_gravity=gravity()
            
        elif xy in self.draws.bbox:
            pass
            
        elif xy in self.selected.bbox:
            pass
            
    def playmode(self,xy):      
        pass    
            
    def touch_began(self, touch):
        xy =touch.location
        if xy in self.toolbar.bbox:
            self.wrench(xy)
            if self.edit_mode==True:
                self.editmode(xy)   
            else:
                self.playmode(xy)
        else:
            xy-=self.ground.position
            #non toolbar interactions
            if self.edit_mode==True:
               i=int(+xy.x//(2*self.unit))
               j=int(-1-xy.y//(2*self.unit))
               self.change_tile(i,j,0)
                
            
        

run(MyScene(), PORTRAIT, show_fps=True)

