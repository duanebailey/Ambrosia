from ambrosia import *
from random import random

def rand(low,high):
  range = high-low
  return low + range*random()

def plasterMat(hue):
  mat = Material()
  mat.type('plaster')
  mat.color(hsv2rgb((hue,1,1)))
  return mat

def snowstorm(n,flake):
  if n == 0:
    return Mesh()
  else:
    flurry = snowstorm(n-1,flake)
    t = xRot(rand(0,360))*yRot(rand(0,360))*zRot(rand(0,360))
    t = t*translate(rand(0,100),0,0)*zRot(rand(0,360))*yRot(rand(0,360))
    flurry.addPoly(t.mapPoly(flake))
    return flurry

def snowstorm2(n,flake):
  flurry = Mesh()
  for i in range(n):
    t = xRot(rand(0,360))*yRot(rand(0,360))*zRot(rand(0,360))
    t = t*translate(rand(0,100),0,0)*zRot(rand(0,360))*yRot(rand(0,360))
    flurry.addPoly(t.mapPoly(flake))
  return flurry

snowflake=raisePoly(polygon(6,5))
blizzard=snowstorm2(200,snowflake)
scene.add(blizzard,whitePlastic)
camera.shoot(scene)
