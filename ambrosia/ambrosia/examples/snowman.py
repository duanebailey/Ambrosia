# Duane Bailey (c) 2014
# A snowman.
from ambrosia import *
noseSize=.5
eyeSize=.1  # size of eye
eyeUp=10     # angle of eye, above noze
eyeAngle=25  # angle of eye, measured from midline
# an orange material
orange=(1,0.5,0)
orangePlaster = Material()
orangePlaster.type('plaster').color(orange)
head = Group()
head.add(sphere,whitePlaster)
head.add(cone,magentaPlaster,translate(0,50,0)*scale(0.24,1,0.24)*scale(noseSize)*xRot(-90)*translate(0,0,-45))
head.add(sphere,blackPlaster,scale(eyeSize),translate(0,0,-50)*xRot(eyeUp)*yRot(eyeAngle))
head.add(sphere,blackPlaster,scale(eyeSize),translate(0,0,-50)*xRot(eyeUp)*yRot(-eyeAngle))
head.translate(0,50,0)
head.scale(0.5)
# sphere.translate(0,50,0)
snowman = Group()
snowman.add(sphere,whitePlaster,translate(0,50,0))
snowman.add(sphere,whitePlaster,translate(0,50,0)*scale(.75)*translate(0,100,0))
snowman.add(head,orangePlaster,translate(0,175,0))
# A second head, for 13-old boys:
# snowman.add(head,purplePlaster,translate(0,225,0)*yRot(180))
scene.add(snowman,scale(golden))
# To see him in profile:
# scene.add(snowman,scale(golden)*yRot(-90))
camera.shoot()
