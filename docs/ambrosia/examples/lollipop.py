# A week old lollipop (c) 2008 duane a. bailey
from ambrosia import *
from utils import rand

popdrop=Group()
popdrop.add(cylinder,whitePlaster,translate(0,50,0)*scale(0.05,1,0.05))
popdrop.add(cylinder,xRot(90),scale(.5,.5,.06)*translate(0,100,0))

def randomCandyMat():
  mat = Material()
  colour = hsv2rgb((rand(0,360),1,1,))
  mat.color(colour).transparency(0.3).refraction(1.6)
  return mat

def pop(n):
  if n == 1:
      return popdrop
  else:
      bud = pop(n-1)
      gamma=39
      gammaPrime=40
      plant = Group()
      plant.add(popdrop,yRot(rand(0,360)),randomCandyMat())
      plant.add(bud,randomCandyMat(),yRot(rand(0,360))*scale(golden)*zRot(-gamma)*translate(0,61.8,0))
      plant.add(bud,randomCandyMat(),yRot(rand(0,360))*scale(golden)*zRot(gammaPrime)*translate(0,39,0))
      return plant
          
scene=Group()
scene.add(bulb,translate(0,300,-300))
scene.add(pop(9),translate(0,-65,0)*scale(2.5))
camera.shoot(scene)
