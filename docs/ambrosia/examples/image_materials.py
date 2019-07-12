# A model demonstrating the differences between
# surface and grain images. (c) 2008 duane a. bailey
from ambrosia import *
sunnyMaterial = Material().surfaceImage('Sunflower.png')
sunnyGrainMaterial = Material().grainImage('Sunflower.png')

scene.add(cube,translate(-100,0,-100),sunnyMaterial)
scene.add(cube,translate(100,0,100),sunnyGrainMaterial)
scene.add(bulb,translate(0,0,-300))
scene.add(bulb,translate(0,300,0))
scene.add(bulb,translate(-300,0,0))

IsometricCamera().shoot(scene)
