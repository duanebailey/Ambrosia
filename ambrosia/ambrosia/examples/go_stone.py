# A go stone, second attempt. (c) 2008 duane a. bailey
from ambrosia import *

goStone = Intersection()
goStone.add(sphere,scale(1,0.4,1)).add(cylinder,scale(.985,1,0.985))

scene.add(goStone,whitePlaster)

image.background(dkGray)
camera.pos((0,0,-200)).shoot()
