from ambrosia import *
def placeList(obj,grp,pts):
    for (x,y,z) in pts:
        grp.add(obj,translate(x,y,z))

ball=Sphere().material(whitePlaster).scale(.1,.1,.1)
# generate 31 points from (-100 0 0) to (100 0 0) along arcing path
points=morph(30,(-100,0,0),(50,100,0),(100,0,0))
placeList(ball,scene,points)
camera.shoot()



