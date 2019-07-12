; Exam Model 1 for (c) 2007 (converted for use with Mead) Duane A. Bailey
; (pick-color)
(require (lib "Defs.ss" "Mead"))

(tell image (background (hsv2rgb '(240 .5 .5))))
(tell image (keep #t) (debug #t))
(object profile Camera
        (image image))
(object detail1 Camera (image image))
(object detail2 Camera(image image))
(object chalk-cam Camera(image image))
(object pencil-cam Camera(image image))
(object fount-cam Camera(image image))
(object pen-cam Camera(image image))
(object pilot-cam Camera(image image))
(object shell-cam Camera(image image))


(object bulb Light
  (intensity .5)
  (color white)
  )

;;;;;;
;; the attachment to the knife

(object attachment-mat Material
  (color white)
  (type 'plastic)
  (specularity 0.7)
  (reflection 0.5)
  )
(object table-mat Material
  (color (hsv2rgb '(0 .05 1)))
  (specularity 0)
  (reflection .5)
  (roughness 0.05)
  )

(object attachment0 Difference
  (add cone (scale 2 2 2) attachment-mat)
  (add cylinder (compose (zRot 90) (scale 2 2 2) (scale 1 .1 .2) (translate 0 0 0)))
  (add cylinder (compose (xRot -90) (scale 2 2 2) (scale .9 2 1) (translate 100 100 0)))
  (add cylinder (compose (xRot -90) (scale 2 2 2) (scale .9 2 1) (translate -100 100 0)))
  )
(object attachment Intersection
  (add attachment0)
  (add sphere (compose (scale 2 2 2) (scale 1 1.5 1) (translate 0 -100 0)))
  (translate 0 100 0)
  (scale 1 2 1)
  (xRot 90)
  )


;;;;;;
;; holder
;; (pick-color)
(object case-mat Material
  (type 'plastic)
  (color '(.85 0 0))
  (specularity .1)
  (reflection .1)
  )
(object emblem0 Difference
  (add cylinder (scale 2 2 2) (scale .2 .05 .25) attachment-mat)
  (add cylinder (scale 2 2 2) (scale .18 1 .23) attachment-mat)
  )
(object emblem1 Group
  (add emblem0)
  (add cube     (scale 2 2 2) (scale .14 .05 .03) attachment-mat)
  (add cube     (scale 2 2 2) (scale .03 .05 .14) attachment-mat)
  )
(object emblem Difference
  (add emblem1)
  (add cube (scale 2 2 2) (translate 0 -100 0))
  )

(object case-half0 Group
  (add cylinder (compose (xRot -90) (scale 2 2 2) (scale .3 .1 1)) case-mat)
  (add sphere   (compose (scale .3 .1 .2) (scale 2 2 2) (translate 0 0 -100)) case-mat)
  (add sphere   (compose (scale .3 .1 .2) (scale 2 2 2) (translate 0 0 100)) case-mat)
  )
(object case-half1 Difference
  (add case-half0)
  (add cube (compose (scale 2 2 2) (scale 1 1 2) (translate 0 105 0)))
  )
(object case-half2 Group
  (add case-half1)
  (add emblem (translate 0 1 30))
  )
(object case-half Difference
  (add case-half2)
  (add cube (compose (scale 2 2 2) (scale 1 1 2) (translate 0 -100 0)))
  )

(object case Group
  (add case-half (compose (zRot 90) (translate -8 0 0)))
  (add case-half (compose (zRot -90) (translate 8 0 0)))
  )



;;;;;;;;;;;;;;;;;;;
; Pencil
; (pick-color)

(object pencil-yellow-mat Material
  (type 'plastic)
  (color '(1 1 .13))
  (specularity 0.1)
  )

(object pencil-wood-mat Material
  (type 'plaster)
  (color (hsv2rgb '(30 .61 .9)))
  (specularity 0)
  )

(object pencil-graphite-mat Material
  (type 'plastic)
  (color '(.2 .2 .2))
  (specularity 0.1)
  )

(define pencil-outline (polyXform (2to3d (polygon 6 25)) (translate 0 0 -100) ))

(define pencil-shell (extrude pencil-outline (translate 0 0 200)))

(object pencil0 Group
  (add pencil-shell pencil-yellow-mat)
  (add pencil-shell (scale 0.98 0.98 0.98) pencil-wood-mat)
  (add cylinder (compose (scale 2 2 2) (scale 0.06 1.1 0.06) (xRot -90)) pencil-graphite-mat)
  )
(object pencil1 Intersection
  (add pencil0)
  (add cone (compose (scale 2 2 2) (scale 0.65 1 0.65) (xRot -90)))
  )
(object pencil Group
  (add pencil1)
  (add attachment (compose (scale .25 .25 .2) (translate 0 0 100)) attachment-mat)
  (scale .6 .6 1)
  (translate 0 0 -160)
  )

;;;;;;;;;;;;;;;;;;;
; Pilot point
; (pick-color)
(object pilot-plastic-mat Material
  (color '(0.929412 0.0941176 0.117647))
  (type 'plastic)
  (specularity .1)
  )

(object pilot-ink-mat Material
  (color '(0.929412 0.0941176 0.117647))
  (type 'plaster)
  (specularity .1)
  )

(object pilot-metal-mat Material
  (color white)
  (type 'plastic)
  (specularity 0.3)
  )

(define pilot-grip-base
  (sweep (append '((0 -80 0))
                 (polyXform (2to3d
                             '((-6.39758e-05 -100) (16.4594 -98.6361) (32.4699 -94.5817) (47.5947 -87.9474) (61.4212 -78.9141) (73.5724 -67.7282) (83.7166 -54.6948) (91.5773 -40.1696) (96.94 -24.5486) (99.6584 -8.25795) (99.6584 8.25793) ))(compose (scale .06 .8 1) (translate -12 0 0))) '((0 6.6 0))
                                                                                                                                                                                                                                                                                                ) 50)
  )

(object pilot-grip Difference
  (add pilot-grip-base (compose (translate 0 80 0) (xRot -90)) pilot-plastic-mat)
  (add cube (compose (scale 2 2 2) (translate 0 0 -100) (scale 1 1 3) (translate 0 0 -50)))
  )

(object pilot-nose0 Group
  (add cylinder (compose (scale 2 2 2)(translate 0 100 0) (scale .06 .02 .06)) pilot-metal-mat)
  (add cone     (compose (scale 2 2 2)(translate 0 100 0) (scale .06 .10 .06) (translate 0 4 0)) pilot-metal-mat)
  )
(object pilot-nose1 Difference
  (add pilot-nose0)
  (add cylinder (compose (scale 2 2 2)(translate 0 110 0)))
  )
(object pilot-nose Group
  (add pilot-nose1)
  (add cylinder (compose (scale 2 2 2) (translate 0 100 0) (scale .02 .08 .02)) pilot-metal-mat)
  (add sphere (compose (scale 2 2 2) (translate 0 100 0) (scale 0.015 .10 0.015)) pilot-ink-mat)
  )

(object pilot0 Difference
  (add sphere (compose (scale 2 2 2) (scale .167 .167 2) (translate 0 0 100)) pilot-plastic-mat)
  (add cube (compose (scale 2 2 2) (translate 0 0 200)))
  (add cube (compose (scale 2 2 2) (translate 0 0 -100) (scale 1 1 2) (translate 0 0 -33)))
  )
(object pilot Group
  (add pilot0)
  (add pilot-grip (translate 0 0 -33) pilot-plastic-mat)
  (add pilot-nose (compose (xRot -90) (scale .8 .8 1) (translate 0 0 -80)))
  (add attachment (compose (scale .167 .167 .2) (translate 0 0 100)) attachment-mat)
  (translate 0 0 -160)
  )

;;;;;;;;
;; Montblanc
;; (pick-color)

(object mb-plastic-mat Material
  (type 'plastic)
  (color black)
  (specularity .2)
  )

(object mb-inker-mat Material
  (type 'plaster)
  (color black)
  ;(specularColor white)
  (specularity .1)
  )

(object mb-metal-mat Material
  (type 'plastic)
  (color '(1 0.8405 0.13))
  (specularity 0.2)
  (reflection 0.3)
  )

(object mb-nib-mat Material
  (type 'plastic)
  (color '(.75 .75 .8))
  (specularity 0.3)
  (reflection 0.5)
  )

(object montblanc0 Difference
  (add sphere (compose (scale 2 2 2) (scale .19 .19 2) (translate 0 0 100)) mb-plastic-mat)
  (add cube (compose (scale 2 2 2) (translate 0 0 200)))
  (add cube (compose (scale 2 2 2) (translate 0 0 -100) (scale 1 1 2) (translate 0 0 -25)))
  )
(object montblanc1 Group
  (add montblanc0)
  (add cone (compose (scale 2 2 2) (xRot -90) (translate 0 0 -100) (scale .15 .15 .375) (translate 0 0 -25)) mb-metal-mat)
  )
(object montblanc2 Difference
  (add montblanc1)
  (add cone (compose (scale 2 2 2) (xRot -90) (translate 0 0 -100) (scale .15 .15 .375) (translate 0 0 -18)))
  (add cube (compose (scale 2 2 2) (translate 0 0 -180)))
  )
(object montblanc Group
  (add montblanc2)
  (add attachment (compose (scale .19 .19 .20) (translate 0 0 100)) attachment-mat)
  (translate 0 0 -160)
  )

(object inkercyl Group
  (add cylinder (compose (scale 2 2 2) (xRot -90) (scale .10 .05 .01)))
  )

(object inker Group
  (add inkercyl (translate 0 0 -5))
  (add inkercyl (translate 0 0 -10))
  (add inkercyl (translate 0 0 -15))
  (add inkercyl (translate 0 0 -20))
  (add inkercyl (translate 0 0 -25))
  (add inkercyl (translate 0 0 -30))
  (add inkercyl (translate 0 0 -35))
  )

(object well Intersection
  (add inker)
  (add cone (compose (scale 2 2 2) (xRot 90) (translate 0 0 -53) (scale .2 .1 .5) (xRot -8) (translate 0 2 0)))
  )

(object nibcone Difference
  (add cone (compose (scale 2 2 2) (xRot 90) (translate 0 0 -50) (scale .20 .10 .5)))
  (add cone (compose (scale 2 2 2) (xRot 90) (translate 0 0 -53) (scale .20 .1 .5)))
  )

(object nibtop Difference
  (add nibcone (compose (xRot -8) (translate 0 2 0)))
  (add cube (compose (scale 2 2 2) (translate 0 0 100)))
  (add cube (compose (scale 2 2 2) (translate 0 -100 0)))
  (add cube (compose (scale 2 2 2) (translate 0 0 -165)))
  )

(object nib Difference
  ; (add well (identity) mb-inker-mat)
  (add nibtop mb-nib-mat)
  (add cylinder (compose (scale 2 2 2) (scale .18 1 .35) (translate 20 0 -75)))
  (add cylinder (compose (scale 2 2 2) (scale .18 1 .35) (translate -20 0 -75)))
  (add cylinder (compose (scale 2 2 2) (scale .02 1 .02) (translate 0 0 -30)))
  (add cube (compose (scale 2 2 2) (translate 0 0 -100) (scale 0.005 1 .25) (translate 0 0 -30))) 
  )

(object fountblanc0 Difference
  (add cone (compose (scale 2 2 2) (xRot -90) (translate 0 0 -100) (scale .19 .19 2.81) (translate 0 0 100)) mb-plastic-mat)
  ; (subtractchild cube (translate 0 0 200))
  (add cube (compose (scale 2 2 2) (translate 0 0 -100) (scale 1 1 3) (translate 0 0 -25)))
  )
(object fountblanc Group
  (add fountblanc0)
  (add cylinder (compose (scale 2 2 2) (xRot -90) (translate 0 0 -100) (scale .16 .16 .02) (translate 0 0 -25)) mb-metal-mat)
  (add cylinder (compose (scale 2 2 2) (xRot -90) (translate 0 0 100) (scale .19 .19 .02) (translate 0 0 50)) mb-metal-mat)
  ;(subtractchild cylinder (compose (xRot -90) (translate 0 0 -100) (scale .15 .15 .01) (translate 0 0 -18)))
  ;(subtractchild cube (translate 0 0 -180))
  (add nib (compose (translate 0 0 -20)))
  (add attachment (compose (scale .19 .19 .20) (translate 0 0 100)) attachment-mat)
  (translate 0 0 -160)
  )

;;;;;;
;; chalk
;; (pick-color)
(object chalk-mat Material
        (type 'plaster)
        (color '(.8 .8 .8))
        (specularity 0)
        )

(object chalk0 Difference
        (add cylinder (compose (scale 2 2 2) (xRot -90) (scale .2 .2 1)) chalk-mat)
        (add cube (compose (scale 2 2 2) (translate 100 0 0) (yRot 70) (translate 0 0 -100)))
        (add cube (compose (scale 2 2 2) (translate -100 0 0) (yRot -30) (zRot 10) (translate 0 0 -100)))
        (add cube (compose (scale 2 2 2) (translate 0 100 0) (xRot -45) (zRot 10) (translate 0 0 -100)))
  )
(object chalk Group
  (add chalk0)
  (add attachment (compose (scale .2 .2 .2) (translate 0 0 100)) attachment-mat)
  (translate 0 0 -160)
  )
;; Tootsie Roll Pop
;;
(define orange (hsv2rgb '(30 1 1)))
(object tang Material
        (color orange)
        (transparency 0.5)
        (reflection .0)
        (refraction 1.5)
        (diffuse .9)
        (specularity 0)
        (roughness 1)
        )
                  
(object pop0 Group
        
        (add sphere (scale .9 .9 .9) tang)
        (add cylinder (compose
                       (scale 1.1 .45 1.1)
                       (zRot -90)) tang)
        (add cylinder (compose
                       (translate 0 -50 0)
                       (scale .16 4 .16))
             whitePlaster)
        (yRot 45)
        (translate 0 200 0)
        (scale .5 .5 .5)
        (xRot -90)
        )
(object pop Group
  (add pop0)
  (add attachment (compose (scale .04 .04 .2) (translate 0 0 100)) attachment-mat)
  (translate 0 0 -160)
  )

;; SETUP
(object lights Group
  (add bulb (translate 150 200 0))
  (add bulb (translate -150 200 0))
  (add bulb (translate 0 200 -200))
  (add cube (compose (scale 2 2 2) (scale 10 .1 10) (translate 0 -50 0)) table-mat)
  )

(object scene Group
  (add lights)
  (add chalk (compose (translate -4 0 0) (xRot 135) (translate 0 0 100)))
  (add pencil (compose (translate 4 0 0) (xRot 75) (translate 0 0 100)))
  (add montblanc (compose (translate 0 0 0) (xRot 5) (translate 0 0 -100)))
  (add pilot (compose (translate -4 0 0) (xRot 50) (translate 0 0 -100)))
  (add pop (compose (translate -4 0 0) (xRot 100) (translate 0 0 -100)))
  (add case)
  )

(object chalk-scene Group
        (add chalk)
        (add lights)
        )

(object pencil-scene Group
        (add pencil (xRot 5) (yRot 30))
        (add lights)
        )

(object pen-scene Group
        (add montblanc)
        (add lights)
        )

(object fount-scene Group
        (add pop (yRot -30))
        (add lights)
        )

(object pilot-scene Group
        (add pilot (yRot 30))
        (add lights)
        )

(object shell-scene Group
        (add case)
        (add lights)
        )


(object scene1 Group
        (add fountblanc (translate -50 0 0))
        (add montblanc (translate 50 0 0))
        )

;(colordev (setdevicesize 600 400))
;(colordev (setdevicesize 300 200))

;(detail1 (getcamera))
; (profile (getcameraalt))
(tell chalk-cam
 (pos '(-647.17 173.409 -150))
 (direction '(0.965926 -0.258819 0))
 (subject 'chalk-scene)
 (angle 45)
 )
; (fount-cam (getcamera))
(tell fount-cam
 (pos '(-77.0463 230.693 -516.251))
 (direction '(0.200633 -0.557597 0.805501)) ; up angle -42.3327)
 (subject 'fount-scene)
 (angle 45)
 )

(tell pen-cam
 (pos '(0 50 -500))
 (coi '(0 0 0))
 (subject 'pen-scene)
 (angle 45)
 )

(tell pencil-cam
 (pos '(-647.17 173.409 -150))
 (direction '(0.965926 -0.258819 0))
 (subject 'pencil-scene)
 (angle 45)
 )
;(pilot-cam (getcamera))
(tell pilot-cam
 (pos '(-516.77 138.468 -135))
 (direction '(0.965926 -0.258819 -9.76048e-10)) ; up angle -30)
 (subject 'pilot-scene)
 (angle 45)
 )

;(shell-cam (getcamera))
(tell shell-cam
 (pos '(-150 50 -400))
 (coi '(0 0 0))
 (subject 'shell-scene)
 (angle 45)
 )

(tell profile
 ;(setcamera  '(748.127 149.906 1295.76) '(-0.499387 -0.0499387 -0.864939) 0)
 (pos '(-671.746 760.519 -1163.47))
 (coi '(0 100 0))
 (subject 'scene)
 (angle 35)
 )

(tell detail1
 (pos '(-361.84 156.462 -686.702))
 (direction '(0.499388 0.0499387 0.864938))
 (subject 'scene)
 (angle 54)
 )

(tell detail2
 (pos '(0 0 -500 ))
 (direction '(0 0 1))
 (subject 'scene)
 (angle 45)
 )

(tell image (antiAlias 1))
(tell chalk-cam (shoot))
(tell fount-cam (shoot))
(tell pencil-cam (shoot))
(tell pilot-cam (shoot))
(tell shell-cam (shoot))

(tell profile (shoot))
(tell detail1 (shoot))

; unneeded
;;(tell pen-cam (shoot))

;;(tell detail2 (shoot))