from ambrosia import *

def multiadd(n,obj,grp,initXform,delXform):
  if n > 0:
    grp.add(obj,initXform)
    multiadd(n-1,obj,grp,initXform*delXform,delXform)

step = Cube().scale(.5,.1,.2).material(bluePlaster)
stairway = Group()
#multiadd(20,step,stairway,translate(100,-120,0),translate(0,12,0)*yRot(-15))
multiadd(20,step,stairway,translate(0,-120,0),translate(0,15,15))

scene.add(stairway)
camera.shoot()
