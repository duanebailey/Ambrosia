## Chess set for Computer Science 109.
## (c) 2008,2014 duane a. bailey

## This model was constructed for Exam 1, 2008.
## For the most part, this model file may be read and understood by students
## who've made it this far.
## That said, this model code could be greatly improved and should not be 
## construed as a good example of anything ;-)

from ambrosia import *
from ambrosia.zoo.teapot import Teapot
from math import sin,cos

## The squares of the chess board are 50x50, which should fit within the view
## of the camera.
## The chess pieces were fashoned after traditional Staunten pieces and the
## relative sizes are approximately correct.
## In the end, the pieces are scaled by another factor of 2 to fit this particular
## board.
pieceScale=2

## This board undulates to emphasize the location of the power on the board.
## An artistic effect.  If you like a flat board, uncomment the 1 below, which
## will make all board squares their natural height.
## Students: You are not expected to understand this...yet.
def boardHeight(r,c):
    ra = pi/4 * (r-0.5)
    ca = pi/4 * (c-4.5)
    return 1+(((1+cos(ca))/2.0)*((1+cos(ra))/2.0))

## This is the basis for a chessboard square.  Scaling it up in the y direction
## makes it grow upward; all squares are at the same level.
square=Cube().scale(0.5).translate(0,25,0)

## Some shiny materials for the chessboard and the Plane that forms the
## "stage" for alternate camera views.
whiteBoardMat=Material().color(white).reflection(0.3).specularity(0.5).diffuse(1).roughness(0.05)
blackBoardMat=Material().color(black).reflection(0.3).specularity(0.5).diffuse(1).roughness(0.05)

## These are the materials for the pieces.  Black was too black, so I
## used a gray.  Colors looked tacky.  Specularity is most obvious in the
## Queen Detail
whitePieceMat=Material().color(white).reflection(0.1).specularity(0.5).diffuse(1).roughness(0.05)
blackPieceMat=Material().color(dkGray).reflection(0.1).specularity(0.5).diffuse(1).roughness(0.05)

## This is a brute force technique for constructing the board.
## Don't be shocked, I used cut and paste and a few find/replaces.
## We'll learn to program later.
board=Group()
board.add(square,whiteBoardMat,scale(1,boardHeight(1,1),1)*translate(-175,0,175))
board.add(square,blackBoardMat,scale(1,boardHeight(1,2),1)*translate(-125,0,175))
board.add(square,whiteBoardMat,scale(1,boardHeight(1,3),1)*translate(-75,0,175))
board.add(square,blackBoardMat,scale(1,boardHeight(1,4),1)*translate(-25,0,175))
board.add(square,whiteBoardMat,scale(1,boardHeight(1,5),1)*translate(25,0,175))
board.add(square,blackBoardMat,scale(1,boardHeight(1,6),1)*translate(75,0,175))
board.add(square,whiteBoardMat,scale(1,boardHeight(1,7),1)*translate(125,0,175))
board.add(square,blackBoardMat,scale(1,boardHeight(1,8),1)*translate(175,0,175))

board.add(square,blackBoardMat,scale(1,boardHeight(2,1),1)*translate(-175,0,125))
board.add(square,whiteBoardMat,scale(1,boardHeight(2,2),1)*translate(-125,0,125))
board.add(square,blackBoardMat,scale(1,boardHeight(2,3),1)*translate(-75,0,125))
board.add(square,whiteBoardMat,scale(1,boardHeight(2,4),1)*translate(-25,0,125))
board.add(square,blackBoardMat,scale(1,boardHeight(2,5),1)*translate(25,0,125))
board.add(square,whiteBoardMat,scale(1,boardHeight(2,6),1)*translate(75,0,125))
board.add(square,blackBoardMat,scale(1,boardHeight(2,7),1)*translate(125,0,125))
board.add(square,whiteBoardMat,scale(1,boardHeight(2,8),1)*translate(175,0,125))
board.add(square,whiteBoardMat,scale(1,boardHeight(3,1),1)*translate(-175,0,75))
board.add(square,blackBoardMat,scale(1,boardHeight(3,2),1)*translate(-125,0,75))
board.add(square,whiteBoardMat,scale(1,boardHeight(3,3),1)*translate(-75,0,75))
board.add(square,blackBoardMat,scale(1,boardHeight(3,4),1)*translate(-25,0,75))
board.add(square,whiteBoardMat,scale(1,boardHeight(3,5),1)*translate(25,0,75))
board.add(square,blackBoardMat,scale(1,boardHeight(3,6),1)*translate(75,0,75))
board.add(square,whiteBoardMat,scale(1,boardHeight(3,7),1)*translate(125,0,75))
board.add(square,blackBoardMat,scale(1,boardHeight(3,8),1)*translate(175,0,75))

board.add(square,blackBoardMat,scale(1,boardHeight(4,1),1)*translate(-175,0,25))
board.add(square,whiteBoardMat,scale(1,boardHeight(4,2),1)*translate(-125,0,25))
board.add(square,blackBoardMat,scale(1,boardHeight(4,3),1)*translate(-75,0,25))
board.add(square,whiteBoardMat,scale(1,boardHeight(4,4),1)*translate(-25,0,25))
board.add(square,blackBoardMat,scale(1,boardHeight(4,5),1)*translate(25,0,25))
board.add(square,whiteBoardMat,scale(1,boardHeight(4,6),1)*translate(75,0,25))
board.add(square,blackBoardMat,scale(1,boardHeight(4,7),1)*translate(125,0,25))
board.add(square,whiteBoardMat,scale(1,boardHeight(4,8),1)*translate(175,0,25))
board.add(square,whiteBoardMat,scale(1,boardHeight(5,1),1)*translate(-175,0,-25))
board.add(square,blackBoardMat,scale(1,boardHeight(5,2),1)*translate(-125,0,-25))
board.add(square,whiteBoardMat,scale(1,boardHeight(5,3),1)*translate(-75,0,-25))
board.add(square,blackBoardMat,scale(1,boardHeight(5,4),1)*translate(-25,0,-25))
board.add(square,whiteBoardMat,scale(1,boardHeight(5,5),1)*translate(25,0,-25))
board.add(square,blackBoardMat,scale(1,boardHeight(5,6),1)*translate(75,0,-25))
board.add(square,whiteBoardMat,scale(1,boardHeight(5,7),1)*translate(125,0,-25))
board.add(square,blackBoardMat,scale(1,boardHeight(5,8),1)*translate(175,0,-25))

board.add(square,blackBoardMat,scale(1,boardHeight(6,1),1)*translate(-175,0,-75))
board.add(square,whiteBoardMat,scale(1,boardHeight(6,2),1)*translate(-125,0,-75))
board.add(square,blackBoardMat,scale(1,boardHeight(6,3),1)*translate(-75,0,-75))
board.add(square,whiteBoardMat,scale(1,boardHeight(6,4),1)*translate(-25,0,-75))
board.add(square,blackBoardMat,scale(1,boardHeight(6,5),1)*translate(25,0,-75))
board.add(square,whiteBoardMat,scale(1,boardHeight(6,6),1)*translate(75,0,-75))
board.add(square,blackBoardMat,scale(1,boardHeight(6,7),1)*translate(125,0,-75))
board.add(square,whiteBoardMat,scale(1,boardHeight(6,8),1)*translate(175,0,-75))
board.add(square,whiteBoardMat,scale(1,boardHeight(7,1),1)*translate(-175,0,-125))
board.add(square,blackBoardMat,scale(1,boardHeight(7,2),1)*translate(-125,0,-125))
board.add(square,whiteBoardMat,scale(1,boardHeight(7,3),1)*translate(-75,0,-125))
board.add(square,blackBoardMat,scale(1,boardHeight(7,4),1)*translate(-25,0,-125))
board.add(square,whiteBoardMat,scale(1,boardHeight(7,5),1)*translate(25,0,-125))
board.add(square,blackBoardMat,scale(1,boardHeight(7,6),1)*translate(75,0,-125))
board.add(square,whiteBoardMat,scale(1,boardHeight(7,7),1)*translate(125,0,-125))
board.add(square,blackBoardMat,scale(1,boardHeight(7,8),1)*translate(175,0,-125))

board.add(square,blackBoardMat,scale(1,boardHeight(8,1),1)*translate(-175,0,-175))
board.add(square,whiteBoardMat,scale(1,boardHeight(8,2),1)*translate(-125,0,-175))
board.add(square,blackBoardMat,scale(1,boardHeight(8,3),1)*translate(-75,0,-175))
board.add(square,whiteBoardMat,scale(1,boardHeight(8,4),1)*translate(-25,0,-175))
board.add(square,blackBoardMat,scale(1,boardHeight(8,5),1)*translate(25,0,-175))
board.add(square,whiteBoardMat,scale(1,boardHeight(8,6),1)*translate(75,0,-175))
board.add(square,blackBoardMat,scale(1,boardHeight(8,7),1)*translate(125,0,-175))
board.add(square,whiteBoardMat,scale(1,boardHeight(8,8),1)*translate(175,0,-175))


## For kings and queens and bishops and knights.
goldMat=Material().color((0.8,0.7,0)).diffuse(1).reflection(0.3).specularity(1).roughness(0.05)

## These were used to dress the Queen's collar, which has 6 cutouts.
## Could have been used to motivate a hue-related question, but red looked
## too classy to avoid.
shinyRed=Material().color(red).diffuse(1).reflection(0.3).specularity(0.9).roughness(0.05)

## The following not used and should be updated to be similar to red.
shinyYellow=Material().color(yellow).diffuse(1).reflection(0.5).specularity(0.9).roughness(0.05)
shinyGreen=Material().color(green).diffuse(1).reflection(0.5).specularity(0.9).roughness(0.05)

shinyCyan=Material().color(cyan).diffuse(1).reflection(0.5).specularity(0.9).roughness(0.05)
shinyBlue=Material().color(blue).diffuse(1).reflection(0.5).specularity(0.9).roughness(0.05)
shinyMagenta=Material().color(magenta).diffuse(1).reflection(0.5).specularity(0.9).roughness(0.05)
silverMat=Material().color(white).diffuse(1).reflection(0.5).specularity(0.9).roughness(0.05)
## unit-sized shapes.
## these are nice because we can scale them to be exactly the size (in units) we desire.
## they all remain around the origin.
unitCylinder=Cylinder().scale(0.01)
unitSphere = Sphere().scale(0.01)
unitCube = Cube().scale(0.01)

## constants of the known universe
## width of a pawn
narrow = 15
narrowR = narrow/2
## width of a queen
medium = 18
mediumR = medium/2

## inset of bevel on base
baseInset=1
## total thickness of lowest base
baseHeight=3
## artifact
baseThickness=baseHeight - (2*baseInset)

## OL=outline
## Outlines for base spindle objects
narrowBaseOL = raisePoly([[0,0],[narrowR,0],[narrowR,baseInset+baseThickness],[narrowR-baseThickness,baseHeight],[0,baseHeight]])
mediumBaseOL = raisePoly([[0,0],[mediumR,0],[mediumR,baseInset+baseThickness],[mediumR-baseThickness,baseHeight],[0,baseHeight]])

## Base proper for pawns, rooks, bishops, knights.
narrowBase=Spindle().profile(narrowBaseOL)

## The royalty base.
mediumBase=Spindle().profile(mediumBaseOL)

## Knee is the torus that sits on the base.
## I think this detracts from the design, but we're out of time.
kneeHeight=4

## The knee proper.  This torus maxes out 2 units (minor radius) from the perimeter -
## this will be important when we make the torso.
narrowKnee=Torus().minor(kneeHeight/2).major(narrowR-kneeHeight/2).translate(0,kneeHeight/2,0)
mediumKnee=Torus().minor(kneeHeight/2).major(mediumR-kneeHeight/2).translate(0,kneeHeight/2,0)

## The torso is the sweeping section from the "shoulder" to the "knee".
## At this point, the easiest construction technique is to subtract
## a torus (a donut with a hole) from a cylinder.
## For the torus we use the lower half.  The queen's collar uses a portion of
## the top half of a similar structure.
pawnTorsoHeight=5 # total rise
narrowTorsoTorus=Torus().minor(4).major(5.5).scale(1,pawnTorsoHeight/4,1).translate(0,pawnTorsoHeight,0)

## The torso proper.
## The cylinder sits on the lower half of the torus with rim consistent with
## the circular base of the torus.
narrowTorso=Difference().add(unitCylinder,translate(0,0.5,0)*scale(11,pawnTorsoHeight,11)).add(narrowTorsoTorus)

## The shoulder for the pawn.  Needs more care in design.
## Ideally, we'd use bezier lathes, but not yet...
narrowShoulderOL=raisePoly([[0,0],[4,0],[4,1.5],[2.5,2.5],[0,2.5]])
narrowShoulder=Spindle().profile(narrowShoulderOL)

## Pawn head.
pawnHead=Sphere().scale(0.08).translate(0,4,0)

## Entire pawn.
pawn=Group().add(narrowBase).add(narrowKnee,translate(0,baseHeight,0))
pawn.add(narrowTorso,translate(0,baseHeight+kneeHeight,0))
pawn.add(narrowShoulder,translate(0,baseHeight+kneeHeight+pawnTorsoHeight,0))
pawn.add(pawnHead,translate(0,14,0))
pawn.scale(pieceScale)

## Specialized shape scenes
## Two lights (exam question), offset for visibility. (more lights is too bright)
lighting=Group().add(bulb,translate(200,400,-400))
lighting.add(bulb,translate(-200,400,400))

## A stage for viewing individual parts
stage=Plane().material(whiteBoardMat)
pawn_scene=Group().add(lighting).add(stage).add(pawn,whitePieceMat)
pawnCam=Camera().subject(pawn_scene).pos((0,30,-200)).COI((0,35,0)).image(image).angle(30)
image.antiAlias(1)
pawnCam.shoot()

## rook
## see pawn for parallel comments
## torso
rookTorsoHeight=12
rookTorsoTorus=Torus().minor(2).major(5.5).scale(1,rookTorsoHeight/2,1).translate(0,rookTorsoHeight,0)
rookTorso=Difference()
rookTorso.add(unitCylinder,translate(0,0.5,0)*scale(11,rookTorsoHeight,11))
rookTorso.add(rookTorsoTorus)

## shoulder
rookShoulderHeight=3
rookShoulderOL=raisePoly(((0,0),(3.5,0),(5.5,2),(5.5,3),(0,3)))
rookShoulder=Spindle().profile(rookShoulderOL)

## basis for exam question on CSG
rookHead=Difference()
rookHead.add(unitCylinder,translate(0,0.5,0)*scale(12,3,12))
rookHead.add(unitSphere,scale(10,5,10)*translate(0,3,0))
rookHead.add(unitCube,scale(13,3,2)*translate(0,3,0))
rookHead.add(unitCube,scale(2,3,13)*translate(0,3,0))

## a total rook
rook=Group()
rook.add(narrowBase)
rook.add(narrowKnee,translate(0,baseHeight,0))
rook.add(rookTorso,translate(0,baseHeight+kneeHeight,0))
rook.add(rookShoulder,translate(0,baseHeight+kneeHeight+rookTorsoHeight,0))
rook.add(rookHead,translate(0,baseHeight+kneeHeight+rookTorsoHeight+rookShoulderHeight,0))
rook.scale(pieceScale)

rook_scene=Group()
rook_scene.add(lighting)
rook_scene.add(stage)
rook_scene.add(rook,translate(-25,0,0)*yRot(45),blackPieceMat)
rook_scene.add(rook,translate(25,0,15)*yRot(-45),whitePieceMat)

rookCam=Camera().subject(rook_scene).pos((0,100,-200)).COI((0,35,0)).image(image).angle(40)

rookCam.shoot()

## Knight
## See pawn for parallel comments
## torso
knightTorsoHeight=12
knightTorsoTorus=Torus().minor(2).major(5.5).scale(1,knightTorsoHeight/2,1).translate(0,knightTorsoHeight,0)
knightTorso=Difference()
knightTorso.add(unitCylinder,translate(0,0.5,0)*scale(11,knightTorsoHeight,11))
knightTorso.add(knightTorsoTorus)

## total, unabashed surrender....
teapot=Teapot()
teapot.translate(4,0,0).yRot(90).scale(0.01)
# this centers the base (and tippy-top) of the standard teapot at origin

## Head = teapot plus royal bobble
knightHead=Group()
knightHead.add(teapot,scale(20))
knightHead.add(unitSphere,goldMat,scale(3)*translate(0,9,0))

## knight proper: faces camera
knight=Group()
knight.add(narrowBase)
knight.add(narrowKnee,translate(0,baseHeight,0))
knight.add(knightTorso,translate(0,baseHeight+kneeHeight,0))
knight.add(knightHead,translate(0,baseHeight+kneeHeight+knightTorsoHeight,0))
knight.scale(pieceScale)

knight_scene=Group()
knight_scene.add(lighting)
knight_scene.add(stage)
knight_scene.add(knight,yRot(90),whitePieceMat)

knightCam=Camera()
knightCam.subject(knight_scene).pos((0,100,-200)).COI((0,40,0)).image(image).angle(40)

knightCam.shoot()

## Bishop
## See pawn for parallel commentary
## torso
bishopTorsoHeight=10
bishopTorsoTorus=Torus().minor(2).major(5.5).scale(1,bishopTorsoHeight/2,1)
bishopTorsoTorus.translate(0,bishopTorsoHeight,0)
bishopTorso=Difference()
bishopTorso.add(unitCylinder,translate(0,0.5,0)*scale(11,bishopTorsoHeight,11))
bishopTorso.add(bishopTorsoTorus)

## royal-types have a "shoulder"
bishopShoulderHeight=3.5
bishopShoulderOL=raisePoly(((0,0),(5.5,0),(6,1),(5.0,1.5),(5.0,3),(4.0,3.5),(4.0,4.5),(4.5,5),(4.5,6),(0,6)))
bishopShoulder=Spindle().profile(bishopShoulderOL)

## This could be the basis for an exam question.  What is used to cut the gash?
bishopHead=Difference()
bishopHead.add(unitSphere,translate(0,0.5,0)*scale(9,12,9))
bishopHead.add(unitCube,translate(-0.5,0.5,0)*scale(11,0.75,11)*zRot(-50)*translate(-0.5,7,0)*yRot(-90))
bishopCap=Sphere().scale(0.03,0.02,0.03).material(goldMat)

## The entire dude.  Faces camera.
bishop=Group()
bishop.add(narrowBase)
bishop.add(narrowKnee,translate(0,baseHeight,0))
bishop.add(bishopTorso,translate(0,baseHeight+kneeHeight,0))
bishop.add(bishopShoulder,translate(0,baseHeight+kneeHeight+bishopTorsoHeight,0))
bishop.add(bishopHead,translate(0,baseHeight+kneeHeight+bishopTorsoHeight+bishopShoulderHeight,0))
bishop.add(bishopCap,translate(0,33,0))
bishop.scale(pieceScale)

bishop_scene=Group().add(lighting).add(stage).add(bishop,yRot(90),whitePieceMat)

bishop_shoulder_scene=Group().add(lighting).add(stage).add(bishopShoulder,whitePieceMat)

bishopCam=Camera().subject(bishop_scene).pos((0,30,-200)).COI((0,40,0)).image(image).angle(40)

bishopShoulderCam=Camera().subject(bishop_shoulder_scene).pos((0,50,-200)).COI((0,0,0)).image(image).angle(10)

bishopCam.shoot()
bishopShoulderCam.shoot()

## Queen - the royal pain.
## See pawn for commentary on torsos
queenTorsoHeight=14
queenTorsoTorus=Torus().minor(3).major(7).scale(1,queenTorsoHeight/3,1).translate(0,queenTorsoHeight,0).scale(1,.9,1)
queenTorso=Difference()
queenTorso.add(unitCylinder,translate(0,0.5,0)*scale(14,queenTorsoHeight,14))
queenTorso.add(queenTorsoTorus)

## standard shoulder
queenShoulderHeight=6
queenShoulderOL=raisePoly(((0,0),(6.5,0),(7,1),(6.0,1.5),(6.0,3),(5.0,3.5),(5.0,4.5),(5.5,5),(5.5,6),(0,6)))
queenShoulder=Spindle().profile(queenShoulderOL)

## construction of the "collar".
## too complicated for an exam question, but wonderful design
queenCollarTorus=Torus().minor(5).major(9).scale(1,7/5,1)
queenCollarA=Difference()
queenCollarA.add(unitCylinder,translate(0,0.5,0)*scale(14,6,14))
queenCollarA.add(queenCollarTorus)

## this cylinder is used to notch collar.  We make use of the knowledge
## that six pennies exactly circumnavigate a seventh
cy=Cylinder().scale(0.01,1,0.01).scale(9,1,9).translate(0,0,9)

## To hollow out the collar, we subtract from self
queenCollar=Difference()
queenCollar.add(queenCollarA)
queenCollar.add(queenCollarA,scale(0.95,1.01,0.95)) # 1.01 to drill through
queenCollar.add(cy,shinyRed) # purdy
queenCollar.add(cy,yRot(60),shinyRed)
queenCollar.add(cy,yRot(120),shinyRed)
queenCollar.add(cy,yRot(180),shinyRed)
queenCollar.add(cy,yRot(-60),shinyRed)
queenCollar.add(cy,yRot(-120),shinyRed)

## head
queenHead=Group()
queenHead.add(queenCollar)
queenHead.add(unitSphere,scale(9,10,9)*translate(0,6,0))
queenHead.add(unitSphere,goldMat,scale(3,3,3)*translate(0,11,0))

## her magesticness
queen=Group()
queen.add(mediumBase)
queen.add(mediumKnee,translate(0,baseHeight,0))
queen.add(queenTorso,translate(0,baseHeight+kneeHeight,0))
queen.add(queenShoulder,translate(0,baseHeight+kneeHeight+queenTorsoHeight,0))
queen.add(queenHead,translate(0,baseHeight+kneeHeight+queenTorsoHeight+queenShoulderHeight,0))
queen.scale(pieceScale)

queen_scene=Group().add(lighting).add(stage).add(queen,whitePieceMat)
queenCam=Camera().subject(queen_scene).pos((0,200,-200)).COI((0,65,0)).image(image).angle(10)
queenCam.shoot()

## King
## See queen and pawn for comments.
## Queen from the shoulders down
kingTorsoHeight=14
kingTorsoTorus=Torus().minor(3).major(7).scale(1,kingTorsoHeight/3,1).translate(0,kingTorsoHeight,0).scale(1,.9,1)
kingTorso=Difference()
kingTorso.add(unitCylinder,translate(0,0.5,0)*scale(14,kingTorsoHeight,14))
kingTorso.add(kingTorsoTorus)

kingShoulderHeight=6
kingShoulderOL=raisePoly(((0,0),(6.5,0),(7,1),(6.0,1.5),(6.0,3),(5.0,3.5),(5.0,4.5),(5.5,5),(5.5,6),(0,6)))
kingShoulder=Spindle().profile(kingShoulderOL)

## He's a block-, no lathe-head.
kingHeadOL=raisePoly(((0,0),(4,0),(6,6),(6,8),(0,11)))
kingHeadL=Spindle().profile(kingHeadOL)

## Pretty nice, if I do say so.
crossOL=translate(0,0,-1).mapPoly(raisePoly(((0,0),(2,0),(1,2),(3,1),(4,3),(3,5),(1,4),(2,6),(0,7),(-2,6),(-1,4),(-3,5),(-4,3),(-3,1),(-1,2),(-2,0),(0,0))))
cross=extrude(crossOL,translate(0,0,2)) ## basis for exam question

## head
kingHead=Group()
kingHead.add(kingHeadL)
kingHead.add(unitSphere,goldMat,scale(4,3,4)*translate(0,11,0))
kingHead.add(cross,goldMat,scale(0.75)*translate(0,12,0))

## The man
king=Group()
king.add(mediumBase)
king.add(mediumKnee,translate(0,baseHeight,0))
king.add(kingTorso,translate(0,baseHeight+kneeHeight,0))
king.add(kingShoulder,translate(0,baseHeight+kneeHeight+kingTorsoHeight,0))
king.add(kingHead,translate(0,baseHeight+kneeHeight+kingTorsoHeight+queenShoulderHeight,0))
king.scale(pieceScale)

## The board with all pieces set up.
## black pieces face naturally, white pieces must turn about.
game=Group()
game.add(board)
game.add(rook,blackPieceMat,translate(-175,50*boardHeight(1,1),175))
game.add(knight,blackPieceMat,translate(-125,50*boardHeight(1,2), 175))
game.add(bishop,blackPieceMat,translate(-75 ,50 *boardHeight(1,3), 175))
game.add(queen,blackPieceMat,translate(-25,50*boardHeight(1,4),175))
game.add(king,blackPieceMat,translate(25,50*boardHeight(1,5),175))
game.add(bishop,blackPieceMat,translate(75,50*boardHeight(1,6),175))
game.add(knight,blackPieceMat,translate(125,50*boardHeight(1,7),175))
game.add(rook,blackPieceMat,translate(175,50*boardHeight(1,8),175))
game.add(pawn,blackPieceMat,translate(-175,50*boardHeight(2,1),125))
game.add(pawn,blackPieceMat,translate(-125,50*boardHeight(2,2),125))
game.add(pawn,blackPieceMat,translate(-75,50*boardHeight(2,3),125))
game.add(pawn,blackPieceMat,translate(-25,50*boardHeight(2,4),125))
game.add(pawn,blackPieceMat,translate(25,50*boardHeight(2,5),125))
game.add(pawn,blackPieceMat,translate(75,50*boardHeight(2,6),125))
game.add(pawn,blackPieceMat,translate(125,50*boardHeight(2,7),125))
game.add(pawn,blackPieceMat,translate(175,50*boardHeight(2,8),125))
  
game.add(rook,whitePieceMat,yRot(180)*translate(-175,50*boardHeight(8,1),-175))
game.add(knight,whitePieceMat,yRot(180)*translate(-125,50*boardHeight(8,2),-175))
game.add(bishop,whitePieceMat,yRot(180)*translate(-75,50*boardHeight(8,3),-175))
game.add(queen,whitePieceMat,yRot(180)*translate(-25,50*boardHeight(8,4),-175))
game.add(king,whitePieceMat,yRot(180)*translate(25,50*boardHeight(8,5),-175))
game.add(bishop,whitePieceMat,yRot(180)*translate(75,50*boardHeight(8,6),-175))
game.add(knight,whitePieceMat,yRot(180)*translate(125,50*boardHeight(8,7),-175))
game.add(rook,whitePieceMat,yRot(180)*translate(175,50*boardHeight(8,8),-175))
game.add(pawn,whitePieceMat,yRot(180)*translate(-175,50*boardHeight(7,1),-125))
game.add(pawn,whitePieceMat,yRot(180)*translate(-125,50*boardHeight(7,2),-125))
game.add(pawn,whitePieceMat,yRot(180)*translate(-75,50*boardHeight(7,3),-125))
game.add(pawn,whitePieceMat,yRot(180)*translate(-25,50*boardHeight(7,4),-125))
game.add(pawn,whitePieceMat,yRot(180)*translate(25,50*boardHeight(7,5),-125))
game.add(pawn,whitePieceMat,yRot(180)*translate(75,50*boardHeight(7,6),-125))
game.add(pawn,whitePieceMat,yRot(180)*translate(125,50*boardHeight(7,7),-125))
game.add(pawn,whitePieceMat,yRot(180)*translate(175,50*boardHeight(7,8),-125))

## main scene
scene=Group()
scene.add(lighting)
scene.add(game,translate(0,-50,0)*scale(0.75))

royal_scene=Group().add(lighting).add(stage)
royal_scene.add(queen,whitePieceMat,translate(0,0,0))
royal_scene.add(king,whitePieceMat,translate(50,0,0))
royal_scene.add(king,blackPieceMat,yRot(90)*translate(-50,0,0))

## Specialized cameras (mainCam is probably unnecessary).
mainCam=Camera().COI((0,0,0)).subject(scene).image(image).angle(60).pos((300,100,-100))

royalCam=Camera().subject(royal_scene).pos((0,100,-200)).image(image).COI((0,50,0))

royalCam.shoot()
mainCam.shoot()
