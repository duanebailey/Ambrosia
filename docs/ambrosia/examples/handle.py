from ambrosia import *
cube.handle('top',(0,50,0))
scene.add(cube,scale(.5,.5,.5)*translate(10,20,30))
scene.add(cube)
print(scene.getHandle('top'))
