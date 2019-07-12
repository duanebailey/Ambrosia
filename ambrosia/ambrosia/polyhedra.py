#! /usr/bin/env python3
# Project Ambrosia (c) 2013-19 Duane A. Bailey
from ambrosia.basics import *
from ambrosia.objects import *
from ambrosia.meshes import Mesh
from math import sin,cos,sqrt

__all__ = ['Hexahedron', 'Tetrahedron', 'Octahedron', 'Dodecahedron', 'Icosahedron']

class Hexahedron(Mesh):
    def __init__(self):
        super().__init__()
        face = translate(0,0,-50).mapPoly(raisePoly([(-50,-50),(50,-50),(50,50),(-50,50)]))
        uvFace = [(0,0),(1,0),(1,1),(0,1)]
        for t in [identity,xRot(90),xRot(-90),xRot(-180),yRot(90),yRot(-90)]:
            self.addUVPoly(t.mapPoly(face),uvFace)

class Tetrahedron(Mesh):
    def __init__(self):
        super().__init__()
        uvFace = [(0,0),(1,0),(.5,sqrt(3)/2)]
        a = (50,50,50)
        b = (-50,-50,50)
        c = (-50, 50, -50)
        d = (50,-50,-50)
        self.addUVPoly([a,b,c],uvFace)
        self.addUVPoly([a,b,d],uvFace)
        self.addUVPoly([a,c,d],uvFace)
        self.addUVPoly([b,c,d],uvFace)

class Octahedron(Mesh):
    def __init__(self):
        super().__init__()
        uvFace = [(0,0),(1,0),(.5,sqrt(3)/2)]
        up=(0,50,0)
        down=(0,-50,0)
        west=(-50,0,0)
        east=(50,0,0)
        north=(0,0,50)
        south=(0,0,-50)
        self.addUVPoly([west, south, up], uvFace)
        self.addUVPoly([south, east, up], uvFace)
        self.addUVPoly([east, north, up], uvFace)
        self.addUVPoly([north, west, up], uvFace)
        self.addUVPoly([south, west, down], uvFace)
        self.addUVPoly([west, north, down], uvFace)
        self.addUVPoly([north, east, down], uvFace)
        self.addUVPoly([east, south, down], uvFace)

class Dodecahedron(Mesh):
    def __init__(self):
        super().__init__()
        s= 28.86738474
        b= s*(1+sqrt(5))/2 # (* s (/ (+ 1 (sqrt 5)) 2))
        a= s*2/(1+sqrt(5)) # (* s (/ 2 (+ 1 (sqrt 5))))
        p0=(s,s,s)
        p1=(-s,s,s)
        p2=(s,-s,s)
        p3=(s,s,-s)
        p4=(-s,-s,s)
        p5=(-s,s,-s)
        p6=(s,-s,-s)
        p7=(-s,-s,-s)
        p8=(0,a,b)
        p9=(b,0,a)
        p10=(a,b,0)
        p11=(0,-a,b)
        p12=(b,0,-a)
        p13=(-a,b,0)
        p14=(0,a,-b)
        p15=(-b,0,a)
        p16=(a,-b,0)
        p17=(0,-a,-b)
        p18=(-b,0,-a)
        p19=(-a,-b,0)
        uvFace=[(0.34549,0.0),(0.9045069943749474,0.18163563200134025),(0.9045069943749474,0.7694208842938134),(0.34549,0.9510565162951536),(0,0.4755282581475769)]
        self.addUVPoly([p0,p8,p1,p13,p10],uvFace)
        self.addUVPoly([p0,p9,p2,p11,p8],uvFace)
        self.addUVPoly([p0,p10,p3,p12,p9],uvFace)
        self.addUVPoly([p4,p15,p1,p8,p11],uvFace)
        self.addUVPoly([p4,p11,p2,p16,p19],uvFace)
        self.addUVPoly([p4,p19,p7,p18,p15],uvFace)
        self.addUVPoly([p5,p13,p1,p15,p18],uvFace)
        self.addUVPoly([p5,p14,p3,p10,p13],uvFace)
        self.addUVPoly([p5,p18,p7,p17,p14],uvFace)
        self.addUVPoly([p6,p16,p2,p9,p12],uvFace)
        self.addUVPoly([p6,p12,p3,p14,p17],uvFace)
        self.addUVPoly([p6,p17,p7,p19,p16],uvFace)

class Icosahedron(Mesh):
    def __init__(self):
        super().__init__()
        a=25.1 #24.97027456
        b=a/golden
        p0=(0,a,b)
        p1=(b,0,a)
        p2=(a,b,0)
        p3=(0,-a,b)
        p4=(b,0,-a)
        p5=(-a,b,0)
        p6=(0,a,-b)
        p7=(-b,0,a)
        p8=(a,-b,0)
        p9=(0,-a,-b)
        p10=(-b,0,-a)
        p11=(-a,-b,0)
        uvFace=[(0,0),(1,0),(.5,sqrt(3)/2)]
        self.addUVTri([p1,p2,p0],uvFace)
        self.addUVTri([p2,p5,p0],uvFace)
        self.addUVTri([p5,p7,p0],uvFace)
        self.addUVTri([p7,p3,p0],uvFace)
        self.addUVTri([p3,p1,p0],uvFace)
        self.addUVTri([p2,p1,p4],uvFace)
        self.addUVTri([p5,p2,p6],uvFace)
        self.addUVTri([p7,p5,p10],uvFace)
        self.addUVTri([p3,p7,p11],uvFace)
        self.addUVTri([p1,p3,p8],uvFace)
        self.addUVTri([p8,p4,p1],uvFace)
        self.addUVTri([p4,p6,p2],uvFace)
        self.addUVTri([p6,p10,p5],uvFace)
        self.addUVTri([p10,p11,p7],uvFace)
        self.addUVTri([p11,p8,p3],uvFace)
        self.addUVTri([p4,p8,p9],uvFace)
        self.addUVTri([p8,p11,p9],uvFace)
        self.addUVTri([p11,p10,p9],uvFace)
        self.addUVTri([p10,p6,p9],uvFace)
        self.addUVTri([p6,p4,p9],uvFace)
