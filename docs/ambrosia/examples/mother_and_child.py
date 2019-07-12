# Mother & Child, a Moore homage. (c) 2008 Duane A. Bailey
from ambrosia import *

# I'm not pleased with these colors, probably due to poor lighting
pink=(1,.75,.75)
babyBlue=(.75,.75,1)
pinkPlaster = Material().type('plaster').color(pink)
babyBluePlaster = Material().type('plaster').color(babyBlue)
mother = Difference()
mother.add(sphere,pinkPlaster,scale(1,3,1))
mother.add(cylinder,mirrorMat,scale(0.5,3,0.5)*zRot(-60)*translate(0,30,-40))
child = Group()
child.add(sphere,babyBluePlaster,scale(.4,1.2,.3))
family = Group().add(mother).add(child,zRot(-60)*translate(0,30,-37))
family.add(bulb,translate(0,0,-17.5))

# To better control lighting, we build a lighting object with our lamps
# where we actually want them (bulb starts at origin).
lighting = Group()
lighting.add(bulb,translate(-200,0,-500))
lighting.add(bulb,translate(200,0,-500))

# create a *new* scene, with no initial lights, add lighting
scene = Group()
scene.add(lighting).add(family,zRot(-10))
image.background((1,0.95,0.95))
camera.subject(scene).shoot()
