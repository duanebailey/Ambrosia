from ambrosia import *

Hexagon2D = polygon(6)
Hexagon3D = raisePoly(Hexagon2D)

hexWrench = extrude(Hexagon3D,translate(0,0,100))
nut = Difference()
nut.add(sphere,yellowPlaster).add(cube,translate(0,-50,0)*scale(1.5))
nut.add(hexWrench,bluePlaster,scale(.5,.5,1)*xRot(-90)*translate(0,20,0))
image.background(white)
scene.add(nut,xRot(-45))
camera.shoot()
