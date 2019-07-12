from ambrosia import *
outline=[(0,10)]
outline.extend(morph(20,(25,10),(55,10),(90,20),(90,50)))
# the points at end of previous and start of next form lip at top
outline.extend(morph(20,(50,100),(50,80),(100,70),(100,50))[1:])
outline.extend(morph(20,(100,50),(100,20),(55,0),(25,0))[1:])
outline.extend([(0,0)])
roseBowlOL=raisePoly(outline)
roseBowl=sweep(roseBowlOL,5)
scene.add(roseBowl)
camera.shoot()
