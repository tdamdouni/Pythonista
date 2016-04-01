# Planes game made with Pie

import gamepie as pie

import random

class Game(pie.Game):
    def conf(self):
        self.title = "Planes" # Window title
        self.version = "0.1" # Game version
        self.gamepie = "0.1" # GamePie version
        self.size = (480, 800)
        pie.require("graphics",
                    "audio",
                    "keyboard",
                    "mouse",
                    "system")

    def load(self):
        self.planeImg = pie.graphics.newImage("assets/plane.png")
        self.bulletImg = pie.graphics.newImage("assets/bullet.png")
        self.enemyImg = pie.graphics.newImage("assets/enemy.png")
        
        self.bulletSound = pie.audio.newSource("assets/gun-sound.wav")

        self.plane = pie.graphics.Sprite(self.planeImg)
        self.plane.x = (pie.graphics.getWidth() - self.plane.w)/2
        self.plane.y = pie.graphics.getHeight() - self.plane.h
        self.plane.speed = 150
        self.plane.alive = True
        self.plane.score = 0

        self.bullets = []
        self.enemies = []

        self.buttondown = False
        self.presspos = 0

        self.maxShootTimer = 0.4
        self.shootTimer = self.maxShootTimer

        self.maxEnemyTimer = 1
        self.enemyTimer = self.maxEnemyTimer

    def mousepressed(self, x, y, button):
        if self.plane.contains((x, y)):
            self.buttondown = True
            self.presspos = x - self.plane.x

    def mousereleased(self, x, y, button):
        self.buttondown = False

    def mousemoved(self, x, y, dx, dy):
        if self.buttondown:
            self.plane.x = x - self.presspos
            if self.plane.x < 0:
                self.plane.x = 0
            elif self.plane.x + self.plane.w > pie.graphics.getWidth():
                self.plane.x = pie.graphics.getWidth() - self.plane.w

    def update(self, dt):
        # Handle events (key presses, etc)

        if self.shootTimer > 0:
            self.shootTimer -= dt

        if pie.system.getOS() == "iOS":
            self.events_iOS(dt)
        else:
            self.events_desktop(dt)

        if not self.plane.alive:
            return

        for bullet in self.bullets:
            bullet.y -= bullet.speed * dt
            if bullet.y + bullet.w < 0:
                self.bullets.remove(bullet)

        for enemy in self.enemies:
            enemy.y += enemy.speed * dt
            if enemy.y > pie.graphics.getHeight():
                self.enemies.remove(enemy)

            for bullet in self.bullets:
                if enemy.collides(bullet):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.plane.score += 1
                    continue

            if enemy.collides(self.plane):
                self.plane.alive = False
                self.enemies = []
                self.bullets = []

        self.enemyTimer -= dt
        if self.enemyTimer <= 0:
            self.enemyTimer = self.maxEnemyTimer
            enemy = pie.graphics.Sprite(self.enemyImg)
            enemy.speed = 150
            enemy.x = random.randint(0, pie.graphics.getWidth() - enemy.w)
            enemy.y = -enemy.h
            self.enemies.append(enemy)

    def events_iOS(self, dt):
        if self.shootTimer <= 0:
            self.shootTimer = self.maxShootTimer
            bullet = pie.graphics.Sprite(self.bulletImg)
            bullet.speed = 200
            bullet.y = self.plane.y - bullet.h/2
            bullet.x = self.plane.x + (self.plane.w - bullet.w)/2
            self.bullets.append(bullet)
            self.bulletSound.play()
    
    def events_desktop(self, dt):
        if pie.keyboard.isKeyPressed("escape"):
            self.exit()

        if not self.plane.alive:
            return

        if pie.keyboard.isKeyPressed("space"):
            if self.shootTimer <= 0:
                self.shootTimer = self.maxShootTimer
                bullet = pie.graphics.Sprite(self.bulletImg)
                bullet.speed = 200
                bullet.y = self.plane.y - bullet.h/2
                bullet.x = self.plane.x + (self.plane.w - bullet.w)/2
                self.bullets.append(bullet)
                self.bulletSound.play()

        if pie.keyboard.isKeyPressed("left", "a"):
            self.plane.x -= self.plane.speed * dt
            if self.plane.x < 0:
                self.plane.x = 0

        elif pie.keyboard.isKeyPressed("right", "d"):
            self.plane.x += self.plane.speed * dt
            if self.plane.x + self.plane.w > pie.graphics.getWidth():
                self.plane.x = pie.graphics.getWidth() - self.plane.w

    def draw(self, dt):
        if self.plane.alive:
            pie.graphics.drawSprite(self.plane)

            for bullet in self.bullets:
                pie.graphics.drawSprite(bullet)

            for enemy in self.enemies:
                pie.graphics.drawSprite(enemy)

            pie.graphics.write("Score: %d" % self.plane.score, 0, 0)
        else:
            pie.graphics.write("Game Over! Your score: %d" %
                self.plane.score, 0, 0)

planes_game = Game()
pie.run(planes_game)
