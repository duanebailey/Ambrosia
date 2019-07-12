## A hot air balloon toolkit, from Ben Grass '07
from ambrosia import *

## Use whatever image you wish, here, to cover the balloon
irisMat = Material().surfaceImage('Irises.png')

## The number of fabric panels in balloon (we only place 3)
n=12

## A bezier curve defining the right interface of a panel
right=raisePoly([(30,-120),(150,30),(165,144),(0,150)])

## A control curve, expanded out for billowing effect
almostRight=(scale(1.3,1,1)*yRot(120/n)).mapPoly(right)

# Another control curve, expanded out similarly
almostLeft=(scale(1.3,1,1)*yRot(240/n)).mapPoly(right)

# Bezier curve defining the left edge
left=yRot(360/n).mapPoly(right)

# the 16 points describing the panel
panelPatch=left+almostLeft+almostRight+right

# A function that constructs the UV coordinates for
# panel m out of n
def panelUV(m,n):
  leftU = ((n-m-1)/n)
  rightU = ((n-m)/n)
  return [(leftU,0),(leftU,1),(rightU,1),(rightU,0)]

# A (partial) balloon - the first three panels
# note refinement is high
# balloon=PatchMesh()
# balloon.addPatch(panelPatch)
# balloon.addPatch(yRot(360/n).mapPoly(panelPatch))
# balloon.addPatch(yRot(360*2/n).mapPoly(panelPatch))
# balloon.refinement(5)

balloon=PatchMesh()
balloon.addUVPatch(panelPatch,panelUV(0,n))
balloon.addUVPatch(yRot(360/n).mapPoly(panelPatch),panelUV(1,n))
balloon.addUVPatch(yRot(360*2/n).mapPoly(panelPatch),panelUV(2,n))
balloon.refinement(5)

scene.add(balloon,irisMat)
camera.shoot()
