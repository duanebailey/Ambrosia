# A simple clown model.  (c) 2008 Duane Bailey
# Demonstration from February 4, 2008

# This following line is required for every model
from ambrosia import *

# These lines we didn't see in class; they just give names to ("define") constants
eyeAngle=30
eyeNoseAngle=18.5

# This object is just a single clown eye, default material, at the origin
clownEye = Group()
clownEye.add(sphere,scale(.1,.1,.1))

# This is an entire clown
clown = Group()
clown.add(sphere)
clown.add(sphere,whitePlaster,scale(.2,.2,.2)*translate(0,0,-50))
clown.add(clownEye,bluePlaster,translate(0,0,-50)*xRot(eyeAngle)*yRot(eyeNoseAngle))
clown.add(clownEye,greenPlaster,translate(0,0,-50)*xRot(eyeAngle)*yRot(-eyeNoseAngle))

# add two clowns; the new material sticks to parts of objects without
# previously defined material
scene.add(clown,whitePlaster,translate(100,0,0))
scene.add(clown,redPlaster,translate(-100,0,0))

# idiom for taking pictures
image.background(white)
camera.shoot()

