#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
#
"""This module contains all classes associated with meshes."""

from ambrosia.decorators import *
from ambrosia.basics import *
from ambrosia.objects import *

__all__ = ('extrude', 'sweep', 'loft', 'FuzzList', 'HeightField', 'Mesh', 'PatchMesh')
###############################################################################
# FuzzList
@checkdoc
class FuzzList(AmbrosiaObject):
    """This class has some features of a list, but matching is fuzzy."""
    __slots__ = ['_items','_near']
    def __init__(self,base=None,nearf=None,description="A fuzzy list."):
        super().__init__(description=description)
        self._items = base if base is not None else []
        self._near = nearf if nearf is not None else near

    def __getitem__(self,i):
        """Get the ith item."""
        return self._items[i]

    def __setitem__(self,i,v):
        """Set the ith item to v."""
        _items[i] = v

    def __contains__(self,v):
        """Determine if v is in items."""
        for i in self._items:
            if near(i,v):
                return True
        return False

    def __len__(self):
        """Return length of list."""
        return len(self._items)

    def __iter__(self):
        """Return the values of the underlying list."""
        for v in self._items:
            yield v

    def find(self,v):
        """Return index of near item, or -1."""
        for i in range(len(self)):
            if near(self[i],v):
                return i
        return -1

    def intern(self,v):
        """Store v in list, if necessary, and return ultimate index."""
        i = self.find(v)
        if i < 0:
            i = len(self._items)
            self._items.append(v)
        return i

###############################################################################
# Mesh: solids constructed from triangles
@checkdoc
class Mesh(Primitive):
    """A Mesh is a possibly solid structure defined by a collection of triangles."""
    def __init__(self,description="A triangle mesh."):
        super().__init__(description=description)
        self.set('mesh.vertices',FuzzList())
        self.set('mesh.uvvertices',FuzzList())
        self.set('mesh.triangles',[])
        self.set('mesh.uvtriangles',[])

    def register(self,v):
        """Assign an index to vertex v."""
        return self.get('mesh.vertices').intern(v)

    def uvregister(self,v):
        """Assign an index to uv vertex v."""
        return self.get('mesh.uvvertices').intern(v)
        
    def addTri(self,t):
        """Add a triangle to the mesh."""
        indexTri = [self.register(v) for v in t]
        self.get('mesh.triangles').append(indexTri)
        return self

    def addUVTri(self,t,uv):
        """Add a uv-identifed triangle to the mesh."""
        indexTri = [self.register(v) for v in t]
        indexUVTri = [self.uvregister(v) for v in uv]
        self.get('mesh.triangles').append(indexTri)
        self.get('mesh.uvtriangles').append(indexUVTri)
        return self
    
    def addPoly(self,p):
        """Triangulate and add polygon to the mesh."""
        for t in triangulate(p):
            self.addTri(t)
        return self

    def addUVPoly(self,p,uv):
        """Triangulate and add polygon to the mesh."""
        for (t,uvt) in triangulateUV(p,uv):
            self.addUVTri(t,uvt)
        return self

    def registerVertices(self,vl):
        """Directly set the vertex dictionary for this mesh."""
        self.set('mesh.vertices',FuzzList(vl))
        return self

    def registerUVVertices(self,uvl):
        """Directly set the UV-vertex dictionary for this mesh."""
        self.set('mesh.uvvertices',FuzzList(uvl))
        return self

    def registerTriangles(self,tl):
        """Directly set the triangle list for this mesh."""
        self.set('mesh.triangles',tl)

    def registerUVTriangles(self,uvtl):
        """Directly set the uv-triangle list for this mesh."""
        self.set('mesh.uvtriangles',uvtl)
        return self
            
    def _POV_(self,context):
        if context.selects(self):
            vl = self.get('mesh.vertices')
            t = self.getXform()
            m = self.getMaterial()
            prt('mesh2 {\n')
            prt('vertex_vectors {{ {}'.format(len(vl)))
            for vtx in vl:
                prt(',')
                pov.writePoint(vtx)
            prt('}\n')
            uvl = self.get('mesh.uvvertices')
            if len(uvl) > 0:
                prt('uv_vectors {{ {}'.format(len(uvl)))
                for vtx in uvl:
                    prt(',')
                    pov.writePoint(vtx)
                prt('}\n')
            tl = self.get('mesh.triangles')
            prt('face_indices {{ {}'.format(len(tl)))
            for tri in tl:
                prt(',')
                pov.writePoint(tri)
            prt('}\n')
            uvtl = self.get('mesh.uvtriangles')
            if len(uvtl) > 0:
                prt('uv_indices {{ {}'.format(len(uvtl)))
                for tri in uvtl:
                    prt(',')
                    pov.writePoint(tri)
                prt('}\n')
            prt('inside_vector <0,0,1>\n')
            POV(super(),context)
            prt('}\n')

###############################################################################
# PatchMesh: a mesh constructed from Bezier patches.
@checkdoc
class PatchMesh(Primitive):
    """A PatchMesh is a possibly solid structure defined by a collection of Bezier patches."""
    def __init__(self,description="A Bezier patch mesh."):
        super().__init__(description=description)
        self.set('patchmesh.vertices',FuzzList())
        self.set('patchmesh.uvvertices',FuzzList())
        self.set('patchmesh.patches',[])
        self.set('patchmesh.uvpatches',[])
        self.refinement(3)

    def registerVertices(self,vl):
        """Directly set the vertex dictionary for this mesh."""
        self.set('patchmesh.vertices',FuzzList(vl))

    def registerUVVertices(self,uvl):
        """Directly set the UV-vertex dictionary for this mesh."""
        self.set('patchmesh.uvvertices',FuzzList(uvl))

    def registerPatches(self,pl):
        """Directly set the patch list for this mesh."""
        self.set('patchmesh.patches',pl)

    def registerUVPatches(self,uvpl):
        """Directly set the uv-patch list for this mesh."""
        self.set('patchmesh.uvpatches',uvpl)

    def register(self,v):
        """Assign an index to vertex v."""
        return self.get('patchmesh.vertices').intern(v)

    def uvregister(self,v):
        """Assign an index to uv vertex v."""
        return self.get('patchmesh.uvvertices').intern(v)
        
    def addPatch(self,p):
        """Add a patch to the mesh."""
        indexPatch = [self.register(v) for v in p]
        self.get('patchmesh.patches').append(indexPatch)

    def addUVPatch(self,p,uv):
        """Add a uv-identifed triangle to the mesh."""
        assert len(p) == 16
        assert len(uv) == 4
        indexPatch = [self.register(v) for v in p]
        indexUVPatch = [self.uvregister(v) for v in uv]
        self.get('patchmesh.patches').append(indexPatch)
        self.get('patchmesh.uvpatches').append(indexUVPatch)
    
    def refinement(self,ref):
        """Set the refinement level of the patches in this mesh."""        
        self.set('patchmesh.refinement',ref)
        return self

    def getRefinement(self):
        """Get the refinement level of the patches in this mesh."""
        return self.get('patchmesh.refinement')

    def _POV_patch(self,p,v,r,context):
        prt('bicubic_patch {{ type 0 flatness 0.1 u_steps {} v_steps {}\n'.format(r,r))
        for i in range(16):
            if i:
                prt(',')
            pov.writePoint(v[p[i]])
        POV(super(),context)
        prt('}\n')

    def _POV_uvpatch(self,p,v,uvp,uvv,r,context):
        prt('bicubic_patch {{ type 0 flatness 0.1 u_steps {} v_steps {}\n'.format(r,r))
        prt('uv_vectors ');
        for i in range(4):
            if i:
                prt(',')
            pov.writePoint(uvv[uvp[i]])
        for i in range(16):
            if i:
                prt(',')
            pov.writePoint(v[p[i]])
        POV(super(),context)
        prt('}\n')

    def _POV_(self,context):
        if context.selects(self):
            t = self.getXform()
            m = self.getMaterial()
            uvpl = self.get('patchmesh.uvpatches')
            pl = self.get('patchmesh.patches')
            vl = self.get('patchmesh.vertices')
            r = self.get('patchmesh.refinement')
            if len(uvpl) > 0:
                uvvl = self.get('patchmesh.uvvertices')
                for i in range(len(pl)):
                    p = pl[i]
                    uvp = uvpl[i]
                    self._POV_uvpatch(p,vl,uvp,uvvl,r,context)
            else:
                for i in range(len(pl)):
                    p = pl[i]
                    self._POV_patch(p,vl,r,context)

###############################################################################
# HeightField: a surface generated from an image
@checkdoc
class HeightField(Primitive):
    """HeightFields are surfaces that are constructed from image pixel
    intensitifges."""
    def __init__(self,description="A height field."):
        super().__init__(description=description)
        self.scale(100,100,100)
        self.translate(-50,-50,-50)
        self.image("untitled")
        self.imageType("png")

    def image(self,v):
        """Set the image attribute."""
        self.set('heightfield.image',v)
        #assert fileExists(environment.makeFilePath(v)), "Warning: HeightField's image file, {}, not found in images folder.".format(v)        
        return self

    def getImage(self):
        """Get the image attribute value."""
        return self.get('heightfield.image')

    def imageType(self,v):
        """Set imageType attribute."""
        self.set('heightfield.imageType',v)
        return self

    def getImageType(self):
        """Get imageType attribute."""
        return self.get('heightfield.imageType')

    def smooth(self,v):
        """Set smooth attribute."""
        self.set('heightfield.smooth',v)
        return self

    def getSmooth(self):
        """Get smooth attribute."""
        return self.get('heightfield.smooth')

    def clipLevel(self,v):
        """Set clipLevel attribute."""
        self.set('heightfield.clipLevel',v)
        return self

    def getClipLevel(self):
        """Get clipLevel attribute."""
        return self.get('heightfield.clipLevel')

    def _POV_(self,context):
        if context.selects(self):
            s = self.getSmooth()
            cl = self.getClipLevel()
            it = self.getImageType()
            i = self.getImage()
            t = self.getXform()
            m = self.getMaterial()
            #context.pushXform(t)
            #context.pushMaterial(m)
            prt('height_field {{ {} "{}" '.format(it,environment.makeImagePath(i)))
            if s:
                prt(' smooth')
            if cl:
                prt(' water_level {}'.format(cl))
            prt('\n')
            POV(super(),context)
            prt('}\n')
            #context.popMaterial()
            #context.popXform()

###############################################################################
# Extruded objects
# Extrude is a 'factory': it produces other objects

def extrude(front,*xforms):
    """Extrude a face through one or more transforms."""
    result = Mesh()
    cap = closePoly(front)
    result.addPoly(cap)
    # extrude0(cap0,xs,result)
    for x in xforms:
        nextCap = x(cap)
        for ((p0,p1),(q0,q1)) in zip(edges(cap),edges(nextCap)):
            # HANDEDNESS
            result.addTri([p0,q0,p1]).addTri([p1,q0,q1])
        cap = nextCap
    # back cap is reversed (to face backward)
    result.addPoly(cap[::-1])
    return result

###############################################################################
# Sweep: a factory for polygonal meshes.
def sweep(profile,n,capped=False):
    """Sweep a polygon around y-axis in n steps."""
    assert n > 2 and isinstance(n,int)
    profile = openPoly(profile)
    t = yRot(360/n)
    result = Mesh()

    if capped:
        first = profile[0]
        firstOnY = [0,first[1],0]
        if not near(first,firstOnY):
            print("adding bottom cap")
            cap = []
            for i in range(n):
                cap.append(first)
                first = t(first)
            result.addPoly(cap)

        last = profile[-1]
        lastOnY = [0,last[1],0]
        if not near(last,lastOnY):
            print("adding top cap.")
            cap = []
            for i in range(n):
                cap.append(last)
                last = t(last)
            result.addPoly(cap[::-1])

    for i in range(n):
        newProfile = t(profile)
        for ((p0,p1),(q0,q1)) in zip(edges(profile),edges(newProfile)):
            if near(p0,q0): # when p0 near y axis
                if not near(p1,q1):
                    result.addTri([p0,p1,q1])
            elif near(p1,q1): # when p1 near y axis
                result.addTri([p0,p1,q0])
            else:
                result.addTri([p0,p1,q0])
                result.addTri([p1,q1,q0])
        profile = newProfile
    return result


def loft(*sections):
    """Loft a surface across several sections."""
    result = Mesh()
    current = sections[0]
    cap = closePoly(current)
    result.addPoly(cap)
    for next in sections:
        for ((p0,p1),(q0,q1)) in zip(edges(current),edges(next)):
            # HANDEDNESS
            result.addTri([p0,q0,p1]).addTri([p1,q0,q1])
        current = next
    # back cap is reversed (to face backward)
    result.addPoly(closePoly(current))
    return result
