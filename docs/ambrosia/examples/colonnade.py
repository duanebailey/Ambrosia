from ambrosia import *

def colonnade(n):
  if n == 0:
    return Group()
  else:
    columns = colonnade(n-1)
    column = Cylinder()
    column.scale(0.05,1,0.05).material(whitePlaster)
    columns.add(column,translate(n*20,0,0))
    return columns

scene.add(colonnade(10),yRot(-45))
camera.pos(xRot(20)).shoot()
