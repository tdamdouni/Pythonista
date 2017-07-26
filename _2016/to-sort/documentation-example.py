# https://forum.omz-software.com/topic/3147/documentation-examples

import ui

class DrawSomething(ui.View):
    rect = (0, 0, 200, 200)
    
    def draw(self):
        self.my_draw()
        
    def my_draw(self):
        with ui.GState():
            ui.set_color('deeppink')
            shape = ui.Path.rect(*self.rect)
            shape.fill()
                
    def image_get(self):
        with ui.ImageContext(self.rect[2], self.rect[3]) as ctx:
            self.my_draw()
            img = ctx.get_image()
            img.show()
            return img
    def image_save(self, path):
        img = self.image_get()
        with open(path, 'wb') as file:
            file.write(img.to_png())

if __name__ == '__main__':
    ds = DrawSomething()
    ds.present('sheet')
    ds.image_get()
    ds.image_save('test2.png')
