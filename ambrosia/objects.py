#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
"""Low level ambrosia object hierarchy.

(c) 2013 duane a. bailey

This module implements many primitive ambrosia classes and is responsible
for defining most global object definitions.

Classes defined here:
  AmbrosiaObject - base class for all ambrosia objects.
   Transform     - class describing 3-space transformations
   Environment   - communication between ambrosia and the operating system
   POVWriter     - writer for dumping objects to POV format
   Transformable - object that can be moved/rotated/scaled/tagged
    Material     - POV-based materials: solids, metals, surface maps, etc.
    Primitive    - basis for transformable objects with attached materials
     CSG         - grouping class for constructive solid geometry
      Group      - additive/union-based grouping
      Intersection - intersection-based group
      Difference - grouping with annihilation
   Context       - a private class for managing walks through CSG objects
   Reference     - handle for general primitives
   Color         - internal representation of color

Global functions:
  translate, scale, xRot, yRot, zRot, xy/xz/yzMirror
  POV
  describe

Miscelaneous globals:
  environment, pov

Global materials:
  black/ltGray/gray/dkGray/white versions of Plaster/Plastic
  red/yellow/green/cyan/blue/magenta/purple versions of Plaster/Plastic
  mirrorMat, greenGlass
  identityXform
"""
import abc
import math
import os
from sys import stdout,setrecursionlimit,getrecursionlimit
from collections import Hashable
from itertools import count
from ambrosia.decorators import *
from ambrosia.basics import *

__all__ = ['AmbrosiaObject', 'blackPlaster', 'blackPlastic', 'bluePlaster', 'bluePlastic', 'Color', 'Context', 'CSG', 'cyanPlaster', 'cyanPlastic', 'defaultMaterial', 'describe', 'Difference', 'dkGrayPlaster', 'dkGrayPlastic', 'emptyMaterial', 'Environment', 'environment', 'grayPlaster', 'grayPlastic', 'greenGlass', 'greenPlaster', 'greenPlastic', 'Group', 'identity', 'Intersection', 'ltGrayPlaster', 'ltGrayPlastic', 'magentaPlaster', 'magentaPlastic', 'Material', 'mirrorMat', 'POV', 'pov', 'POVWriter', 'Primitive', 'prt', 'purplePlaster', 'purplePlastic', 'redPlaster', 'redPlastic', 'Reference', 'scale', 'Transform', 'Transformable', 'translate', 'whitePlaster', 'whitePlastic', 'xRot', 'xyMirror', 'xzMirror', 'yellowPlaster', 'yellowPlastic', 'yRot', 'yzMirror', 'zRot' ]


###############################################################################
# Ambrosia class tree root.
@checkdoc
class AmbrosiaObject(metaclass=abc.ABCMeta):
    """This class is the root of the ambrosia object hierarchy.

    These objects are never explicitly constructed.  Instead, they
    form the root class for all other objects found in ambrosia.

    All AmbrosiaObjects have the ability to save ambrosia-specific
    attributes.  The set and get methods allow one to access and
    modify these attributes.  For example, we might want to store
    the location of the top of a cube:
        cube = Cube().set("top",(0,50,0))
    Later, we can get this attribute with
        cube.get("top")
    
    One can see the attributes associated with any ambrosia object with
    the describe method:
        describe(cube)
    prints the attributes:
        ... ("top",(0,50,0)) ...
    """
    __slots__ = [ "_attrs" ]
    
    def __init__(self,description="An ambroisia object."):
        """Initialize object."""
        self._attrs = dict()
        self._attrs['object.name'] = type(self).__name__
        self._attrs['object.description'] = description
        
    def get(self,key):
        """Get attribute value."""
        return self._attrs.get(key,None)
    
    def set(self,key,value):
        """Set attribute value."""
        self._attrs[key] = value
        
    def description(self,d):
        """Provide a human readable description of object."""
        self.set('object.description',d)
        return self

    def getDescription(self):
        """Return human readable description of object."""
        if self.get('object.description') is None:
            print(self)
        return self.get('object.description')

    def name(self,n):
        """Provide a name for this object."""
        self.set('object.name',n)
        return self

    def getName(self):
        """Return a name for this object."""
        return self.get('object.name')

    def __str__(self):
        """Provide a human readable object state."""
        return "\n".join(sorted([str((k,self._attrs[k])) for k in self._attrs]))

    def copy(self):
        """Copy basic structure.  Subclasses are responsible for other state."""
        c = type(self)()
        c._attrs = self._attrs.copy()
        return c

    def __handle__(self,msg):
        """Handle message from subclass."""
        assert False,"Cannot handle msg: "+msg


###############################################################################
# The Transform class
@checkdoc
class Transform(AmbrosiaObject):
    """The encapsulation of a 3-space transform.

    This class describes the effects of zero or more translations, rotations,
    scales, and mirrors on target objects.  By default, the identity transform
    is created.  The methods scale, translate, xRot, yRot, zRot, xyMirror,
    xzMirror, and yzMirror each provide a means for mutating the state of the
    transform to include an additional transformation step.  For example,
        t.scale(3,3,3)
    will modify t in such a way that t has the additional effect of scaling
    by 3. (This appends the transform; the prepend method allows the insertion
    of a transform before the value, t.)

    The global routines xRot, translate, etc. are factory methods
    that produce objects that represent the transformion processes.  Thus
        t = xRot(90)
    is equivalent to
        t = Transform().xRot(90)
        
    The transform also keeps track of the history (a string) of the
    construction of the transformation.

    Transforms are useful for mapping points in one space into the transformed
    space.  This is typically accomplished by using the transform as a
    function:
        >>> t = translate(1,0,1)
        >>> t((0,0,0))
        (1,0,1)
    Passing a polygon as the parameter will transform each of the points of
    the polygon by the transformation; the result is a polygon.
    """
    def __init__(self,description="An ambrosia transform."):
        """Initialize transformation as identity."""
        super().__init__(description=description)
        self.reset()

    def reset(self):
        """Initialize the transform to the identity."""
        self.set('xform.history',[])
        self.set('xform.matrix',[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1])
        return self

    def __eq__(self,other):
        """Quick check to see if two transforms are the same."""
        t = self.getMatrix()
        ot = other.getMatrix()
        for i in range(16):
            if math.fabs(t[i] - ot[i]) > fuzz:
                return False
        return True

    def copy(self):
        """Copy transform."""
        result = super().copy()
        result.set('xform.history',result.getHistory().copy())
        result.set('xform.matrix',result.getMatrix().copy())
        return result

    def isIdentity(self):
        """Return true if this transform is the identity."""
        return self == identity

    def _appendHistory(self,t):
        """Append string to evaluation history."""
        self.get('xform.history').append(t)

    def __call__(self,value):
        if isinstance(value,tuple):
            return self.mapPoint(value)
        else:
            return self.mapPoly(value)

    def map(self,value):
        """Compute the action of the transformation on a value."""
        return self(value)

    def mapPoly(self,poly):
        """Compute the action of the transformation on a polygon."""
        return [ self.mapPoint(p) for p in poly ]

    def mapPoint(self,p):
        """Map a point, p, through this transformation."""
        typeCheck(p,({int,float},{int,float},{int,float}))
        t = self.getMatrix()
        p = list(p)
        p1 = p+[1]
        omega = dotProduct(t[3::4],p1)
        if near(omega,0):
            print("omega is 0.  matrix={}, p1={}".format(t,p1))
        return tuple(dotProduct(t[i::4],p1)/omega for i in range(3))

    def mapDirection(self,d):
        """Map a direction vector, d, using this transformation."""
        return vectorDifference(self.mapPoint(d),self.mapPoint((0,0,0)))

    def yzMirror(self):
        """Append an mirror transform through the y-z plane."""
        self._appendHistory('(yzMirror)')
        t = self.getMatrix()
        t[0::4] = [-v for v in t[0::4]]
        return self

    def xzMirror(self):
        """Append an mirror transform through the x-z plane."""
        self._appendHistory('(xzMirror)')
        t = self.getMatrix()
        t[1::4] = [-v for v in t[1::4]]
        return self

    def xyMirror(self):
        """Append an mirror transform through the x-y plane."""
        self._appendHistory('(xyMirror)')
        t = self.getMatrix()
        t[2::4] = [-v for v in t[2::4]]
        return self

    def xRot(self,angle):
        """Append an x-rotation through angle (degrees)."""
        self._appendHistory("xRot({})".format(angle))
        a = deg2rad(angle)
        c = math.cos(a)
        s = math.sin(a)
        t = self.getMatrix()
        t1 = t[1]
        t5 = t[5]
        t9 = t[9]
        t13 = t[13]
        t[1] = c*t1-s*t[2]
        t[2] = s*t1+c*t[2]
        t[5] = c*t5-s*t[6]
        t[6] = s*t5+c*t[6]
        t[9] = c*t9-s*t[10]
        t[10] = s*t9+c*t[10]
        t[13] = c*t13-s*t[14]
        t[14] = s*t13+c*t[14]
        return self

    def yRot(self,angle):
        """Append a y-rotation through angle (degrees)."""
        self._appendHistory("yRot({})".format(angle))
        a = deg2rad(angle)
        c = math.cos(a)
        s = math.sin(a)
        t = self.getMatrix()
        t0 = t[0]
        t4 = t[4]
        t8 = t[8]
        t12 = t[12]
        t[0] = c*t0+s*t[2]
        t[2] = c*t[2]-s*t0
        t[4] = c*t4+s*t[6]
        t[6] = c*t[6]-s*t4
        t[8] = c*t8+s*t[10]
        t[10] = c*t[10]-s*t8
        t[12] = c*t12+s*t[14]
        t[14] = c*t[14]-s*t12
        return self

    def zRot(self,angle):
        """Append a z-rotation through angle (degrees)."""
        self._appendHistory("zRot({})".format(angle))
        a = deg2rad(angle)
        c = math.cos(a)
        s = math.sin(a)
        t = self.getMatrix()
        t0 = t[0]
        t4 = t[4]
        t8 = t[8]
        t12 = t[12]
        t[0] = c*t0-s*t[1]
        t[1] = s*t0+c*t[1]
        t[4] = c*t4-s*t[5]
        t[5] = s*t4+c*t[5]
        t[8] = c*t8-s*t[9]
        t[9] = s*t8+c*t[9]
        t[12] = c*t12-s*t[13]
        t[13] = s*t12+c*t[13]
        return self

    def scale(self,*args):
        """Append a scaling transform, scaling dimensions by x,y, and z."""
        if len(args) == 3:
            (x,y,z) = args
            assert x*y*z != 0, "Warning: scale({},{},{}) includes zero scale.".format(x,y,z)
            self._appendHistory("scale({},{},{})".format(x,y,z))
        elif len(args) == 1:
            x = args[0]
            assert x != 0, "Warning: Scale by 0"
            y = x
            z = x
            self._appendHistory("scale({})".format(x))
        else:
            assert False,"Scale must have 1 or 3 parameters."
        t = self.getMatrix()
        t[0::4] = [x*v for v in t[0::4]]
        t[1::4] = [y*v for v in t[1::4]]
        t[2::4] = [z*v for v in t[2::4]]
        return self
    
    def translate(self,x,y,z):
        """Append a translation, moving space by x, y, and z."""
        self._appendHistory("translate({},{},{})".format(x,y,z))
        t = self.getMatrix()
        v3 = t[3]
        v7 = t[7]
        v11 = t[11]
        v15 = t[15]
        t[0] = v3*x+t[0]
        t[1] = v3*y+t[1]
        t[2] = v3*z+t[2]
        t[4] = v7*x+t[4]
        t[5] = v7*y+t[5]
        t[6] = v7*z+t[6]
        t[8] = v11*x+t[8]
        t[9] = v11*y+t[9]
        t[10] = v11*z+t[10]
        t[12] = v15*x+t[12]
        t[13] = v15*y+t[13]
        t[14] = v15*z+t[14]
        return self

    def getHistory(self):
        """Return transform history."""
        return self.get('xform.history')

    def getMatrix(self):
        """Return the transform array."""
        return self.get('xform.matrix')

    def __mul__(self,other):
        """Compose transformation with another transform."""
        ot = other.getMatrix()
        t = self.getMatrix()
        result = Transform()
        rt = result.getMatrix()
        for i in range(16):
            rt[i] = dotProduct(t[i-i%4:i+4-i%4:1],ot[i%4::4])
        return result

    def __imul__(self,other):
        """Update this transform by following it with other."""
        self.getHistory().extend(other.getHistory())
        new = self*other
        self.set('xform.matrix',new.getMatrix())
        return self

    def append(self,other):
        """Update this transform by following it with other."""
        self *= other

    def prepend(self,other):
        """Update this transform by preceding it with other."""
        self.set('xform.history',other.getHistory()+self.getHistory())
        new = other*self
        self.set('xform.matrix',new.getMatrix())
        return self

    def normalize(self):
        """Normalize the transformation (forces t[3][3] to 1)."""
        t = self.getMatrix()
        omega = t[15]
        assert omega
        if omega != 1:
            for i in range(16):
                t[i] /= omega
        return self

    def _POV_(self,context):
        """Print POV equivalent."""
        pov.writeXform(self.getMatrix(),prefix="matrix")


###############################################################################
# Environment objects
@checkdoc
class Environment(AmbrosiaObject):
    """Objects that support communication with the operating system.

    Typically, you do not create new environments.  Instead, you use the
    Environment referenced by the 'environment' reference.

    The envioronment keeps track of communication link to the renderer.
    Currently, this is managed by a "writer".  See writer/getWriter.

    For complex projects (like movies) it's important to set the image
    folder -- the folder where material images are found, as well as the
    project folder -- the folder where intermediate files are written.
    For example, the intermediate frames of a movie are stored in the 
    project folder.
    """
    
    def __init__(self,description="A rendering environment."):
        """Initialize the environment."""
        super().__init__(description=description)
        self.set('environment.imageFolder','images')
        self.set('environment.projectFolder','images')
        self.set('environment.libraryPath',[])

    def __copy__(self):
        """Create an identical copy of this environment."""
        return super().copy()

    def writer(self,w):
        """Set the current writer."""
        self.set('environment.writer',w)

    def getWriter(self):
        """Get the current writer."""
        return self.get('environment.writer')
    
    def imageFolder(self,f):
        """Set the image folder location."""
        if f[:1] == '~':
            f = os.getenv('HOME')+f[1:]
        self.set('environment.imageFolder',f)
        return self

    def getImageFolder(self):
        """Get the location of where images are stored."""
        return self.get('environment.imageFolder')

    def projectFolder(self,f):
        """Set the folder for holding project files."""
        self.set('environment.projectFolder',f)
        return self

    def getProjectFolder(self):
        """Get the name of the folder containing project files."""
        return self.get('environment.projectFolder')

    def libraryFolder(self,f):
        """Construct the library folder path."""
        self.get('environment.libraryPath').append(f)

    def getLibraryPath(self):
        """Return a list of library folders."""
        return self.get('environment.libraryPath')

    def makeImagePath(self,f=None):
        """Construct the name of an image, based on environment.
        If the filename starts with /, it is used, as is.
        otherwise, it is prepended by the imageFolder.
        if the image folder begins with a /, it is used as-is, otherwise
        it is prepended with the current directory.
        """
        file = [ f or "untitled.png" ]
        absolute = file[0][:1] == '/'
        folder = [] if absolute else [ self.getImageFolder() ]
        absolute = absolute or (folder[0][:1] == '/')
        here = [] if absolute else [ os.getcwd() or "/tmp" ]
        return '/'.join(here+folder+file)

    def recursionLimit(self,n=1000):
        result = self.getRecursionLimit()
        setrecursionlimit(n)
        return result

    def getRecursionLimit(self):
        return getrecursionlimit()

    def _POV_(self,context):
        """Print environment for POV."""
        p = self.getLibraryPath().copy()
        while p:
            print('Library_Path="{}"'.format(p.pop()))

# Global 'environment'
environment = Environment(description="Default ambrosia environment.")

@checkdoc
class POVWriter(AmbrosiaObject):
    __slots__ = ["_outputFile"]
    
    def __init__(self,description="A POV writing assistant."):
        super().__init__(description=description)
        self._outputFile = None

    def open(self,filename):
        """Open file for output to hold POV model or init file."""
        self._outputFile = open(filename,"wt")
#        prt('#version 3.6;\n')
#        prt('global_settings {assumed_gamma 1.0}\n')

    def close(self):
        """Close previously opened POV file."""
        if self._outputFile:
            self._outputFile.close()
        self._outputFile = None

    def getOutputFile(self):
        """Return the output file used with POV."""
        return self._outputFile

    def writePoint(self,p):
        """Write a (2 or 3d) point to POV output file."""
        l = [str(x) for x in p]
        prt("<{}>".format(",".join(l)))

    def writeXform(self,x,prefix=None):
        """Print POV represenation of a transform."""
        prt("{} <{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}> ".format(prefix if not None else "" ,*[x[i] for i in [0,1,2,4,5,6,8,9,10,12,13,14]]))

    def writeColor(self,c):
        """Write a color in a standard way to POV output file."""
        l = len(c)
        if l==0:
            prt("color rgb <0.5,0.5,0.5>")
        elif l < 3:
            prt("color rgb <{},{},{}>".format(c[0],c[0],c[0]))
        elif l == 3:
            prt("color rgb <{},{},{}>".format(c[0],c[1],c[2]))
        elif l == 4:
            prt("color rgb <{},{},{},{}>".format(c[0],c[1],c[2],1-c[3]))
        else:
            prt("color rgb <{},{},{},{},{}>".format(c[0],c[1],c[2],1-c[3],c[4]))
            

###############################################################################
# The Transformable class
#
@checkdoc
class Transformable(AmbrosiaObject):
    """This class describes all ambrosia objects that can be transformed."""
    
    def __init__(self,description="A transformable object."):
        """Initialize a Transformable object."""
        super().__init__(description=description)
        self.set('xformable.xform',Transform())
        self.set('xformable.centroid',origin)
        self.set('xformable.tags',set())
        self.set('xformable.handles',dict())

    def getTags(self):
        """Return tag set."""
        return self.get('xformable.tags')

    def tags(self,tl):
        """Replace tags from iterable."""
        self.set('xformable.tags',set(tl))
        return self

    def tag(self,*items):
        """Mix in new tags."""
        self.getTags().update(items)
        return self
    
    def hasTag(self,tag):
        """Check for specific tag."""
        return tag in self.getTags()

    def untag(self,tag):
        """Remove a tag from the tag set."""
        self.getTags().discard(tag)
        return self

    def handle(self,name,pt):
        """Identify a location with a name."""
        l = self.get('xformable.handles')
        assert(isinstance(name,str))
        assert(len(pt) == 3)
        l[name] = pt
        return self

    def getHandle(self,name):
        """Get the location associated with name."""
        assert(isinstance(name,str))
        l = self.get('xformable.handles')
        if name in l:
            return self.getXform().mapPoint(l[name])
        else:
            return None

    def getHandles(self,name):
        """Get a list of all handles with a particular name."""
        assert(isinstance(name,str))
        l = self.get('xformable.handles')
        if name in l:
            return [(self.getName(),self.getXform().mapPoint(l[name]))]
        else:
            return []
    
    def getXform(self):
        """Return the transform associated with this object."""
        return self.get('xformable.xform')

    def xform(self,t):
        """Set the transform to t."""
        self.set('xformable.xform',t.copy())

    def absoluteXform(self,t):
        """Reset the transform to t."""
        self.xform(t)

    def relativeXform(self,t):
        """Reset the transform to t."""
        self.getXform().suffixWith(t)

#     def getCentroid(self):
#         """Return the center of this object's mass."""
#         return self.get('xformable.centroid')

#     def centroid(self, p):
#         """Set the center of mass for this object."""
#         self.set('xformable.centroid',p)
#         return self

    def translate(self,x,y,z):
        """Translate object origin to (x,y,z)."""
        self.getXform().translate(x,y,z)
        return self

    def xRot(self,angle):
        """Rotate object about x axis."""
        self.getXform().xRot(angle)
        return self

    def yRot(self,angle):
        """Rotate object about y axis."""
        self.getXform().yRot(angle)
        return self

    def zRot(self,angle):
        """Rotate object about z axis."""
        self.getXform().zRot(angle)
        return self
    
    def scale(self,*args):
        """Scale an object by xs along x axis, etc."""
        if len(args) == 3:
            (x,y,z) = args
            assert x*y*z != 0, "Warning: scale({},{},{}) includes zero scale.".format(x,y,z)
        elif len(args) == 1:
            x = args[0]
            assert x != 0, "Warning: Scale by 0"
            y = x
            z = x
        else:
            assert False,"Scale must have 1 or 3 parameters."
        self.getXform().scale(x,y,z)
        return self
    
    def xyMirror(self):
        """Mirror in x-y plane."""
        self.getXform().xyMirror()
        return self

    def xzMirror(self):
        """Mirror in x-z plane."""
        self.getXform().xzMirror()
        return self

    def yzMirror(self):
        """Mirror in y-z plane."""
        self.getXform().yzMirror()
        return self

    def __handle__(self,msg):
        """Handle transform- or material-setting message."""
        if isinstance(msg,Transform):
            self.getXform().append(msg)
        elif isinstance(msg,str):
            self.tag(msg)
        else:
            super().__handle__(msg)

    def _POV_(self,context):
        context.pushXform(self.getXform())
        context.pushTags(self.getTags())
        context.getTotalXform()._POV_(context)
        if self.getTags():
            print("// tags: {}".format(context.getMergedTags()))
        context.popTags()
        context.popXform()

###############################################################################
# Primitive ambrosia objects.  These objects have materials
@checkdoc
class Primitive(Transformable):
    """Primitive objects are Transformable and can have materials associated
    with them."""
    
    def __init__(self,description="A primitive object."):
        """Initialize the the Primitive object."""
        super().__init__(description=description)
        self.set('primitive.material',emptyMaterial)

    def copy(self):
        """Make a copy of this Primitive."""
        return super().copy()

    def getMaterial(self):
        """Return the associated material, or None."""
        return self.get('primitive.material')

    def material(self,m):
        """Set the material associated with is Primitive."""
        self.set('primitive.material',m)
        return self


    def __handle__(self,msg):
        """Handle transform- or material-setting message."""
        if isinstance(msg,Material):
            self.material(msg)
        else:
            super().__handle__(msg)

    def _POV_primitive(self,context):
        """Print POV version of this Primitive."""
        context.pushMaterial(self.getMaterial())
        POV(context.getMergedMaterial(),context)
        context.popMaterial()
        POV(super(),context)

    def _POV_(self,context):
        """Print POV version of this Primitive."""
        self._POV_primitive(context)

###############################################################################
# The Context class: a graphics context for ambrosia objects.
@checkdoc
class Context(AmbrosiaObject):
    """This class provides a nested graphics context for ambrosia objects."""
    
    __slots__ = [ "_materialStack", "_transformStack", "_tagStack" ]
    def __init__(self,description="A graphics context."):
        super().__init__(description=description)
        self._materialStack = [[defaultMaterial,defaultMaterial]]
        t = Transform()
        self._transformStack = [[t,t]]
        s = set()
        self._tagStack = [[s,s]]
        self.verboseGrouping(False)

    def getXform(self):
        """Return current transform."""
        return self._transformStack[-1][0]

    def getTotalXform(self):
        """Return accumulated transform."""
        return self._transformStack[-1][1]

    def getMaterial(self):
        """Return current material."""
        return self._materialStack[-1][0]

    def getMergedMaterial(self):
        """Return material with all material properties."""
        return self._materialStack[-1][1]

    def getTags(self):
        """Return current tag set."""
        return self._tagStack[-1][0]

    def getMergedTags(self):
        """Return merged tag set."""
        return self._tagStack[-1][1]

    def getSelectionPredicate(self):
        """Return current selection predicate."""
        return self.get('selectionPredicate')

    def selectionPredicate(self):
        """Set selection predicate to f."""
        self.set('context.selectionPredicate',f)

    def selects(self,object):
        """Return True if the selection predicate would select object."""
        f = self.get('context.selectionPredicate')
        if f is None:
            return True
        else:
            return f(object)

    def getVerboseGrouping(self):
        """Return True if grouping should be explicit in POV file."""
        return self.get('context.verboseGrouping')

    def verboseGrouping(self,bool):
        """Turn on explicit grouping."""
        self.set('context.verboseGrouping',bool)
        return self
    
    def pushXform(self,t):
        """Add a new transform to the transform stack."""
        newTotal = t*self.getTotalXform()
        self._transformStack.append([t,newTotal])
        return self

    def popXform(self):
        """Remove last transform from stack."""
        self._transformStack.pop()

    def pushMaterial(self,m):
        """Add a new material to the material stack."""
        newMat = m.mergeWith(self.getMergedMaterial())
        self._materialStack.append([m,newMat])
        return self

    def popMaterial(self):
        """Remove last material from stack."""
        self._materialStack.pop()

    def pushTags(self,t):
        """Add a new tag set to the tag stack."""
        newTags = t.union(self.getMergedTags())
        self._tagStack.append([t,newTags])
        return self

    def popTags(self):
        """Remove last tagset from stack."""
        self._tagStack.pop()

    def mapPoint(self,p):
        """Map point according to the current context."""
        return self.getTotalXform().mapPoint(p)

    def mapDirection(self,p):
        """Map direction vector according to the current context."""
        return self.getTotalXform().mapDirection(p)

    def _POV_(self):
        pass

###############################################################################
# The Reference object
@checkdoc
class Reference(Primitive):
    """Reference objects provide a means to assign transformations or
    materials to one of several instances of a single objects."""

    def __init__(self,object=None,description="An ambrosia object reference."):
        """Create a reference to an object."""
        super().__init__(description=description)
        self.object(object)
    
    def getObject(self):
        """Return the object of this reference."""
        return self.get('reference.target')

    def object(self,o):
        """The object of this reference."""
        self.set('reference.target',o)
        if o is not None:
            self.description("A reference to: "+o.getDescription())

    def getHandle(self,name):
        result = super().getHandle(name)
        if result is not None:
            return result
        else:
            result = self.getObject().getHandle(name)
            if result is not None:
                return self.getXform().mapPoint(result)
            else:
                return None

    def getHandles(self,name):
        result = super().getHandles(name)
        x = self.getXform()
        n = self.getName()+'.'
        result.extend([(n+where,x.mapPoint(p)) for (where,p) in self.getObject().getHandles(name)])
        return result

    def _POV_(self,context):
        context.pushXform(self.getXform())
        context.pushMaterial(self.getMaterial())
        context.pushTags(self.getTags())
        self.getObject()._POV_(context)
        context.popTags()
        context.popMaterial()
        context.popXform()

###############################################################################
# Basis for CSG objects
@checkdoc
class CSG(Primitive):
    """This is the main grouping mechanism."""
    def __init__(self,description="A group object."):
        super().__init__(description=description)
        self.set('csg.references',[])
        self._action("union")

    def _action(self,a):
        """The type of CSG action."""
        self.set('csg.action',a)

    def getReferences(self):
        """Return a list of references in the CSG object."""
        return self.get('csg.references')

    def add(self,target,*msgs):
        """Add a new object to the group."""
        typeCheck(target,Transformable)
        r = Reference(target)
        for m in msgs:
            typeCheck(m,{Transform,Material})
            r.__handle__(m)
        self.getReferences().append(r)
        return self

    def clear(self):
        """Remove all objects from CSG group."""
        self.getReferences().clear()
        return self

    def getHandle(self,name):
        result = super().getHandle(name)
        if result is not None:
            return result
        for r in self.getReferences():
            result = r.getHandle(name)
            if result is not None:
                return self.getXform().mapPoint(result)
        return None

    def getHandles(self,name):
        result = super().getHandles(name)
        x = self.getXform()
        n = self.getName()
        for (i,r) in zip(count(),self.getReferences()):
            nm = "{}[{}].".format(n,i)
            result.extend([(nm+where,x.mapPoint(p)) for (where,p) in r.getHandles(name)])
        return result

    def __getitem__(self,item):
        """Return the ith reference."""
        return self.getReferences()[item]

    def __len__(self):
        """Return number of references in object."""
        return len(self.getReferences())

    def __iter__(self):
        """Iterate across CSG object."""
        return iter(self.getReferences())

    def _POV_(self,context):
        """Write POV description of this group object."""
        refs = self.get('csg.references')
        action = self.get('csg.action')
        t = self.getXform()
        m = self.getMaterial()
        g = self.getTags()
        vg = context.getVerboseGrouping()
        context.verboseGrouping(True)
        context.pushMaterial(m)
        context.pushXform(t)
        context.pushTags(g)
        if vg:
            prt("{} {{".format(action))
        for o in refs:
            o._POV_(context)
        if vg:
            prt("}")
        context.popTags()
        context.popXform()
        context.popMaterial()
        context.verboseGrouping(vg)

###############################################################################
# A Group container object.
@checkdoc
class Group(CSG):
    """This is the main grouping structure in ambrosia."""
    def __init__(self,description="A group object."):
        super().__init__(description=description)
        self._action("union")
        
@checkdoc
class Intersection(CSG):
    """This is the main grouping structure in ambrosia."""
    def __init__(self,description="A group object."):
        super().__init__(description=description)
        self._action("intersection")

@checkdoc
class Difference(CSG):
    """This is the main grouping structure in ambrosia."""
    def __init__(self,description="A group object."):
        super().__init__(description=description)
        self._action("difference")

# Global "pov"
def POV(obj,context=None):
    """Utility routine for dumping POV with optional context."""
    if context is None:
        context = Context()
    obj._POV_(context)

pov = POVWriter("The global POV writer.")
environment.writer(pov)
def prt(v):
    """Basic print method w/o newline."""
    of = environment.getWriter().getOutputFile() or stdout
    print(v,end="",file=of)

###############################################################################
# Global message sourcing primitives
def describe(object):
    object.describe()

def translate(x,y,z):
    t = Transform()
    return t.translate(x,y,z)

def scale(*args):
    if len(args) == 3:
        (x,y,z) = args
        assert x*y*z != 0, "Warning: scale({},{},{}) includes zero scale.".format(x,y,z)
    elif len(args) == 1:
        x = args[0]
        assert x != 0, "Warning: Scale by 0"
        y = x
        z = x
    else:
        assert False,"Scale must have 1 or 3 parameters."
    return Transform().scale(x,y,z)

def xRot(angle):
    t = Transform()
    return t.xRot(angle)

def yRot(angle):
    t = Transform()
    return t.yRot(angle)

def zRot(angle):
    t = Transform()
    return t.zRot(angle)

def xyMirror():
    t = Transform()
    return t.xyMirror()

def yzMirror():
    t = Transform()
    return t.yzMirror()

def xzMirror():
    t = Transform()
    return t.xzMirror()

def product(*xforms):
    t = Transform()
    for x in xforms:
        t *= x
    return t

###############################################################################
# Color: internal representation of colors
@checkdoc
class Color(AmbrosiaObject):
    """This class is used, internally, to represent colors."""
    __slots__ = [ "_red", "_green", "_blue", "_alpha", "_filter" ]
    
    def __init__(self,color=None,description="A color."):
        super().__init__(description = description)
        self.color([1,1,1,1,0] if color is None else color)

    @classmethod
    def wrap(cls,base):
        """Construct a color from base, or use base if it is a Color."""
        if isinstance(base,Color):
            return base
        else:
            return Color(base)

    def getColor(self):
        """Get the full color specification."""
        return self.getRGBAF

    def color(self,l):
        """Set the individual color parameters."""
        self._red,self._green,self._blue = l[:3]
        self._alpha = l[3] if len(l) > 3 else 1
        self._filter = l[4] if len(l) > 4 else 0
        return self

    def getRed(self):
        """Get red component."""
        return self._red

    def red(self,v):
        """Set red component."""
        self._red = v
        return self

    def getGreen(self):
        """Get green component."""
        return self._green

    def green(self,v):
        """Set green component."""
        self._green = v
        return self

    def getBlue(self):
        """Get blue component."""
        return self._blue

    def blue(self,v):
        """Set blue component."""
        self._blue = v
        return self

    def getAlpha(self):
        """Get alpha component."""
        return self._alpha

    def alpha(self,v):
        """Set alpha component."""
        self._alpha = v
        return self

    def getTransmit(self):
        """Get the transmissiveness."""
        return 1-self._alpha

    def transmit(self,t):
        """Set the transmissiveness."""
        self._alpha = (1-t)
        return self

    def getFilter(self):
        """Get filter component."""
        return self._filter

    def filter(self,v):
        """Set filter component."""
        self._filter = v
        return self

    def getRGB(self):
        """Get 3-tuple of red, green, and blue values."""
        return [self._red,self._green,self._blue]

    def getRGBA(self):
        """Get 4-tuple of red, green, blue, and alpha values."""
        return [self._red,self._green,self._blue,self._alpha]

    def getRGBAF(self):
        """Get 5-tuple of red, green, blue, alpha, and filter values."""
        return [self._red,self._green,self._blue,self._alpha,self._filter]

    def copy(self):
        """Create a copy of this object."""
        return super().copy()

    def _POV_(self,contextIgnored=None):
        prt("rgbft <{},{},{},{},{}>".format(self.getRed(),self.getGreen(),self.getBlue(),self.getTransmit(),self.getFilter()))

###############################################################################
# Materials
#
@checkdoc
class Material(Transformable):
    """Representation of materials.  This particular implementation is
    biased toward materials that are found in POV."""
    def __init__(self,description="A material."):
        """Initialize material."""
        super().__init__(description=description)
        self.imageType("png")
        self.scale(100)
        self.translate(-50,-50,-50)
    
    def type(self,t):
        """Shorthand for setting values for materials."""
        if t == "plastic":
            self.ambient(0.1).diffuse(0.5).roughness(0.05).specularity(0.7)
        elif t == "plaster":
            self.ambient(0.2).diffuse(0.9).roughness(1).specularity(0)
        elif t == "mirror":
            self.ambient(0).diffuse(0.1).reflection(0.9)
        elif t == "glass":
            self.ambient(0).diffuse(0.1).transparency(0.8).refraction(1.5)
        else:
            assert(False)
        return self

    def getImageType(self):
        """Get the imageType value associated with the material."""
        return self.get('material.imageType')

    def imageType(self,v):
        """Set the imageType value associated with the material."""
        self.set('material.imageType',v)
        return self

    def pattern(self,t,*l):
        """Set pattern, with optional colors."""
        self.set('material.pattern',t)
        if len(l) == 1:
            self.color(l[0])
        else:
            self.colors(l)
        return self

    def brickPattern(self,brickColor,mortarColor):
        """Brick pattern requires two colors."""
        self.pattern("brick",brickColor,mortarColor)
        return self

    def checkerPattern(self,c0,c1):
        """Checker pattern requires two colors."""
        self.pattern("checker",c0,c1)
        return self

    def hexagonPattern(self,c0,c1,c2):
        """Hexagon pattern requires 3 colors."""
        self.pattern("hexagon",c0,c1,c2)
        return self

    def radialPattern(self,radius,c0,c1,*cn):
        """Set radial pattern; requires radius and two colors."""
        self.pattern("radial",c0,c1,*cn)
        self.frequency(radius)
        return self

    def getFrequency(self):
        """Get frequency (or radius)."""
        return self.get('material.pattern_frq')

    def frequency(self,v):
        """Set frequency (or, for radial, radius) of pattern to v."""
        self.set('material.pattern_frq',v)
        return self

    def gradientPattern(self,c0,c1,*others):
        """Gradient pattern requires two colors."""
        self.pattern("gradient",c0,c1,*others)
        return self

    def granitePattern(self,c0,c1,*others):
        """Granite patterns require two colors."""
        self.pattern("granite",c0,c1,*others)
        return self

    def cracklePattern(self,c0,c1,*others):
        """Crackle pattern requires two colors."""
        self.pattern("crackle",c0,c1,*others)
        return self

    def marblePattern(self,c0,c1,others):
        """Marble requires two colors; turbulence defaults to .6."""
        self.pattern("marble",first,second,*others)
        if self.turbulence is None:
            self.turbulence(0.6)
        return self

    def getTurbulence(self):
        """Get marble turbulence."""
        return self.get('material.turbulence') # defaults to None if not set
    
    def turbulence(self,v):
        """Set marble turbulence."""
        self.set('material.turbulence',v)
        return self

    def solid(self,c):
        """Set material to solid color."""
        self.color(c)
        return self

    def grainImage(self,img):
        """Use image as cross grain pattern."""
        self.image(img)
        self.pattern("grain")
        return self

    def grainPattern(self, i, c0, c1, *others):
        """Use colored monochrome image as cross grain pattern."""
        self.image(i)
        self.pattern("grainPattern",c0,c1,*others)
        return self

    def getImage(self):
        """Return image associated with pattern."""
        return self.get('material.image')

    def image(self,v):
        """Set image associated with pattern."""
        self.set('material.image',v)
        # assert fileExists(environment.makeFilePath(v)), "Warning: Material's image file, {}, not found in images folder.".format(v)
        return self

    def surfaceImage(self, i):
        """Map image onto the surface of object."""
        self.image(i)
        self.pattern("surface")
        self.UVMapped(True)
        return self

    def getPattern(self):
        """Get pattern type."""
        return self.get('material.pattern')

    def getUVMapped(self):
        """Get whether pattern is UV mapped."""
        return self.get('material.UVMapped')
    
    def UVMapped(self,v):
        """Set whether pattern is UV mapped."""
        self.set('material.UVMapped',v)
        return self
    
    def getColor(self):
        """Get the color of the material."""
        return self.get('material.color')

    def color(self,c):
        """Set the color of the material."""
        self.set('material.color',Color.wrap(c))
        return self

    def getColors(self):
        """Get the multiple colors associated with the matieral."""
        return self.get('material.colors')

    def colors(self,cl):
        """Set the multiple colors of the material."""
        self.set('material.colors',[Color.wrap(c) for c in cl])
        return self

    def getTransparency(self):
        """Get transparency associated with this material."""
        return self.get('material.transparency')

    def transparency(self,v):
        """Set the transparency associated with this material."""
        self.set('material.transparency',v)
        return self

    def getImageType(self):
        """Get image type associated with this material."""
        return self.get('material.imageType')

    def imageType(self,v):
        """Set the image type associated with this material."""
        self.set('material.imageType',v)
        return self

    # these items all have to do with the "finish" of the material.
    def getPhong(self):
        """Get the phong value associated with the material."""
        return self.get('material.phong')

    def phong(self,v):
        """Set the phong value associated with the material."""
        self.set('material.phong',v)
        return self

    def getAmbient(self):
        """Get the ambient value associated with the material."""
        return self.get('material.ambient')

    def ambient(self,v):
        """Set the ambient value associated with the material."""
        self.set('material.ambient',v)
        return self

    def getDiffuse(self):
        """Get the diffuse value associated with the material."""
        return self.get('material.diffuse')

    def diffuse(self,v):
        """Set the diffuse value associated with the material."""
        self.set('material.diffuse',v)
        return self

    def getSpecularity(self):
        """Get the specularity value associated with the material."""
        return self.get('material.specularity')

    def specularity(self,v):
        """Set the specularity value associated with the material."""
        self.set('material.specularity',v)
        return self

    def getRoughness(self):
        """Get the roughness value associated with the material."""
        return self.get('material.roughness')

    def roughness(self,v):
        """Set the roughness value associated with the material."""
        if v <= 0:
            print("Warning: Material roughness set to 0.05 instead of {}.".format(v))
            v = 0.05
        self.set('material.roughness',v)
        return self

    def getRefraction(self):
        """Get the refraction value associated with the material."""
        return self.get('material.refraction')

    def refraction(self,v):
        """Set the refraction value associated with the material."""
        self.set('material.refraction',v)
        return self

    def getCaustics(self):
        """Get the caustics value associated with the material."""
        return self.get('material.caustics')

    def caustics(self,v):
        """Set the caustics value associated with the material."""
        self.set('material.caustics',v)
        return self

    def getFadeDistance(self):
        """Get the fadeDistance value associated with the material."""
        return self.get('material.fadeDistance')

    def fadeDistance(self,v):
        """Set the fadeDistance value associated with the material."""
        self.set('material.fadeDistance',v)
        return self

    def getFadePower(self):
        """Get the fadePower value associated with the material."""
        return self.get('material.fadePower')

    def fadePower(self,v):
        """Set the fadePower value associated with the material."""
        self.set('material.fadePower',v)
        return self

    def getReflection(self):
        """Get the reflection value associated with the material."""
        return self.get('material.reflection')

    def reflection(self,v):
        """Set the reflection value associated with the material."""
        self.set('material.reflection',v)
        return self

    def getMetallic(self):
        """Get the metallic value associated with the material."""
        return self.get('material.metallic')

    def metallic(self,v):
        """Set the metallic value associated with the material."""
        self.set('material.metallic',v)
        return self

    def mergeWith(self,m):
        """New material with material's attributes, m providing missing values."""
        nm = Material()
        nm._attrs = m._attrs.copy()
        nm._attrs.update(self._attrs)
        return nm

    def _POV_turbulence(self,contextIgnored=None):
        prt(" wrp{{turbulence {}}}".format(self.getTurbulence()))

    def _POV_colors(self,cl):
        for c in cl:
            _POV_(c,None)

    def _POV_colorMap(self,m):
        prt(" color_map {")
        n = len(m)-1
        for (i,c) in zip(range(n+1),m):
            prt("[{} ".format(i/n))
            POV(c,False)
            prt("]")
        prt("}")
                
    def _POV_pigment(self):
        prt("pigment{")
        if self.getUVMapped():
            prt("uv_mapping ")
        pattern = self.getPattern()
        if pattern in ['grain','surface']:
            prt('image_map{{{} "{}"'.format(self.getImageType(),environment.makeImagePath(self.getImage())))
            if self.getTransparency() is not None:
                prt(' transmit all {}'.format(self.getTransparency()))
            prt('}')
        elif pattern in ['radial']:
            prt('radial frequency {} '.format(self.getFrequency()))
            self._POV_colorMap(self.getColors())
        elif pattern in ['grainPattern']:
            prt('image_pattern{{{} "{}"'.format(self.getImageType(),environment.makeImagePath(self.getImage())))
            # if self.getOneShot(): prt(" once")
            prt("}")
            self._POV_colorMap(self.getColors())
        elif pattern in ['checker','brick','hexagon']:
            prt("{} ".format(pattern))
            self._POV_colors(self.getColors())
        elif pattern in ['gradient']:
            prt("gradient x ")
            self._POV_colorMap(self.getColors())
        elif pattern in ['granite','crackle','marble']:
            prt("{} ".format(pattern))
            self._POV_colorMap(self.getColors())
        else:
            prt("color ")
            c = self.getColor()
            c._POV_()
            if (self.getTransparency()) and (0 == c.getTransmit()):
                prt(" transmit {}".format(self.getTransparency()))
        if self.getTurbulence():
            self._POV_turbulence(self.getTurbulence())
        prt("}")

    def _POV_finish(self):
        a = self.getAmbient()
        p = self.getPhong()
        df = self.getDiffuse()
        sp = self.getSpecularity()
        r = self.getRoughness()
        rf = self.getReflection()
        mt = self.getMetallic()
        if a or df or sp or rf or mt or p:
            prt("finish {")
            if a:
                prt(" ambient {}".format(a))
            if df:
                prt(" diffuse {}".format(df))
            if sp:
                prt(" specular {}".format(sp))
            if r:
                prt(" roughness {}".format(r))
            if rf or mt:
                prt(" reflection {")
                if rf:
                    prt(rf)
                if mt:
                    prt(" metallic")
                prt("}")
            if p:
                prt(" phong {}".format(p))
            prt("} ")

    def _POV_interior(self):
        ior = self.getRefraction()
        cau = self.getCaustics()
        fd = self.getFadeDistance()
        fp = self.getFadePower()
        if ior or cau or fd or fp:
            prt("interior { ")
            if ior:
                prt(" ior {}".format(ior))
            if cau:
                prt(" caustics {}".format(cau))
            if fd:
                prt(" fade_distance {}".format(fd))
            if fp:
                prt(" fade_power {}".format(fp))
            prt("}")
    
    def _POV_(self,contextIgnored=None):
        prt("texture{")
        self._POV_pigment()
        self._POV_finish()
        self.getXform()._POV_(None)
        prt("}")
        self._POV_interior()

###############################################################################
# Unique global objects

def _testTransform():
    """Basic tests of sanity for Transforms.

    >>> t = Transform()
    >>> t.isIdentity()
    True
    >>> p = (1, 2, 3)
    >>> print(t.mapPoint(p))
    [1.0, 2.0, 3.0]
    >>> s = t.copy()
    >>> t.translate(1,0,0).isIdentity()
    False
    >>> s.isIdentity()
    True
    >>> print(t.mapPoint(p))
    [2.0, 2.0, 3.0]
    >>> print(t.xRot(90).mapPoint(p))
    [2.0, -3.0, 2.0]
    >>> print(t.reset().yRot(90).getHistory())
    ['yRot(90)']
    >>> near(t.mapPoint(p),[3,2,-1])
    True
    >>> t.zRot(90)
    <__main__.Transform object at 0x...>
    >>> near(t.mapPoint(p),[-2,3,-1])
    True
    >>> t.reset().scale(2,3,4)
    <__main__.Transform object at 0x...>
    >>> near(t.mapPoint(p),[2,6,12])
    True
    """

def _testTransformable():
    """Tests for Tranformable objects.

    >>> t = Transformable()
    >>> t
    <__main__.Transformable object at 0x...>
    >>> t.getXform()
    <__main__.Transform object at 0x...>
    >>> t.getXform().isIdentity()
    True
    >>> t.translate(1,2,3)
    <__main__.Transformable object at 0x...>
    >>> t.getXform().isIdentity()
    False
    >>> t.getTags()
    set()
    >>> t.tag(3)
    <__main__.Transformable object at 0x...>
    >>> t.getTags()
    {3}
    >>> t.untag(5)
    <__main__.Transformable object at 0x...>
    >>> t.getTags()
    {3}
    >>> t.untag(3)
    <__main__.Transformable object at 0x...>
    >>> t.getTags()
    set()
    """

###############################################################################
# BUILTINS:

emptyMaterial = Material()
defaultMaterial = Material().color(gray)

blackPlaster = Material().type("plaster").color(black)
blackPlastic = Material().type("plastic").color(black)
dkGrayPlaster = Material().type("plaster").color(dkGray)
dkGrayPlastic = Material().type("plastic").color(dkGray)
grayPlaster = Material().type("plaster").color(gray)
grayPlastic = Material().type("plastic").color(gray)
ltGrayPlaster = Material().type("plaster").color(ltGray)
ltGrayPlastic = Material().type("plastic").color(ltGray)
whitePlaster = Material().type("plaster").color(white)
whitePlastic = Material().type("plastic").color(white)
redPlaster = Material().type("plaster").color(red)
redPlastic = Material().type("plastic").color(red)
yellowPlaster = Material().type("plaster").color(yellow)
yellowPlastic = Material().type("plastic").color(yellow)
greenPlaster = Material().type("plaster").color(green)
greenPlastic = Material().type("plastic").color(green)
cyanPlaster = Material().type("plaster").color(cyan)
cyanPlastic = Material().type("plastic").color(cyan)
bluePlaster = Material().type("plaster").color(blue)
bluePlastic = Material().type("plastic").color(blue)
magentaPlaster = Material().type("plaster").color(magenta)
magentaPlastic = Material().type("plastic").color(magenta)
purplePlaster = Material().type("plaster").color(purple)
purplePlastic = Material().type("plastic").color(purple)

mirrorMat = Material().type("mirror").color(gray)
greenGlass = Material().type("glass").color(green)

identity = Transform()
