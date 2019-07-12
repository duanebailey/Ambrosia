#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
#
"""This module contains all the primitive modelling objects."""
from ambrosia.decorators import *
from ambrosia.basics import *
from ambrosia.objects import *
from ambrosia.cameras import *

__all__ = ('Cone', 'Cube', 'Cylinder', 'Plane', 'Sphere', 'Superellipsoid', 'Torus', 'SOR', 'Spindle', 'Prism')

###############################################################################
# Cube.  A solid CSG cube.
@checkdoc
class Cube(Primitive):
    """A regular cube, 100 units on a side."""
    def __init__(self,description="A cube."):
        """Construct a basic cube."""
        super().__init__(description=description)
        self.dimensions(100,100,100)

    def dimensions(self,dx,dy,dz):
        """Set the dimensions of the cube."""
        self.set('cube.dimensions',(dx,dy,dz))
        return self

    def getDimensions(self):
        """Get the base dimensions of the cube."""
        return self.get('cube.dimensions')

    def _POV_(self,context):
        if context.selects(self):
            d = self.getDimensions()
            t = self.getXform()
            prt('box { ')
            pov.writePoint(vectorScale(d,-0.5))
            pov.writePoint(vectorScale(d,0.5))
            prt('\n')
            POV(super(),context)
            prt('}\n')

###############################################################################
# Plane: an infinite flat surface
@checkdoc
class Plane(Primitive):
    """A class that describes a plane."""
    def __init__(self,description="A plane."):
        super().__init__(description=description)
        self.normal(0,1,0).offset(0)

    def normal(self,x,y,z):
        """Describe a vector pointing out of front of plane."""
        self.set('plane.normal',normalize([x,y,z]))
        return self

    def getNormal(self):
        """Get a (unit) vector pointing out of front of plane."""
        return self.get('plane.normal')

    def offset(self,o):
        """Set the distance of the plane from the origin."""
        self.set('plane.offset',o)
        return self

    def getOffset(self):
        """Get the distance of the plane from the origin."""
        return self.get('plane.offset')

    def _POV_(self,context):
        if context.selects(self):
            n = self.getNormal()
            o = self.getOffset()
            t = self.getXform()
            m = self.getMaterial()
            prt('plane { ')
            pov.writePoint(n)
            prt(',{}\n'.format(o))
            POV(super(),context)
            prt('}\n')

###############################################################################
# Sphere
@checkdoc
class Sphere(Primitive):
    """Sphere objects."""
    def __init__(self,description="A sphere."):
        super().__init__(description=description)
        self.center([0,0,0]).radius(50)

    def center(self,p):
        """Set the center of the sphere."""
        self.set('sphere.center',p)
        return self

    def getCenter(self):
        """Get the center of the sphere."""
        return self.get('sphere.center')

    def radius(self,r):
        """Set the radius of the sphere."""
        self.set('sphere.radius',r)
        return self

    def getRadius(self):
        """Get the radius of the sphere."""
        return self.get('sphere.radius')

    def _POV_(self,context):
        if context.selects(self):
            c = self.getCenter()
            r = self.getRadius()
            t = self.getXform()
            m = self.getMaterial()
            prt('sphere { ')
            pov.writePoint(c)
            prt(',{}\n'.format(r))
            POV(super(),context)
            prt('}\n')

###############################################################################
# Cone
@checkdoc
class Cone(Primitive):
    def __init__(self,description="A cone."):
        super().__init__(description=description)
        self.topCenter([0,50,0]).topRadius(0)
        self.bottomCenter([0,-50,0]).bottomRadius(50)
        self.capped(True)

    def topCenter(self,v):
        """Set the topCenter."""
        self.set('cone.topCenter',v)
        return self

    def getTopCenter(self):
        """Get the topCenter."""
        return self.get('cone.topCenter')

    def bottomCenter(self,v):
        """Set the bottomCenter."""
        self.set('cone.bottomCenter',v)
        return self

    def getBottomCenter(self):
        """Get the bottomCenter."""
        return self.get('cone.bottomCenter')

    def topRadius(self,v):
        """Set the topRadius."""
        self.set('cone.topRadius',v)
        return self

    def getTopRadius(self):
        """Get the topRadius."""
        return self.get('cone.topRadius')

    def bottomRadius(self,v):
        """Set the bottomRadius."""
        self.set('cone.bottomRadius',v)
        return self

    def getBottomRadius(self):
        """Get the bottomRadius."""
        return self.get('cone.bottomRadius')

    def capped(self,v):
        """Set the capped."""
        self.set('cone.capped',v)
        return self

    def getCapped(self):
        """Get the capped."""
        return self.get('cone.capped')

    def _POV_(self,context):
        if context.selects(self):
            topCenter = self.getTopCenter()
            bottomCenter = self.getBottomCenter()
            topRadius = self.getTopRadius()
            bottomRadius = self.getBottomRadius()
            capped = self.getCapped()
            t = self.getXform()
            m = self.getMaterial()
            prt('cone { ')
            pov.writePoint(topCenter)
            prt(',{} '.format(topRadius))
            pov.writePoint(bottomCenter)
            prt(',{}\n'.format(bottomRadius))
            if not capped:
                prt(' open')
            POV(super(),context)
            prt('}\n')
    

###############################################################################
# Cylinder
@checkdoc
class Cylinder(Primitive):
    def __init__(self,description="A cylinder"):
        super().__init__(description=description)
        self.topCenter([0,50,0]).bottomCenter([0,-50,0])
        self.radius(50).capped(True)

    def topCenter(self,v):
        """Set the topCenter."""
        self.set('cylinder.topCenter',v)
        return self

    def getTopCenter(self):
        """Get the topCenter."""
        return self.get('cylinder.topCenter')

    def bottomCenter(self,v):
        """Set the bottomCenter."""
        self.set('cylinder.bottomCenter',v)
        return self

    def getBottomCenter(self):
        """Get the bottomCenter."""
        return self.get('cylinder.bottomCenter')

    def radius(self,v):
        """Set the topRadius."""
        self.set('cylinder.radius',v)
        return self

    def getRadius(self):
        """Get the radius."""
        return self.get('cylinder.radius')

    def capped(self,v):
        """Set the capped."""
        self.set('cylinder.capped',v)
        return self

    def getCapped(self):
        """Get the capped."""
        return self.get('cylinder.capped')

    def _POV_(self,context):
        if context.selects(self):
            topCenter = self.getTopCenter()
            bottomCenter = self.getBottomCenter()
            radius = self.getRadius()
            capped = self.getCapped()
            t = self.getXform()
            m = self.getMaterial()
            prt('cylinder { ')
            pov.writePoint(topCenter)
            pov.writePoint(bottomCenter)
            prt(',{}\n'.format(radius))
            if not capped:
                prt(' open')
            POV(super(),context)
            prt('}\n')
    
###############################################################################
# Superellipsoid
@checkdoc
class Superellipsoid(Primitive):
    def __init__(self,description="A superellipsoid."):
        super().__init__(description=description)
        self.roundness(1,1).scale(50,50,50)

    def roundness(self,a,b):
        """Set the roundness."""
        self.set('superellipsoid.roundness',(a,b))
        return self

    def getRoundness(self):
        """Get the roundness."""
        return self.get('superellipsoid.roundness')

    def _POV_(self,context):
        if context.selects(self):
            r = self.getRoundness()
            t = self.getXform()
            m = self.getMaterial()
            prt('superellipsoid {{ <{}, {}>\n'.format(r[0],r[1]))
            POV(super(),context)
            prt('}\n')

###############################################################################
# Torus
@checkdoc
class Torus(Primitive):
    def __init__(self,description="A torus."):
        super().__init__(description=description)
        self.major(75).minor(25)
    
    def major(self,v):
        """Set the major."""
        self.set('torus.major',v)
        return self

    def getMajor(self):
        """Get the major."""
        return self.get('torus.major')

    def minor(self,v):
        """Set the minor."""
        self.set('torus.minor',v)
        return self

    def getMinor(self):
        """Get the minor."""
        return self.get('torus.minor')

    def sturmian(self,v):
        """Set the sturmian."""
        self.set('torus.sturmian',v)
        return self

    def getSturmian(self):
        """Get the sturmian."""
        return self.get('torus.sturmian')
    

    def _POV_(self,context):
        if context.selects(self):
            major = self.getMajor()
            minor = self.getMinor()
            t = self.getXform()
            m = self.getMaterial()
            prt('torus {')
            if self.getSturmian():
                prt('sturm ')
            prt('{},{}\n'.format(major,minor))
            POV(super(),context)
            prt('}\n')

################################################################################ SOR: a surface of discrete or continuous revolution
@checkdoc
class SOR(Primitive):
    def __init__(self,description="A SOR object."):
        super().__init__(description=description)
        self.linear() # other choice: Bezier
        self.set('sturm',False)

    def profile(self,poly):
        """Describe the profile of the SOR."""
        self.set('SOR.profile',poly.copy())
        if self.getType() == 'bezier':
            self._checkBezierProfile()
        return self

    def getProfile(self):
        """Return the SOR profile."""
        return self.get('SOR.profile')

    def linear(self):
        """Set the SOR type to be linear."""
        self.set('SOR.type',"linear")
        return self

    def bezier(self):
        """Set the SOR type to be bezier."""
        self.set('SOR.type',"bezier")
        self._checkBezierProfile()
        return self

    def _checkBezierProfile(self):
        p = self.getProfile()
        l = len(p)
        assert l%4 == 0,"Warning: Bezier-type object has profile {} of length {}, which must be a multiple of 4.".format(p,l)
        for j in range(4,l,4):
            i = j-1
            assert near(p[i],p[j]),"Warning: End of curve {} (location {}) does not correspond with beginning of curve {} (location {}) in Bezier profile.".format(i//4+1,p[i],j//4+1,p[j])

    def cubic(self):
        """Set the SOR type to be cubic."""
        self.set('SOR.type',"cubic")
        return self

    def getType(self):
        """Get the type of the SOR."""
        return self.get('SOR.type')

    def sturm(self):
        """Set the SOR to be sturm."""
        self.set('SOR.sturm',True)
        return self

    def getSturm(self):
        """Return true if this SOR is sturmian."""
        return self.get('SOR.sturm')

###############################################################################
# Spindle: a smoothly turned object
@checkdoc
class Spindle(SOR):
    """Spindle objects describe items that can be turned on a lathe.
    The cross sections of these objects are circular in one direction and
    polygonal or spline-shaped in the other."""

    def __init__(self,description="A spindle object."):
        super().__init__(description=description)

    def _POV_(self,context):
        if context.selects(self):
            outline = self.getProfile()
            t = self.getType()
            s = self.getSturm()
            prt('lathe {{ {}_spline {}\n'.format(t,len(outline)))
            for p in outline:
                prt(',<{},{}>'.format(p[0],p[1]))
            prt('\n')
            POV(super(),context)
            if s:
                prt(' sturm ')
            prt('}\n')

###############################################################################
# Prism: a turned object
@checkdoc
class Prism(SOR):
    """Prism objects describe items that can be turned on a lathe.
    The cross sections of these objects are regular polygons along y-axis and
    polygonal or spline-shaped in the other."""
    def __init__(self,description="A prism object."):
        super().__init__(description=description)
        self.xRot(-90) # orientation should be along +y

    def _POV_(self,context):
        if context.selects(self):
            outline = self.getProfile()
            t = self.getType()
            s = self.getSturm()
            prt('prism {{ {}_spline -50 50 {}\n'.format(t,len(outline)))
            for p in outline:
                prt(',<{},{}>'.format(p[0],p[1]))
            prt('\n')
            POV(super(),context)
            if s:
                prt(' sturm ')
            prt('}\n')

    

    
        
