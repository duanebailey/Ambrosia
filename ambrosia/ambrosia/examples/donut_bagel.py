# Donut Builder model.
from ambrosia import *
donut=Torus().minor(15).major(25)
bagel=Torus().minor(30).major(30).scale(1,0.5,1)
scene.add(donut,redPlaster,translate(-50,0,0))
scene.add(bagel,bluePlaster,translate(50,0,0))
camera.pos((0,0,-200)).pos(xRot(70)).shoot()
