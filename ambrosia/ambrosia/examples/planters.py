from ambrosia import *

# the outline of the object to be spun around the
# y-axis.  Note the first point is repeated, to
# close the outline and the object.
cutaway=raisePoly(((10,0),(50,0),(75,50),(75,60),(60,60),(60,50),(50,10),(10,10),(10,0)))
planter=sweep(cutaway,11)
flowerPot = Spindle().profile(cutaway)
terraCotta = Material().type('plaster').color((.6,.2,0))
redwood=Material().type('plaster').color((1,.2,0))
scene.add(planter,redwood,translate(-80,0,0))
scene.add(flowerPot,terraCotta,translate(80,0,0))

camera.pos((0,400,-100)).shoot()
