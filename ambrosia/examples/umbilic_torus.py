from ambrosia import *
from utils import plasterMat

triOutline=raisePoly(polygon(3,20))
tri=extrude(triOutline,translate(0,0,10))
def triTorus(n,max):
  if n == 0:
    circle = Group()
  else:
    circle = triTorus(n-1,max)
    circle.add(tri,plasterMat(360*(n/max)),
               zRot(120*(n/max))*translate(100,0,0)*yRot(-360*(n/max)))
  return circle

scene.add(triTorus(60,60),cyanPlaster)
camera.pos(xRot(30)).shoot()
