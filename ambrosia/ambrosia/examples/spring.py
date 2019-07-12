from ambrosia import *
def multigon(n,poly,initXform,delXform):
  if n == 0:
    return []
  else:
    return [initXform.map(poly)] + multigon(n-1,poly,initXform*delXform,delXform)

springXsect=raisePoly([(-10,-1),(10,-1),(10,1),(-10,1)])
springFrame=multigon(361,springXsect,translate(100,0,0),translate(0,1,0)*yRot(10))
spring=loft(*springFrame)

scene.add(spring,bluePlaster)

camera.shoot()

