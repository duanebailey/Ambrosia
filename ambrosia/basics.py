#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
#
"""Primitive mathematical definitions for ambrosia.

This module contains primitives that make ambrosia possible.  Many of these
primitives are used internally by ambrosia, but modelers may find these
definitions useful, as well.

Methods defined here fall into the following categories:
 ownership and versioning:
    ambrosiaVersion, ambrosiaCopyright

 type checking:
    typecheck

 geometric compuations:
    dotProduct, vectorLength, vectorScale, crossProduct, normalize,
    vectorDifference, vectorSum, last

 conversion:
    deg2rad, rad2deg
    hsv2rgb, rgb2hsv

 basic mathematical operations:
    clamp, vectorClamp, sqr, sqrDiff, seed, rand, blend, morph, splitBezier, frac

 distance-related operations:
    distance, near

 polygon manipulation:
    closePoly, openPoly
    edges, innerEdges, triples, perimeter, area
    convex, concave, concaves
    lowerPoly, raisePoly, poly2Tri, triList, triangulateUV, triangulate
    polygon, semigon

 point/triangle/polygon interaction:
    triContains, triContainsAny,

 os interaction:
    docmd

The following constants are defined here:
   origin - the location of the origin (0,0,0)
   pi - the number of radians in a semi-circle
   pi2 - the number of radians in a circle
   phi - the height of your belly button, as a percentage of you height
   golden - the ideal aspect ratio
   e - Euler's constant; the base of logarithms
   fuzz - a smallish number; two values are fuzzy-equal when this close

The definitions of the basic colors are also provided here:
   black, dkGray, gray, ltGray, and white
   red, yellow, green, cyan, blue, and magenta
   purple (for Williams)
   purpleA (for Amherst)
"""
import math
import os
import tempfile
from collections import Iterable
from random import random
from random import seed as randseed

__all__ = ( 'ambrosiaCopyright', 'ambrosiaHome', 'ambrosiaVersion', 'area', 'black', 'blend', 'blue', 'clamp', 'clampedType', 'closePoly', 'concave', 'concaves', 'convex', 'crossProduct', 'cyan', 'deg2rad', 'distance', 'dkGray', 'docmd', 'docmdWoutput', 'dotProduct', 'e', 'edges', 'fileExists', 'frac', 'fuzz', 'golden', 'gray', 'green', 'halfpi', 'hsv2rgb', 'innerEdges', 'last', 'lowerPoly', 'ltGray', 'magenta', 'morph', 'near', 'normalize', 'openPoly', 'origin', 'perimeter', 'phi', 'pi', 'pi2', 'poly2tri', 'polygon', 'purple', 'raisePoly', 'rad2deg', 'rand', 'red', 'rgb2hsv', 'scriptsHome', 'seed', 'semigon', 'splitBezier', 'sqr', 'sqrDiff', 'tempDir', 'triContains', 'triContainsAny', 'triList', 'triangulate', 'triangulateUV', 'triples', 'typeCheck', 'userName', 'userHome', 'vectorClamp', 'vectorDifference', 'vectorLength', 'vectorScale', 'vectorSum', 'white', 'yellow')

###############################################################################
# BUILTINS:
# Great Constants of the universe
origin=[0,0,0]
pi = math.acos(-1)
pi2 = 2*pi
halfpi = pi/2
phi = (1+math.sqrt(5))/2
golden = 1/phi
e = math.exp(1)
fuzz = 0.000001

# Basic colors, rgb format
black = (0,0,0)
dkGray = (0.25,0.25,0.25)
gray = (0.5,0.5,0.5)
ltGray = (0.75,0.75,0.75)
white = (1,1,1)
red = (1,0,0)
green = (0,1,0)
blue = (0,0,1)
cyan = (0,1,1)
magenta = (1,0,1)
yellow = (1,1,0)
purple = (89/255,17/255,142/255) # Pantone PMS 267 (Williams)
#purpleA1 = (72/255, 31/255, 145/255) # Pantone PMS 267c (Amherst)
#purpleA2 = (109/255, 40/255, 170/255) # Pantone PMS 266 (Amherst, vibrant)

# Default environment hooks:
ambrosiaHome = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
userHome = os.getenv('HOME')
userName = os.getenv('USER')
scriptsHome = os.path.join(ambrosiaHome,'scripts')
tempDir = tempfile.gettempdir()
###############################################################################
# Definitions
class clampedType(object):
    __slots__ = ('_type','_low','_high')
    def __init__(self,type,low=None,high=None):
        self._type = type
        self._low = low
        self._high = high

    def type(self):
        return self._type

    def low(self):
        return self._low

    def high(self):
        return self._high

    def inRange(self,o):
        return ((self.low() is None) or (self.low() <= o)) and ((self.high() is None) or (o <= self.high()))

    def __str__(self):
        if self.low() is None and self.high is None:
            return "{}".format(self.typeName())
        elif self.low() is None:
            return "{}, no greater than {}".format(self.typeName(),self.high())
        elif self.high() is None:
            return "{}, no less than {}".format(self.typeName(),self.low())
        else:
            return "{} in range {} to {}".format(self.typeName(),self.low(),self.high())

    def typeName(self):
        if isinstance(self.type(),type):
            return self.type().__name__
        if isinstance(self.type(),set):
            return "one of {}".format([t.__name__ for t in self.type()])
        return str(t)
        
def typeCheck(obj,tspec):
    if isinstance(tspec,type):
        assert isinstance(obj,tspec), "{} is of type {}".format(obj,tspec.__name__)
    elif isinstance(tspec,clampedType):
        typeCheck(obj,tspec.type())
        assert tspec.inRange(obj), "{} is of type {}".format(obj,tspec)
    elif isinstance(tspec,set):
        for t in tspec:
            if isinstance(obj,t):
                break
        else:
            assert False, "{} is any type in {}".format(obj,[t.__name__ for t in tspec])
    else:
        tl = len(tspec)
        ol = len(obj)
        assert tl == ol or tl==1, "{} is shape {}".format(obj,tspec)
        if isinstance(tspec,list) or isinstance(tspec,tuple):
            assert isinstance(obj,list) or isinstance(obj,tuple), "{} is of type list or tuple".format(obj)

        if tl == 1:
            for o in obj:
                typeCheck(o,tspec[0])
        for (o,t) in zip(obj,tspec):
            typeCheck(o,t)
    return True

def dotProduct(v0,v1):
    """Compute the dot product of two vectors."""
    return sum([e0*e1 for (e0,e1) in zip(v0,v1)])

def vectorLength(v):
    """Compute the length of a vector."""
    return math.sqrt(sum([e*e for e in v])) # really: sqrt of dotProduct(v,v)

def vectorScale(v,s):
    """Scale a vector v by s."""
    return [s*e for e in v]

def clamp(val,low=None,high=None):
    """Return value clamped between low and high.

    If either of low (high) is not specified, lower (upper) bound is not
    enforced."""
    if (low is not None) and (val < low):
        return low
    if (high is not None) and (val > high):
        return high
    return val
        
def vectorClamp(v,low=None,high=None):
    """Clamp all values in vector.

    If either of low (high) is not specified, lower (upper) bound is not
    enforced."""
    return [clamp(e,low,high) for e in v]

def crossProduct(v0,v1):
    """Compute cross product of two vectors."""
    (x0,y0,z0) = v0
    (x1,y1,z1) = v1
    return [(y0*z1)-(z0*y1),(z0*x1)-(x0*z1),(x0*y1)-(y0*x1)]

def normalize(v):
    """Compute unit-length vector in direction v."""
    l = vectorLength(v)
    if l < fuzz:
        return [0,1,0]
    else:
        return [e/l for e in v]

def deg2rad(deg):
    """Convert degrees to radians."""
    return deg*pi/180

def rad2deg(rad):
    """Convert radians to degrees."""
    return rad/pi*180

def sqr(n):
    """Compute square of n."""
    return n*n

def sqrDiff(a,b):
    """Squared difference ((a-b)^2; never negative) of a and b."""
    if isinstance(a,Iterable):
        return [sqrDiff(u,v) for (u,v) in zip(a,b)]
    else:
        return sqr(a-b)

def distance(a,b):
    """Distance between numbers or vectors."""
    if isinstance(a,Iterable):
        d = vectorDifference(a,b)
        return vectorLength(d)
    else:
        return math.sqrt(sqrDiff(a,b))

def near(a,b):
    """Check that the distance between two numbers or vectors is less than fuzz."""
    return distance(a,b)<fuzz

def vectorDifference(v0,v1):
    """Compute the difference between numbers or vectors."""
    if isinstance(v0,Iterable):
        assert isinstance(v1,Iterable)
        return [vectorDifference(a,b) for (a,b) in zip(v0,v1)]
    else:
        return v0-v1

def vectorSum(v0,v1):
    """Sum two numbers or vectors."""
    if isinstance(v0,Iterable):
        assert isinstance(v1,Iterable)
        return [vectorSum(a,b) for (a,b) in zip(v0,v1)]
    else:
        return v0+v1

def last(l):
    """Get last element of a vector."""
    return l[-1]

def raisePoly(poly):
    """Lift polygon to next higher dimension."""
    assert ((len(poly) == 0) or typeCheck(poly[0],({int,float},{int,float}))),poly[0]
    return [tuple(list(pt)+[0]) for pt in poly]

def closePoly(poly,length=None):
    """Ensure first and last points of polygon are the same."""
    if poly:
        if length is None:
            first = poly[0]
            last = poly[-1]
            if distance(first,last) > fuzz:
                poly = poly+[first]
        else:
            l = len(poly)
            if l != length:
                poly = poly+poly[:length-l]
    return poly

def openPoly(poly):
    """Ensure first and last points of polygon are not the same."""
    if poly:
        first, last = poly[0],poly[-1]
        if distance(first,last) <= fuzz:
            poly = poly[:-1]
    return poly

def edges(poly):
    """Generate edges of a polygon."""
    cpoly = closePoly(poly)
    return zip(cpoly[:-1],cpoly[1:])

def innerEdges(poly):
    """Generate the n-1 edges mentioned along a n point open polygon."""
    return zip(poly[:-1],poly[1:])

def triples(poly):
    """Generate triples of points circumnavigating poly."""
    l = len(openPoly(poly))
    p0,p1 = poly[0],poly[1]
    for i in range(l):
        p2 = poly[(i+2)%l]
        yield(p0,p1,p2)
        p0,p1 = p1,p2

def perimeter(poly):
    """Compute the perimeter of a polygon."""
    return sum([distance(*e) for e in edges(poly)])

def _areaUnder2d(a,b):
    """Compute the area to axis, below 2D points a and b."""
    return 0.5*(a[0]*b[1]-a[1]*b[0])

def area(poly):
    """Compute the area of a polygon (its projection in x-y plane)."""
    return sum([_areaUnder2d(*e) for e in edges(poly)])

def _orient(poly):
    """Return 2D polygon with points in standard order."""
    if area(poly) < 0:
        poly = poly[::-1]
    return poly

def convex(a,b,c):
    """If a-b-c is standard order, return True if a-b-c is convex."""
    return area([a,b,c]) >= 0

def concave(a,b,c):
    """If a-b-c is standard order, return True if a-b-c is concave."""
    return area([a,b,c]) < 0

def triContains(a,b,c,p):
    """True if point p is properly within triangle a-b-c."""
    return concave(a,p,b) and concave(b,p,c) and concave(c,p,a)

def concaves(poly):
    """Return a list of points where perimeter turns to from concave."""
    return [p1 for (p0,p1,p2) in triples(poly) if concave(p0,p1,p2)]

def triContainsAny(a,b,c,poly):
    """Return true if triangle contains any points of polygon."""
    for p in poly:
        if triContains(a,b,c,p):
            return True
    return False

def _ear(poly,concs=None):
    """Find first index of triangle to be pruned from polygon.
    There is always one."""
    l = len(openPoly(poly))
    if concs == None:
        concs = concaves(poly)
    i = 1
    for (a,b,c) in triples(poly):
        if convex(a,b,c) and not triContainsAny(a,b,c, poly):
            # this is the index of *b*:
            return i%l
        i += 1
    return None

def _pts2dirs(poly):
    """Convert a polygon to a list of edge vectors."""
    return [vectorDifference(b,a) for (a,b) in edges(poly)]

def _dirs2pts(dpoly,start=None):
    """Convert a polygon of edge vectors to a vertex poly.
    start is optional starting point (defaults to [0,0]).
    """
    p = [0,0] if start is None else start
    poly = [p]
    for dir in dpoly[:-1]:
        p = vectorSum(p,dir)
        poly.append(p)
    return poly

def _dpolyNormal(dpoly):
    """Return normal information for direction poly."""
    # "edges", here, grabs pairs of direction vectors.
    for (dir0,dir1) in edges(dpoly):
        norm = crossProduct(dir0,dir1)
        if vectorLength(norm) > 0:
            unit0 = normalize(dir0)
            unitNormal = normalize(norm)
            return (unitNormal,unit0,crossProduct(unitNormal,unit0))

def lowerPoly(poly):
    """Lower the polygon from 3D to 2D."""
    dpoly = _pts2dirs(poly)
    newBasis = _dpolyNormal(dpoly)
    u = newBasis[1]
    v = newBasis[2]
    newdpoly = [[dotProduct(u,e),dotProduct(v,e)] for e in dpoly]
    newpoly = _dirs2pts(newdpoly)
    return newpoly if area(newpoly) >= 0 else [[u,-v] for (u,v) in newpoly]

def poly2tri(poly):
    """Return indices of polygon triangulation."""
    # copy to avoid poly side-effects
    poly = openPoly(poly[::])
    result = []
    while len(poly) > 3:
        target = _ear(poly)
        del poly[target]
        result.append(target)
    result.append(1)
    return result

def triList(poly,order):
    """Return a list of triangles that make up a closed polygon."""
    poly = poly+poly[1:2]
    result = []
    for middle in order:
        result.append(poly[middle-1:middle+2])
        del poly[middle]
    return result

def triangulateUV(poly,uvpoly):
    """Triangulate polygon and UV points in parallel."""
    poly = closePoly(poly)
    l = len(poly)
    # this ensures uv is closed consistently with poly
    uvcopy = closePoly(uvpoly,length=l)
    poly2d = lowerPoly(poly)
    order = poly2tri(poly2d)
    return list(zip(list(triList(poly,order)),list(triList(uvcopy,order))))

def triangulate(poly):
    """Convert polygon to a list of triangles."""
    poly = closePoly(poly)
    return list(triList(poly,poly2tri(lowerPoly(poly))))

def polygon(n,radius=50,start=0,x=0,y=0):
    """Return an open regular polygon with n points."""
    result = []
    delta = pi2/n
    start = deg2rad(start)
    for i in range(n):
        angle = i*delta+start
        result.append( (radius * math.cos(angle)+x, radius * math.sin(angle)+y))
    return result

def semigon(n,radius=50,start=None,span=None,x=0,y=0):
    """Return an (open) polygon right of y axis."""
    if start is None:
        start = -halfpi
    else:
        start = deg2Rad(start)
    if span is None:
        span = pi
    else:
        span = deg2rad(span)
    result = []
    delta = span/(n-1)
    for i in range(n):
        angle = i*delta+start
        result.append( (radius * math.cos(angle)+x, radius * math.sin(angle)+y))
    return result

def rand(low,high):
    """Return a random value in range [low,high)."""
    return low+(random()*(high-low))

def seed(newSeed):
    """Set seed for the random number generator."""
    randseed(newSeed)

def _blend(coeffs,*args):
    """Blend similarly shapped lists according to coefficient list."""
    if isinstance(args[0],Iterable):
        c = type(args[0])
        return c([_blend(coeffs,*args_i) for args_i in zip(*args)])
    else:
        return dotProduct(coeffs,args)

def blend(t,*args):
    """Return a value that is 0<=pct<=1 from args[0] to args[-1]."""
    s = 1-t
    l = len(args)
    if l == 1:
        return args[0] # a tautology
    elif l == 2:
        return _blend([s,t],*args)
    elif l == 3:
        return _blend([s*s,2*s*t,t*t],*args)
    elif l == 4:
        return _blend([s*s*s,3*s*s*t,3*s*t*t,t*t*t],*args)
    assert False

def morph(n,*args):
    """Return a list of n+1 values blended across args."""
    return [blend(i/n,*args) for i in range(n+1)]

def splitBezier(p,a,b,c,d):
    """Split a Bezier spline in two at p percent."""
    s0 = blend(p,a,b)
    m = blend(p,b,c)
    t1 = blend(p,c,d)
    s1 = blend(p,s0,m)
    t0 = blend(p,m,t1)
    e = blend(p,s1,t0)
    return ([a,s0,s1,e],[e,t0,t1,d])

def frac(x):
    """Return value between 0 and 1."""
    return x%1

def hsv2rgb(c):
    """Return hsv equivalent to rgb value."""
    h,s,v = c
    h = 6*frac(h/360)
    i = int(h)
    f = h-i
    p = v*(1-s)
    q = v*(1-s*f)
    t = v*(1-s*(1-f))
    if (i==6) or (i==0):
        return (v,t,p)
    elif i == 1:
        return (q,v,p)
    elif i == 2:
        return (p,v,t)
    elif i == 3:
        return (p,q,v)
    elif i == 4:
        return (t,p,v)
    elif i == 5:
        return (v,p,q)
    else:
        return i

def rgb2hsv(c):
    r,g,b = c
    v = max(r,g,b)
    mn = min(r,g,b)
    range = v-mn
    if v == mn:
        h = 0
    elif v == r:
        h = 60*(g-b)/range+(0 if g >= b else 360)
    elif v == g:
        h = 60*(b-r)/range+120
    else:
        h = 60*(r-g)/range+240
    s = 0 if v == 0 else 1-mn/v
    return (h,s,v)

def docmd(cmd):
    os.system(cmd)

def docmdWoutput(cmd):
    return [line.strip() for line in os.popen(cmd)]

def fileExists(f):
    try:
        os.stat(f)
    except FileNotFoundError:
        return False
    else:
        return True

ambrosiaVersion = """ambrosia $VERSION"""

ambrosiaCopyright =  """ambrosia (c) 2013-19 duane a. bailey"""

