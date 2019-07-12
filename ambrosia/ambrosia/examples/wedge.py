from ambrosia import *
front = translate(0,0,-50).mapPoly(raisePoly(((-50,-50),(50,-50),(50,50),(-50,50))))
box = extrude(front,translate(0,0,100)*scale(0.05,2,1))
scene.add(box,redPlaster)
isoCamera=IsometricCamera()
isoCamera.shoot(scene)
