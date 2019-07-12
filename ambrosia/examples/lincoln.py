# Spotlights and postcards (c) 2008 Duane A. Bailey
from ambrosia import *

# The following mesh has one polygon with corresponding
# uv-coordinates
postcard = Mesh()
postcard.addUVPoly([[-100,-100,0],[100,-100,0],[100,100,0],[-100,100,0]],[[0,0],[1,0],[1,1],[0,1]])

# A material that wallpapers surfaces
lincolnPaper=Material().surfaceImage('Lincoln.png')

# A spotlight that shines on the origin
spot=Spotlight().pos((0,0,-200)).COI((0,0,0)).radius(5).falloff(0)

scene.add(spot).add(postcard,lincolnPaper)
camera.shoot()
