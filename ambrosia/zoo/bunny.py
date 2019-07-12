from ambrosia.meshes import Mesh
# The Stanford Bunny
# 35947 vertices and 69451 faces
# 100 units wide, 99.125 units tall, 77.5 units deep
class Bunny(Mesh):
    def __init__(self,description="A Stanford bunny."):
        super().__init__(description=description)
        self.translate(0.0168404,-0.0329874,0.00153695).scale(642.265,642.265,642.265).xyMirror()