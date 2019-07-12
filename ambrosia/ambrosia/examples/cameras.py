from ambrosia import *
from ambrosia.zoo.teapot import Teapot
teapot=Teapot()
scene.add(teapot,whitePlastic)
camera1 = Camera().pos((0,0,-400)).subject(scene)
camera2 = Camera().pos((-200,200,-200)).subject(scene)
image1 = camera1.getImage()
image2 = camera2.getImage()
image1.antiAlias(0).aspectRatio(2)
image2.antiAlias(1)
## Uncommenting the following line would
## have both cameras use image1
#(tell camera2 (image image1))
camera1.shoot()
camera2.shoot()
