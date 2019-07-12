# Adapted from: Flight of the Umbrellas
# (c) 2009 Susan Raich
from ambrosia import *
image.background(white)
#building an umbrella
# the top part of the umbrella: first attempts
umbrellaTop0 = Difference()
umbrellaTop0.add(sphere)
#make the umbrella into a mere shell
umbrellaTop0.add(sphere,scale(.95))
# I want just the top curve of the umbrella
umbrellaTop0.add(cube,scale(1.1)*translate(0,-55,0))

# constructing a drill to cut out little arcs on the edge of the umbrella 
umbrellaBit=Cylinder()
umbrellaBit.xRot(90)
umbrellaBit.scale(.262,.262,2)
#12 of them will fit around my umbrella top of diameter 100: computed as ((/ (* 25 pi) 300)


# a group to put the collected bits in
umbrellaDrill = Group()
for a in [0,30,60,90,120,150]:
    umbrellaDrill.add(umbrellaBit,yRot(a))

# the final top: 
umbrellaTop = Difference().add(umbrellaTop0).add(umbrellaDrill) 

#Now, building the umbrella handle
grip0 = Torus().major(10).minor(2.5)
grip = Difference().add(grip0).add(cube,translate(0,0,50))
handle = Group()
handle.add(cylinder,scale(0.05,1,0.05))
handle.add(grip,xRot(-90)*translate(-10,-50,0))
handle.material(yellowPlaster)

#put together the umbrella top and the handle
raichUmbrella=Group()
raichUmbrella.add(umbrellaTop).add(handle)

scene.add(raichUmbrella,purplePlastic,scale(2))

camera.shoot()
