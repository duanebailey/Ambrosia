#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
#
"""This module contains surface primitives."""
from ambrosia.decorators import *
from ambrosia.basics import *
from ambrosia.objects import *

__all__ = ('Cubic', 'InfiniteCone', 'InfiniteCylinder', 'InfiniteParaboloid', 'InfiniteHyperboloid', 'InfiniteSaddle', 'Quadric', 'Quartic', 'Surface')

_coefficientIndices = [
    None,
    None,
    dict(x2=0,xy=1,xz=2,x=3,y2=4,yz=5,y=6,z2=7,z=8,c=9,
         A=0,B=4,C=7,D=1,E=2,F=5,G=3,H=6,I=8,J=9),
    dict(x3=0,x2y=1,x2z=2,x2=3,xy2=4,xyz=5,xy=6,xz2=7,xz=8,x=9,y3=10,y2z=11,y2=12,yz2=13,yz=14,y=15,z3=16,z2=17,z=18,c=19),
    dict(x4=0,x3y=1,x3z=2,x3=3,x2y2=4,x2yz=5,x2y=6,x2z2=7,x2z=8,x2=9,xy3=10,xy2z=11,xy2=12,xyz2=13,xyz=14,xy=15,xz3=16,xz2=17,xz=18,x=19,y4=20,y3z=21,y3=22,y2z2=23,y2z=24,y2=25,yz3=26,yz2=27,yz=28,y=29,z4=30,z3=31,z2=32,z=33,c=34)]

###############################################################################
# Surface: a general surface determined by equations.
@checkdoc
class Surface(Primitive):
    """Surfaces are modeled by mathematical equations.
    This class implements those surfaces."""
    def __init__(self,degree=2,description="A general surface."):
        super().__init__(description=description)
        self.degree(degree)

    def degree(self,d):
        """Set the degree of the surface.  Must be 2,3, or 4."""
        self.set('surface.degree',d)
        nCoeffs = int((d+1)*(d+2)*(d+3)/6)
        self.set('surface.ncoeffs',nCoeffs)
        self.set('surface.coeffDict',_coefficientIndices[d])
        self.set('surface.coefficients',(nCoeffs*[0]))
        return self

    def getDegree(self):
        """Get the degree of the surface."""
        return self.get('surface.degree')

    def getCoefficients(self):
        """Return the coefficients that determine this surface."""
        return self.get('surface.coefficients')

    def coefficients(self,d):
        """Set coefficients according to coefficient dictionary."""
        global _coefficientIndices
        coeffs = self.getCoefficients()
        coeffd = _coefficientIndices[self.getDegree()]
        for k in d:
            coeffs[coeffd[k]] = d[k]

    def _POV_(self,context):
        if context.selects(self):
            d = self.getDegree()
            nc = self.get('surface.ncoeffs')
            c = self.getCoefficients()
            prt('poly {{{},<'.format(d))
            for i in range(nc):
                if i > 0:
                    prt(',')
                prt('{}'.format(c[i]))
            prt('>\n')
            self._POV_primitive(context)
            prt('}\n')

###############################################################################
# Quadric surfaces: controlled by second degree equations
@checkdoc
class Quadric(Surface):
    """Quadric surfaces are controlled by second degree equations in x,y,z."""
    def __init__(self,description="A quadric surface."):
        super().__init__(description=description)
        self.degree(2)


    def _POV_(self,context):
        if context.selects(self):
            v = self.getCoefficients()
            degree = 2
            ci = _coefficientIndices[degree]
            prt('quadric {')
            prt('<{},{},{}>,<{},{},{}>,<{},{},{}>,{}\n'.format(*[v[ci[s]] for s in 'ABCDEFGHIJ']))
            self._POV_primitive(context)
            prt('}\n')

###############################################################################
# Cubic surfaces: controlled by third degree equations
@checkdoc
class Cubic(Surface):
    """Cubic surfaces are controlled by third degree equations in x,y,z."""
    def __init__(self,description="A cubic surface."):
        super().__init__(description=description)
        self.degree(3)

###############################################################################
# Quartic surfaces: controlled by fourth degree equations
@checkdoc
class Quartic(Surface):
    """Quartic surfaces are controlled by fourth degree equations in x,y,z."""
    def __init__(self,description="A quartic surface."):
        super().__init__(description=description)
        self.degree(4)


###############################################################################
# InfiniteCylinder: a quadric surface x^2+z^2=100^2, a tube along y axis, r=
@checkdoc
class InfiniteCylinder(Quadric):
    """Infinite cylinders extend along the y axis, with diameter 100."""
    def __init__(self,description="An infinite cylinder."):
        super().__init__(description=description)
        self.coefficients(dict(x2=1,z2=1,c=-2500))

###############################################################################
# InfiniteCone: a quadric surface x^2+z^2 = y^2
@checkdoc
class InfiniteCone(Quadric):
    """Infinite cones extend from the origin, upward and downward, infinitely."""
    def __init__(self,description="An infinite cone."):
        super().__init__(description=description)
        self.coefficients(dict(x2=1,z2=1,y2=-1))

###############################################################################
# InfiniteParaboloid: a quadric surface x^2+z^2 = 100y
@checkdoc
class InfiniteParaboloid(Quadric):
    """Infinite paraboloids extend from the origin, upward, infinitely."""
    def __init__(self,description="An infinite paraboloid."):
        super().__init__(description=description)
        self.coefficients(dict(x2=1,z2=1,y=-100))

###############################################################################
# InfiniteHyperboloid: a quadric surface x^2+z^2 = y^2+1
@checkdoc
class InfiniteHyperboloid(Quadric):
    """Infinite hyperboloid extend from the origin, up and down, infinitely.
    In the x-z plane, it forms a disk, with diameter 100."""
    def __init__(self,description="An infinite hyperboloid."):
        super().__init__(description=description)
        self.coefficients(dict(x2=1,z2=1,y2=-1,c=-2500))

###############################################################################
# InfiniteSaddle: a cubic surface x^2-z^2 = 50
@checkdoc
class InfiniteSaddle(Quadric):
    """Infinite saddle from the origin, up and down, infinitely."""
    def __init__(self,description="An infinite saddle."):
        super().__init__(description=description)
        self.coefficients(dict(x2=0.25,z2=-1,y=-50))
