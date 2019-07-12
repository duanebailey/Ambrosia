from ambrosia import *
image.background(white)
circularFrame = Difference()
circularFrame.add(cylinder,xRot(-90)).add(cylinder,xRot(-90)*scale(.9,.9,1.1))
circularFrame.xform(scale(1,1,0.05)*translate(-20,0,0)*zRot(30))

third0 = Difference()
third0.add(circularFrame).add(cube,translate(-50,0,0)*scale(1,2,1))
third = Difference()
third.add(third0,zRot(-60)).add(cube,translate(-50,0,0)*scale(1,2,1)).zRot(60)
frame = Group()
frame.add(third).add(third,zRot(120)).add(third,zRot(-120))
scene.add(frame,scale(2),yellowPlaster)
camera.shoot()
