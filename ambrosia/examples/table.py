# A simple model of a table.  N.B. Legs do not touch top.
# Height: 65 Width: 400 Depth: 100 Sits on xz-plane
# (c) 2009 duane a. bailey
from ambrosia import *
image.background(white)

# A table leg
leg = Cone().xRot(180).translate(0,-50,0).scale(0.15,0.5,0.15).material(redPlaster)

# The table 
table = Group()
table.add(cube,translate(0,50,0)*scale(4,.1,1))
table.add(leg,translate(192.5,-5,-42.5)) # front left
table.add(leg,translate(192.5,-5,42.5)) # back left
table.add(leg,translate(-192.5,-5,-42.5)) # front right
table.add(leg,translate(-192.5,-5,42.5)) # back right
table.translate(0,55,0)

scene.add(table,whitePlaster)
scene.add(table,scale(0.5,0.5,0.5)*translate(0,65,25),magentaPlaster)

# shoot the standard image
camera.shoot()
