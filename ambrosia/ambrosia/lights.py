#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
#
"""Descriptions of various lights available in the ambrosia envioronment."""

from ambrosia.decorators import *
from ambrosia.basics import *
from ambrosia.objects import *

__all__ = ('Light', 'Spotlight', 'LightArray')

@checkdoc
class Light(Transformable):
    """This is base class for a variety of lights in ambrosia."""
    def __init__(self,description="A light."):
        """Construct a white light at the origin."""
        super().__init__(description=description)
        self.pos(origin)
        self.color(white)
        self.shadows(True)
        self.intensity(0.5)

    def copy(self):
        """Construct a copy of this light."""
        return super().copy()

    def color(self,c):
        """Set light color."""
        self.set('light.color',c)
        return self

    def pos(self,p):
        """Set position of light; p may be a transform or point."""
        if isinstance(p,Transform):
            p = p(self.getPos())
        self.set('light.pos',p)
        return self

    def getPos(self):
        """Get position of light."""
        return self.get('light.pos')

    def getColor(self):
        """Get current light color."""
        return self.get('light.color')

    def shape(self,obj):
        """Shape the light as another object."""
        self.set('light.shape',obj)
        return self

    def getShape(self):
        """Get shape of the light."""
        return self.get('light.shape')

    def shadows(self,bool):
        """Have light throw shadows iff bool is True."""
        self.set('light.shadows',bool)
        return self

    def getShadows(self):
        """Return True iff this light throws shadows."""
        return self.get('light.shadows')

    def intensity(self,i):
        """Set the intensity of light."""
        self.set('light.intensity',i)
        return self

    def getIntensity(self):
        """Determine the intensity of the light."""
        return self.get('light.intensity')

    def _POV_transform(self,context):
        """Dump transform settings."""
        POV(super(),context)

    def _POV_(self,context):
        """Dump light to POV file."""
        if context.selects(self):
            context.pushXform(self.getXform())
            prt('light_source {')
            pov.writePoint(context.mapPoint(self.getPos()))
            prt('\n')
            c = self.getColor()
            rgb = Color.wrap(c).getRGB()
            i = self.getIntensity()
            rgb = vectorClamp(vectorScale(rgb,i),low=0,high=1)
            pov.writeColor(rgb)
            if not self.getShadows():
                prt(' shadowless')
            prt('\n')
            s = self.getShape()
            if s is not None:
                prt(' looks_like { ')
                POV(s,context)
                prt(' }\n')
            prt('}\n')
            context.popXform()

###############################################################################
# Spotlight: a directed Light.
@checkdoc
class Spotlight(Light):
    """This class defines lights that possibly shine in a specific direction."""
    def __init__(self,description="A spotlight."):
        """Initialize a spotlight (radius 10, falloff 5, tightness 0, coi origin)."""
        super().__init__(description=description)
        self.radius(10).falloff(5).tightness(0).COI(origin)

    def COI(self,p):
        """Set the center-of-interest of the spot light."""
        if isinstance(p,Transform):
            p = p.mapPoint(self.getCOI())
        self.set('spotlight.coi',p)
        return self

    def getCOI(self):
        """Get the center-of-interest for the spotlight."""
        return self.get('spotlight.coi')
        
    def radius(self,r):
        """Set radius for light, the half angle of the light cone, degrees."""
        self.set('spotlight.radius',r)
        return self

    def getRadius(self):
        """Get the radius of the light."""
        return self.get('spotlight.radius')

    def falloff(self,da):
        """Set the falloff of the light; angle beyond radius of decay."""
        self.set('spotlight.falloff',da)
        return self

    def getFalloff(self):
        """Get the falloff of the light."""
        return self.get('spotlight.falloff')

    def tightness(self,t):
        """Set tightness to t; 0 is sharp edge."""
        self.set('spotlight.tightness',t)
        return self

    def getTightness(self):
        """Get the tightness of the light."""
        return self.get('spotlight.tightness')

    def _POV_(self,context):
        if context.selects(self):
            context.pushXform(self.getXform())
            prt('light_source {')
            pov.writePoint(context.mapPoint(self.getPos()))
            prt('\n')
            rgb = Color.wrap(self.getColor()).getRGB()
            i = self.getIntensity()
            rgb = vectorClamp(vectorScale(rgb,i),low=0,high=1)
            pov.writeColor(rgb)
            if not self.getShadows():
                prt(' shadowless')
            prt(' spotlight\npoint_at')
            pov.writePoint(self.getCOI())
            prt('\n')
            r = self.getRadius()
            f = self.getFalloff()+r
            t = self.getTightness()
            prt('radius {} falloff {} tightness {}\n'.format(r,f,t))
            prt('}\n')
            context.popXform()

###############################################################################
# LightArray: area lighting
@checkdoc
class LightArray(Light):
    """LightArrays simulate large 2D arrays of lights."""
    def __init__(self,description="A light array."):
        super().__init__(description=description)
        self.rows(2).cols(2).width([100,0,0]).height([0,0,100]).pos(origin)
    
    def cols(self,v):
        """Set the cols attribute."""
        self.set('lightarray.cols',v)
        return self

    def getCols(self):
        """Get the cols attribute."""
        return self.get('lightarray.cols')

    def rows(self,v):
        """Set the rows attribute."""
        self.set('lightarray.rows',v)
        return self

    def getRows(self):
        """Get the rows attribute."""
        return self.get('lightarray.rows')

    def width(self,v):
        """Set the width attribute."""
        self.set('lightarray.width',v)
        return self

    def getWidth(self):
        """Get the width attribute."""
        return self.get('lightarray.width')

    def height(self,v):
        """Set the height attribute."""
        self.set('lightarray.height',v)
        return self

    def getHeight(self):
        """Get the height attribute."""
        return self.get('lightarray.height')

    def _POV_(self,context):
        if context.selects(self):
            context.pushXform(self.getXform())
            prt('light_source { ')
            pov.writePoint(context.mapPoint(self.getPos()))
            prt('\n')
            rgb = Color.wrap(self.getColor()).getRGB()
            i = self.getIntensity()
            rgb = vectorClamp(vectorScale(rgb,i),low=0,high=1)
            pov.writeColor(rgb)
            if not self.getShadows():
                prt(' shadowless')
            prt(' area_light\n')
            w = self.getWidth()
            h = self.getHeight()
            wd = context.mapDirection(w)
            hd = context.mapDirection(h)
            pov.writePoint(wd)
            prt(',')
            pov.writePoint(hd)
            prt(', {}, {}\n'.format(self.getCols(),self.getRows()))
            prt('}\n')
            context.popXform()
