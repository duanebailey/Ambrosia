#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
"""Ambrosia, a graphics modeling system.

website: http://www.cs.williams.edu/~bailey/Ambrosia
(c) 2013 duane a. bailey

Ambrosia is a collection of Python classes that allow a camera-oriented
abstraction as an interface to rendering engines.  Currently, only the
POV renderer is supported.

From outside Python, you can get help on a particular ambrosia name
with
   pydoc3 ambrosia.name
Inside Python, you must 
   from ambrosia import *
then
   help(name)
"""
import ambrosia.license
from ambrosia.decorators import *
from ambrosia.basics import *
from ambrosia.objects import *
from ambrosia.cameras import *
from ambrosia.lights import *
from ambrosia.parts import *
from ambrosia.meshes import *
from ambrosia.surfaces import *
from ambrosia.polyhedra import *

from ambrosia.decorators import __all__ as _decorators_all
from ambrosia.basics import __all__ as _basics_all
from ambrosia.objects import __all__ as _objects_all
from ambrosia.cameras import __all__ as _cameras_all
from ambrosia.lights import __all__ as _lights_all
from ambrosia.parts import __all__ as _parts_all
from ambrosia.meshes import __all__ as _meshes_all
from ambrosia.surfaces import __all__ as _surfaces_all
from ambrosia.polyhedra import __all__ as _polyhedra_all
# Synthesize an export list
__all__ = ['bulb', 'camera', 'cube', 'cylinder', 'cone', 'image', 'scene', 'sphere','license']
for x in [ _decorators_all,_basics_all,_objects_all,_cameras_all,_lights_all,_parts_all,_meshes_all,_surfaces_all,_polyhedra_all]:
    __all__.extend(x)
__all__.sort(key=lambda x: x.lower())

###############################################################################
# Globals for scene setup
sphere = None
cube = None
cylinder = None
cone = None
bulb = None
scene = None
camera = None
image = None

def reset():
    global sphere,cube,cylinder,cone,bulb,scene,camera,image
    sphere = Sphere()
    cube = Cube()
    cylinder = Cylinder()
    cone = Cone()
    bulb = Light().color(white)
    scene = Group().add(bulb,translate(0,300,-300))
    camera = Camera().subject(scene)
    image = camera.getImage()

reset()
