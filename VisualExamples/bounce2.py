from visual import *

print("""
Right button drag to rotate "camera" to view scene.
  On a one-button mouse, right is Command + mouse.
Middle button to drag up or down to zoom in or out.
  On a two-button mouse, middle is left + right.
  On a one-button mouse, middle is Option + mouse.
""")

side = 4.0
thk = 0.3
s2 = 2*side - thk
s3 = 2*side + thk
wallR = box (pos=( side, 0, 0), length=thk, height=s2,  width=s3,  color = color.red)
wallL = box (pos=(-side, 0, 0), length=thk, height=s2,  width=s3,  color = color.red)
wallB = box (pos=(0, -side, 0), length=s3,  height=thk, width=s3,  color = color.blue)
wallT = box (pos=(0,  side, 0), length=s3,  height=thk, width=s3,  color = color.blue)
wallBK = box(pos=(0, 0, -side), length=s2,  height=s2,  width=thk, color = (0.7,0.7,0.7))

ball = sphere (color = color.green, radius = 0.4)
ball.mass = 1.0
ball.p = vector (-0.15, -0.23, +0.27)

side = side - thk*0.5 - ball.radius

dt = 0.5
t=0.0
while True:
  rate(100)
  t = t + dt
  ball.pos = ball.pos + (ball.p/ball.mass)*dt
  if not (side > ball.x > -side):
    ball.p.x = -ball.p.x
  if not (side > ball.y > -side):
    ball.p.y = -ball.p.y
  if not (side > ball.z > -side):
    ball.p.z = -ball.p.z
