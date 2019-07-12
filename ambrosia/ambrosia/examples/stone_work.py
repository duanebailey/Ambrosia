# Constructing stonework for facades
# (c) 2009 duane a. bailey

# the purpose, here, is to construct appropriately shaped
# "antimatter" detail than can be removed from a block
# wood or stone used in molding or facades.
from ambrosia import *

# this describes the shape that is scooped from a standard
# length (in z-direction) object.

# you may find it useful to:
# 1. Look at the routerBit directly, or
# 2. Change the Difference to a Group to help with positioning.
routerBit = Difference()
routerBit.add(cube,scale(1,1,1.05)) # slightly long
routerBit.add(cylinder,xRot(90)*scale(0.5,0.5,1.1)*translate(40,-40,0))

# out router works on a standard cube
stone = Difference()
stone.add(cube)
stone.add(routerBit,scale(1,1,1.1)*translate(-50,50,0))

sandstone=(.8,.7,.5)
sandstoneMat=Material()
sandstoneMat.color(sandstone).type('plaster')

# view the stone
scene.add(stone,sandstoneMat,translate(0,0,50)*scale(1,1,1))
scene.add(bulb,translate(0,100,0))
scene.add(bulb,translate(0,300,0))
scene.add(bulb,translate(0,600,0))
scene.add(bulb,translate(0,0,-300))

camera.COI((-25,25,0)).pos((-35,35,-300)).shoot()

