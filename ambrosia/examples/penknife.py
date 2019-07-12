# Exam Model 1 for (c) 2007,2013 (converted for use with Mead) Duane A. Bailey
# Converted to ambrosia 3/2013
from ambrosia import *

image.background(hsv2rgb((240,.5,.5)))
# image.debug(True).keep(True) # uncomment this line to access POV file
image.antiAlias(1) # smooth

profile = Camera().image(image)
detail1 = Camera().image(image)
detail2 = Camera().image(image)
chalk_cam = Camera().image(image)
pencil_cam = Camera().image(image)
fount_cam = Camera().image(image)
pen_cam = Camera().image(image)
pilot_cam = Camera().image(image)
shell_cam = Camera().image(image)

bulb = Light().intensity(.5).color(white)

# ;; the attachment
attachment_mat = Material().color(white).type("plastic")
attachment_mat.specularity(.7).reflection(.5)

table_mat = Material().color(hsv2rgb((0,0.05,1)))
table_mat.specularity(0).reflection(.5).roughness(0.05)

attachment0 = Difference()
attachment0.add(cone,scale(2),attachment_mat)
attachment0.add(cylinder,zRot(90)*scale(2)*scale(1,.1,.2))
attachment0.add(cylinder,xRot(-90)*scale(2)*scale(.9,2,1)*translate(100,100,0))
attachment0.add(cylinder,xRot(-90)*scale(2)*scale(.9,2,1)*translate(-100,100,0))

attachment = Intersection()
attachment.add(attachment0)
attachment.add(sphere,scale(2)*scale(1,1.5,1)*translate(0,-100,0))
attachment.translate(0,100,0)
attachment.scale(1,2,1)
attachment.xRot(90)

# ;;;;;;
# ;; holder
case_mat = Material().type("plastic").color((.85,0,0)).specularity(.1).reflection(.1)

emblem0 = Difference()
emblem0.add(cylinder,scale(2)*scale(.2,0.05,.25),attachment_mat)
emblem0.add(cylinder,scale(2)*scale(.18,1,.23),attachment_mat)

emblem1 = Group()
emblem1.add(emblem0)
emblem1.add(cube,scale(2)*scale(.14,0.05,0.03),attachment_mat)
emblem1.add(cube,scale(2)*scale(.03,0.05,0.14),attachment_mat)

emblem = Difference().add(emblem1).add(cube,scale(2)*translate(0,-100,0))


case_half0 = Group()
case_half0.add(cylinder,xRot(-90)*scale(2)*scale(.3,.1,1),case_mat)
case_half0.add(sphere,scale(.3,.1,.2)*scale(2)*translate(0,0,-100),case_mat)
case_half0.add(sphere,scale(.3,.1,.2)*scale(2)*translate(0,0,100),case_mat)

case_half1 = Difference()
case_half1.add(case_half0)
case_half1.add(cube,scale(2)*scale(1,1,2)*translate(0,105,0))

case_half2 = Group()
case_half2.add(case_half1)
case_half2.add(emblem,translate(0,1,30))

case_half = Difference()
case_half.add(case_half2)
case_half.add(cube,scale(2)*scale(1,1,2)*translate(0,-100,0))

case = Group()
case.add(case_half,zRot(90)*translate(-8,0,0))
case.add(case_half,zRot(-90)*translate(8,0,0))

# ;;;;;;;;;;;;;;;;;;;
# ; Pencil
pencil_yellow_mat = Material().type("plastic").color((1,1,.13)).specularity(0.1)

pencil_wood_mat = Material().type("plaster").color(hsv2rgb((30,.61,.9))).specularity(0)

pencil_graphite_mat = Material().type("plastic").color((.2,.2,.2)).specularity(0.1)

pencil_outline = translate(0,0,-100)(raisePoly(polygon(6,25)))

pencil_shell = extrude(pencil_outline,translate(0,0,200))

pencil0 = Group()
pencil0.add(pencil_shell,pencil_yellow_mat)
pencil0.add(pencil_shell,scale(.98,.98,.98),pencil_wood_mat)
pencil0.add(cylinder,scale(2)*scale(0.06,1.1,0.06)*xRot(-90),pencil_graphite_mat)

pencil1 = Intersection()
pencil1.add(pencil0)
pencil1.add(cone,scale(2)*scale(0.65,1,0.65)*xRot(-90))

pencil = Group()
pencil.add(pencil1)
pencil.add(attachment,scale(.25,.25,.2)*translate(0,0,100),attachment_mat)
pencil.scale(.6,.6,1).translate(0,0,-160)

# ;;;;;;;;;;;;;;;;;;;
# ; Pilot point
pilot_plastic_mat = Material()
pilot_plastic_mat.color((0.929412,0.0941176,0.117647)).type("plastic").specularity(.1)

pilot_ink_mat = Material()
pilot_ink_mat.color((0.929412,0.0941176,0.117647)).type("plaster").specularity(.1)

pilot_metal_mat = Material()
pilot_metal_mat.color(white).type("plastic").specularity(0.3)

outline = [[0,-80,0]] + (scale(0.06,.8,1)*translate(-12,0,0))(raisePoly([[-6.39758e-05,-100],[16.4594,-98.6361],[32.4699,-94.5817],[47.5947,-87.9474],[61.4212,-78.9141],[73.5724,-67.7282],[83.7166,-54.6948],[91.5773,-40.1696],[96.94,-24.5486],[99.6584,-8.25795],[99.6584,8.25793]])) + [[0,6.6,0]]
pilot_grip_base = sweep(outline,20)
#pilot_grip_base = sweep(outline,50) # this can be very slow; ultimately -> spindle

pilot_grip = Difference()
pilot_grip.add(pilot_grip_base,translate(0,80,0)*xRot(-90),pilot_plastic_mat)
pilot_grip.add(cube,scale(2)*translate(0,0,-100)*scale(1,1,3)*translate(0,0,-50))

pilot_nose0 = Group()
pilot_nose0.add(cylinder,scale(2)*translate(0,100,0)*scale(0.06,0.02,0.06),pilot_metal_mat)
pilot_nose0.add(cone,scale(2)*translate(0,100,0)*scale(0.06,0.10,0.06)*translate(0,4,0),pilot_metal_mat)

pilot_nose1 = Difference()
pilot_nose1.add(pilot_nose0)
pilot_nose1.add(cylinder,scale(2)*translate(0,110,0))

pilot_nose = Group()
pilot_nose.add(pilot_nose1)
pilot_nose.add(cylinder,scale(2)*translate(0,100,0)*scale(0.02,0.08,0.02),pilot_metal_mat)
pilot_nose.add(sphere,scale(2)*translate(0,100,0)*scale(0.015,0.10,0.015),pilot_ink_mat)

pilot0 = Difference()
pilot0.add(sphere,scale(2)*scale(.167,.167,2)*translate(0,0,100),pilot_plastic_mat)
pilot0.add(cube,scale(2)*translate(0,0,200))
pilot0.add(cube,scale(2)*translate(0,0,-100)*scale(1,1,2)*translate(0,0,-33))

pilot = Group()
pilot.add(pilot0)
pilot.add(pilot_grip,translate(0,0,-33),pilot_plastic_mat)
pilot.add(pilot_nose,xRot(-90)*scale(.8,.8,1)*translate(0,0,-80))
pilot.add(attachment,scale(.167,.167,.2)*translate(0,0,100),attachment_mat)
pilot.translate(0,0,-160)

# ;;;;;;;;
# ;; Montblanc

mb_plastic_mat = Material().type("plastic").color(black).specularity(.2)

mb_inker_mat = Material().type("plaster").color(black).specularity(.1)

mb_metal_mat = Material().type("plastic").color((1,0.8405,0.13)).specularity(.2).reflection(0.3)

mb_nib_mat = Material().type("plastic").color((.75,.75,.8)).specularity(0.3).reflection(0.5)

montblanc0 = Difference()
montblanc0.add(sphere,scale(2)*scale(.19,.19,2)*translate(0,0,100),mb_plastic_mat)
montblanc0.add(cube,scale(2),translate(0,0,200))
montblanc0.add(cube,scale(2)*translate(0,0,-100)*scale(1,1,2)*translate(0,0,-25))

montblanc1 = Group()
montblanc1.add(montblanc0)
montblanc1.add(cone,scale(2)*xRot(-90)*translate(0,0,-100)*scale(.15,.15,.375)*translate(0,0,-25),mb_metal_mat)

montblanc2 = Difference()
montblanc2.add(montblanc1)
montblanc2.add(cone,scale(2)*xRot(-90)*translate(0,0,-100)*scale(.15,.15,.375)*translate(0,0,-18))
montblanc2.add(cube,scale(2)*translate(0,0,-180))

montblanc = Group()
montblanc.add(montblanc2)
montblanc.add(attachment,scale(.19,.19,.20)*translate(0,0,100),attachment_mat)
montblanc.translate(0,0,-160)

inkercyl = Group()
inkercyl.add(cylinder,scale(2)*xRot(-90)*scale(.1,0.05,0.01))

inker = Group()
for d in [-5,-10,-15,-20,-25,-30,-35]:
    inker.add(inkercyl,translate(0,0,d))

well = Intersection()
well.add(inker)
well.add(cone,scale(2)*xRot(90)*translate(0,0,-53)*scale(.2,.1,.5)*xRot(-8)*translate(0,2,0))

nibcone = Difference()
nibcone.add(cone,scale(2)*xRot(90)*translate(0,0,-50)*scale(.2,.1,.5))
nibcone.add(cone,scale(2)*xRot(90)*translate(0,0,-53)*scale(.2,.1,.5))

nibtop = Difference()
nibtop.add(nibcone,xRot(-8)*translate(0,2,0))
nibtop.add(cube,scale(2)*translate(0,0,100))
nibtop.add(cube,scale(2)*translate(0,-100,0))
nibtop.add(cube,scale(2)*translate(0,0,-165))

nib = Difference()
nib.add(nibtop,mb_nib_mat)
nib.add(cylinder,scale(2)*scale(.18,1,.35)*translate(20,0,-75))
nib.add(cylinder,scale(2)*scale(.18,1,.35)*translate(-20,0,-75))
nib.add(cylinder,scale(2)*scale(0.02,1,0.02)*translate(0,0,-30))
nib.add(cube,scale(2)*translate(0,0,-100)*scale(0.005,1,0.25)*translate(0,0,-30))

fountblanc0 = Difference()
fountblanc0.add(cone,scale(2)*xRot(-90)*translate(0,0,-100)*scale(.19,.19,2.81)*translate(0,0,100),mb_plastic_mat)
fountblanc0.add(cube,scale(2)*translate(0,0,-100)*scale(1,1,3)*translate(0,0,-25))

fountblanc = Group()
fountblanc.add(fountblanc0)
fountblanc.add(cylinder,scale(2)*xRot(-90)*translate(0,0,-100)*scale(.16,.16,.02)*translate(0,0,-25),mb_metal_mat)
fountblanc.add(cylinder,scale(2)*xRot(-90)*translate(0,0,100)*scale(.19,.19,.02)*translate(0,0,50),mb_metal_mat)
fountblanc.add(nib,translate(0,0,-20))
fountblanc.add(attachment,scale(.19,.19,.20)*translate(0,0,100),attachment_mat)
fountblanc.translate(0,0,-160)

# ;;;;;;
# ;; chalk
chalk_mat = Material().type("plaster").color((.8,.8,.8)).specularity(0)

chalk0 = Difference()
chalk0.add(cylinder,scale(2)*xRot(-90)*scale(.2,.2,1),chalk_mat)
chalk0.add(cube,scale(2)*translate(100,0,0)*yRot(70)*translate(0,0,-100))
chalk0.add(cube,scale(2)*translate(-100,0,0)*yRot(-30)*zRot(10)*translate(0,0,-100))
chalk0.add(cube,scale(2)*translate(0,100,0)*xRot(-45)*zRot(10)*translate(0,0,-100))

chalk = Group()
chalk.add(chalk0)
chalk.add(attachment,scale(.2)*translate(0,0,100),attachment_mat)
chalk.translate(0,0,-160)

# ;; Tootsie Roll Pop
# ;;
orange = hsv2rgb((30,1,1))
tang = Material().color(orange).transparency(0.5).reflection(0).refraction(1.5).diffuse(.9).specularity(0).roughness(1)
                  
pop0 = Group()
pop0.add(sphere,scale(.9),tang)
pop0.add(cylinder,scale(1.1,.45,1.1)*zRot(-90),tang)
pop0.add(cylinder,translate(0,-50,0)*scale(.16,4,.16),whitePlaster)
pop0.yRot(45).translate(0,200,0).scale(.5).xRot(-90)

pop = Group()
pop.add(pop0)
pop.add(attachment,scale(.04,0.04,.2)*translate(0,0,100),attachment_mat)
pop.translate(0,0,-160)

# ;; SETUP
lights = Group()
lights.add(bulb,translate(150,200,0))
lights.add(bulb,translate(-150,200,0))
lights.add(bulb,translate(0,200,-200))
lights.add(cube,scale(2)*scale(10,.1,10)*translate(0,-50,0),table_mat)

scene.clear()
scene.add(lights)
scene.add(chalk,translate(-4,0,0)*xRot(135)*translate(0,0,100))
scene.add(pencil,translate(4,0,0)*xRot(75)*translate(0,0,100))
scene.add(montblanc,xRot(5)*translate(0,0,-100))
scene.add(pilot,translate(-4,0,0)*xRot(50)*translate(0,0,-100))
scene.add(pop,translate(-4,0,0)*xRot(100)*translate(0,0,-100))
scene.add(case)

chalk_scene = Group().add(chalk).add(lights)

pencil_scene = Group().add(pencil,xRot(5)*yRot(30)).add(lights)

pen_scene = Group().add(montblanc).add(lights)

fount_scene = Group().add(pop,yRot(-30)).add(lights)

pilot_scene = Group().add(pilot,yRot(30)).add(lights)

shell_scene = Group().add(case).add(lights)

scene1 = Group().add(fountblanc,translate(-50,0,0)).add(montblanc,translate(50,0,0))


# position cameras
chalk_cam.pos((-647.17,173.409,-150)).direction((0.965926,-0.258819,0)).subject(chalk_scene).angle(45)
fount_cam.pos((-77.0463,230.693,-516.251)).direction((0.200633,-0.557597,0.805501)).subject(fount_scene).angle(45)
pen_cam.pos((0,50,-500)).COI((0,0,0)).subject(pen_scene).angle(45)
pencil_cam.pos((-647.17,173.409,-150)).direction((0.965926,-0.258819,0)).subject(pencil_scene).angle(45)
pilot_cam.pos((-516.77,138.468,-135)).direction((0.965926,-0.258819,-9.76048e-10)).subject(pilot_scene).angle(45)
shell_cam.pos((-150,50,-400)).COI(origin).subject(shell_scene).angle(45)
profile.pos((-671.746,760.519,-1163.47)).COI((0,100,0)).subject(scene).angle(35)
detail1.pos((-361.84,156.462,-686.702)).direction((0.499388,0.0499387,0.864938)).subject(scene).angle(54)
detail2.pos((0,0,-500)).direction((0,0,1)).subject(scene).angle(45)


# Shoot images
pilot_cam.shoot()
chalk_cam.shoot()
fount_cam.shoot()
pencil_cam.shoot()
shell_cam.shoot()
profile.shoot()
detail1.shoot()

