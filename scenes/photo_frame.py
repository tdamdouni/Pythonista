import photos, random, scene, sys

photo_count = photos.get_count()
fmt = '{} photos in your camera roll...'
print(fmt.format(photo_count))

if not photo_count:
    sys.exit('Pythonista does not have access to the camera roll or the camera roll is empty.')

def get_random_photo():  # returns the name (a string) of a random photo from the camera role
    return scene.load_pil_image(photos.get_fullscreen_image(random.randint(0, photo_count)))

class MyScene(scene.Scene):
    def __init__(self):
        scene.run(self)

    def setup(self):
        self.photo_layer = scene.Layer(self.bounds)
        self.add_layer(self.photo_layer)
        self.frame_count = 0

    def draw(self):
        scene.background(0, 0, 0)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        if not self.frame_count % 180:  # once every three seconds
            if self.photo_layer.image:  # unload old image to save RAM
                scene.unload_image(self.photo_layer.image)
            self.photo_layer.image = get_random_photo()
        self.frame_count += 1

MyScene()
