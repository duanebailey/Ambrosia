from ambrosia import *

wall = Plane().material(whitePlaster).translate(0,-500,0)
room = Group().add(wall).add(wall,xRot(-90)).add(wall,zRot(-90))
myCyan = (0,1,1)
myTransparentMat = Material()
myTransparentMat.color(myCyan).diffuse(.5).transparency(0.8).refraction(1.5).reflection(0).roughness(0.05).specularity(1)
myBlueShinyMat = Material().color(blue).reflection(0.8).specularity(0.8).transparency(0).diffuse(0.5).roughness(0.05)
myGreenPlaster = Material().diffuse(1).reflection(0).roughness(1).specularity(0).transparency(0).refraction(1).color(hsv2rgb((120,1,1)))
scene.add(room)
scene.add(cone,myGreenPlaster)
scene.add(cube,myTransparentMat,translate(-50,0,-70)).add(sphere,myBlueShinyMat,translate(110,0,50))
camera.pos((0,100,-300)).shoot()
