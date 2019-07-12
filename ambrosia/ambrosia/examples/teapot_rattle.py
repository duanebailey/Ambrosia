## This is a model of a child's rattle, with a silver teapot
## trapped in the center.
## (c) 2009 Duane A. Bailey
#
# For purposes of understanding, each primitive object used
# in this construction is cast from a different material.
# This allows you to see that the sphere (green) cuts the
# corners from the cube (blue), etc.

from ambrosia import *
from ambrosia.zoo.teapot import Teapot

# The outer components
roundedBox = Intersection()
roundedBox.add(cube,bluePlaster)
roundedBox.add(sphere,scale(1.5,1.5,1.5),greenPlaster)

# We now carve out the interior with a large red sphere
rattleBase = Difference()
rattleBase.add(roundedBox).add(sphere,scale(1.2),redPlaster)

# construct a teapot
dipper = Teapot()

# construct the rattle: add teapot to rattleBase
rattle = Group()
rattle.add(rattleBase).add(dipper,translate(30,-20,0),mirrorMat)

# add the rattle to the scene.  No material needs to be 
# specified because everything already has a material.
scene.add(rattle).add(bulb,translate(0,100,0)).add(bulb,translate(0,0,-100))

# tame the background (for wiki use)
image.background(white)

# shoot
camera.pos((100,150,-300)).shoot()

